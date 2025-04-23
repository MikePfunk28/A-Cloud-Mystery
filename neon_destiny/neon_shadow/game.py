import os
import sys
import time
import json
import copy
import random
import uuid
from collections import defaultdict
from typing import Dict, Optional, List, Union, Set, Any, Tuple

from neon_shadow.constants import (
    CLR_RESET, CLR_TITLE, CLR_SECTION, CLR_ERROR, CLR_SUCCESS,
    CLR_WARNING, CLR_BRIGHT, CLR_CYAN, CLR_CREDITS, CLR_SHADOW_ADMIN,
    CLR_CLUE, CLR_HAZARD, CLR_BONUS, PRESS_ENTER
)
from neon_shadow.ui import (
    clear_screen, print_slow, display_ascii_art, display_loading_bar,
    terminal_effect, hacker_animation, display_choices,
    display_notification, display_mini_map, display_aws_info
)
from neon_shadow.utils import get_valid_input, confirm_action
from neon_shadow.player import CloudRanger
from neon_shadow.location import Location
from neon_shadow.quest import Quest
from neon_shadow.event import CloudEvent
from neon_shadow.artifact import CloudArtifact
from neon_shadow.service import CloudService

# Import content
from neon_shadow.content.artifacts import ARTIFACTS
from neon_shadow.content.services import SERVICES
from neon_shadow.content.quests import QUESTS
from neon_shadow.content.events import EVENTS
from neon_shadow.content.locations import LOCATIONS
from neon_shadow.content.vendors import VENDORS
from neon_shadow.content.weather import WEATHER_TYPES, SEVERITY_LEVELS, REGIONAL_WEATHER_TENDENCIES


class Game:
    """Main game class that manages the game state and flow."""

    def __init__(self, difficulty: str = "normal") -> None:
        """Initialize a new game.

        Args:
            difficulty: Game difficulty level ("easy", "normal", or "hard")
        """
        # Initialize core game components
        self.player: Optional[CloudRanger] = None
        self.current_location: Optional[Location] = None
        self.locations: Dict[str, Location] = {}
        self.quests: Dict[str, Quest] = {}
        self.events: Dict[str, CloudEvent] = {}
        self.artifacts: Dict[str, Dict[str, Any]] = {}
        self.services: Dict[str, Dict[str, Any]] = {}

        # Game state variables
        self.current_day: int = 1
        self.game_over: bool = False
        self.game_won: bool = False
        self.difficulty: str = difficulty
        self.win_reason: str = ""
        self.paused: bool = False
        self.battle_mode: bool = False
        self.debug_mode: bool = False
        self.current_enemy: Optional[Any] = None
        self.discovered_locations: Set[str] = set()
        self.weather_conditions: Dict[str, Dict[str, Any]] = {}
        self.global_events: List[str] = []

        # Create game content
        self._create_locations()
        self._create_artifacts()
        self._create_services()
        self._create_quests()
        self._create_events()
        self._create_weather_conditions()
        self._create_vendors()

    def _create_locations(self) -> None:
        """Create game world locations from the LOCATIONS data."""
        for loc_id, loc_data in LOCATIONS.items():
            # Create the base location
            location = Location(
                name=loc_data["name"],
                description=loc_data["description"],
                region=loc_data.get("region"),
                connections=loc_data.get("connections", []),
                events=loc_data.get("events", []),
                services=loc_data.get("services", []),
                difficulty=loc_data.get("difficulty", 1)
            )

            # Add hazards if present
            if "hazards" in loc_data:
                for hazard in loc_data["hazards"]:
                    location.add_hazard(hazard)

            # Store the location
            self.locations[loc_data["name"]] = location

    def _create_artifacts(self) -> None:
        """Create artifact templates from the ARTIFACTS data."""
        self.artifacts = ARTIFACTS

    def _create_services(self) -> None:
        """Create service templates from the SERVICES data."""
        self.services = SERVICES

    def _create_quests(self) -> None:
        """Create game quests from the QUESTS data."""
        for quest_id, quest_data in QUESTS.items():
            quest = Quest(
                id=quest_data["id"],
                title=quest_data["title"],
                description=quest_data["description"],
                objectives=quest_data["objectives"],
                reward=quest_data["reward"],
                prereq_quests=quest_data.get("prereq_quests", []),
                min_skill_level=quest_data.get("min_skill_level", {}),
                min_faction_rep=quest_data.get("min_faction_rep", {}),
                location=quest_data.get("location")
            )

            # Set additional properties
            if "difficulty" in quest_data:
                quest.difficulty = quest_data["difficulty"]
            if "time_limit" in quest_data:
                quest.time_limit = quest_data["time_limit"]
            if "hidden" in quest_data:
                quest.hidden = quest_data["hidden"]

            self.quests[quest_id] = quest

    def _create_events(self) -> None:
        """Create game events from the EVENTS data."""
        for event_id, event_data in EVENTS.items():
            event = CloudEvent(
                id=event_data["id"],
                name=event_data["name"],
                description=event_data["description"],
                event_type=event_data["event_type"],
                effects=event_data.get("effects", {}),
                requirements=event_data.get("requirements", {}),
                chance=event_data.get("chance", 100),
                repeatable=event_data.get("repeatable", False)
            )

            # Set additional properties
            if "cooldown_duration" in event_data:
                event.cooldown_duration = event_data["cooldown_duration"]

            self.events[event_id] = event

    def _create_weather_conditions(self) -> None:
        """Create weather conditions for locations."""
        for loc_name, location in self.locations.items():
            # Choose appropriate weather based on region
            region = location.region if location.region else "unknown"
            regional_weather = REGIONAL_WEATHER_TENDENCIES.get(region,
                                                             REGIONAL_WEATHER_TENDENCIES["unknown"])

            # Weight toward region-appropriate weather but allow any
            if random.randint(1, 100) <= 70:  # 70% chance for regional weather
                weather_name = random.choice(regional_weather)
                weather = next((w for w in WEATHER_TYPES if w["name"] == weather_name),
                              random.choice(WEATHER_TYPES))
            else:
                weather = random.choice(WEATHER_TYPES)

            # Severity based on location difficulty
            severity_level = min(
                6, max(1, location.difficulty // 2 + random.randint(-1, 1)))
            severity = SEVERITY_LEVELS[severity_level]

            self.weather_conditions[loc_name] = {
                "current": weather,
                # Weather will change after this many days
                "duration": random.randint(2, 5),
                "severity": severity,
                "severity_level": severity_level
            }

    def _create_vendors(self) -> None:
        """Create vendors for various locations based on VENDORS data."""
        for vendor_id, vendor_data in VENDORS.items():
            if vendor_data["location"] in LOCATIONS:
                location_name = LOCATIONS[vendor_data["location"]]["name"]
                if location_name in self.locations:
                    self.locations[location_name].add_vendor({
                        "name": vendor_data["name"],
                        "description": vendor_data["description"],
                        "inventory": vendor_data["inventory"],
                        "reputation_required": vendor_data.get("reputation_required", {})
                    })

    def start_game(self) -> None:
        """Start a new game."""
        print(
            f"\n{CLR_TITLE}╔══════════════════════════════════════════════════════════╗{CLR_RESET}")
        print(
            f"{CLR_TITLE}║            CLOUD RANGER: DIGITAL FRONTIER                ║{CLR_RESET}")
        print(
            f"{CLR_TITLE}╚══════════════════════════════════════════════════════════╝{CLR_RESET}")

        print_slow(
            "\nWelcome to the world of Cloud Ranger, where digital infrastructure comes to life!")
        print_slow(
            "As a newly recruited Cloud Ranger, your mission is to protect the cloud, solve mysteries,")
        print_slow("and uncover the identity of the notorious Shadow Admin.")

        print(f"\n{CLR_SECTION}[CHARACTER CREATION]{CLR_RESET}")
        name = input("Enter your ranger name: ")

        print("\nSelect your specialization:")
        print("1. Security Specialist (Security +2, Investigation +1)")
        print("2. Network Engineer (Network +2, Cloud +1)")
        print("3. Database Administrator (Database +2, Serverless +1)")
        print("4. DevOps Engineer (Cloud +2, Security +1)")

        choice = get_valid_input("Enter your choice (1-4): ", range(1, 5))

        # Set initial skills based on specialization
        initial_skills = {}
        if choice == 1:
            initial_skills = {"security": 2, "investigation": 1}
            specialty = "Security Specialist"
        elif choice == 2:
            initial_skills = {"networking": 2, "cloud": 1}
            specialty = "Network Engineer"
        elif choice == 3:
            initial_skills = {"database": 2, "serverless": 1}
            specialty = "Database Administrator"
        else:
            initial_skills = {"cloud": 2, "security": 1}
            specialty = "DevOps Engineer"

        # Create player with starting location
        self.player = CloudRanger(name, specialty, initial_skills)
        self.player.current_location = self.locations.get("Cloud City")

        # Give tutorial quest
        tutorial_quest = self.quests.get("tutorial")
        if tutorial_quest:
            self.player.active_quests.append(tutorial_quest.id)
        else:
            print(f"{CLR_WARNING}Warning: Tutorial quest not found!{CLR_RESET}")

        # Set game parameters based on difficulty
        if self.difficulty == "easy":
            self.player.cloud_credits = 750
            self.player.time_left = 400
            s3_scanner_data = self.artifacts.get("S3_Scanner")
            if s3_scanner_data:
                scanner = CloudArtifact(
                    s3_scanner_data["name"],
                    s3_scanner_data["description"],
                    s3_scanner_data["artifact_type"],
                    s3_scanner_data["aws_service"],
                    s3_scanner_data["cost"],
                    s3_scanner_data["power"]
                )
                self.player.add_artifact(scanner)

        elif self.difficulty == "normal":
            self.player.cloud_credits = 500
            self.player.time_left = 365
        else:  # hard
            self.player.cloud_credits = 300
            self.player.time_left = 300

        print(f"\n{CLR_SUCCESS}Character created! Welcome, {self.player.name} the {self.player.specialty}!{CLR_RESET}")
        input("\nPress Enter to begin your adventure...")

        # Start the game loop
        if self.player:
            self.game_loop()

    def game_loop(self) -> None:
        """Main game loop."""
        if not self.player:
            print(f"{CLR_ERROR}Error: No player initialized{CLR_RESET}")
            return

        while not self.game_over:
            if not self.player.current_location:
                print(f"{CLR_ERROR}Error: Player location not set{CLR_RESET}")
                break

            self.update_game_state()
            self.display_status()

            # Location events
            current_loc_name = self.player.current_location.name
            self.player.current_location.display()

            # Check for triggerable events
            self.check_events()

            # Check for location hazards
            self.check_hazards()

            # Display actions
            self.display_actions()
            choice = self.get_player_action()
            self.process_action(choice)

            # Check win/lose conditions after each turn
            if self.check_game_over():
                break

        # Game over
        self.end_game()

    def update_game_state(self) -> None:
        """Update game state at the beginning of each turn."""
        if not self.player or self.game_over:
            return

        self.current_day += 1  # Advance time first

        # --- Update Weather --- #
        self.update_weather()

        # --- Update Deployed Services --- #
        total_income = 0
        total_costs = 0
        services_to_remove = []  # Track instance IDs of services that failed

        # Use a copy in case the list is modified during iteration
        if hasattr(self.player.inventory, 'deployed_services'):
            deployed_services_copy = self.player.inventory.deployed_services[:]

            for service in deployed_services_copy:
                if not service.is_deployed:
                    continue  # Skip offline services

                # Update uptime and status effects
                service.uptime_days += 1
                service.update_status_effects()

                # --- Calculate Income/Costs --- #
                income = service.calculate_revenue()
                cost = service.cost_per_hour * 24  # Daily cost
                total_income += income * 24  # Daily income
                total_costs += cost

                # --- Random Events for Services --- #
                event_chance = 5  # Base 5% chance per service per day
                # Increase chance based on factors:
                event_chance += service.uptime_days // 10  # +1% every 10 days uptime
                event_chance -= service.security_level    # Higher security reduces chance

                # Apply location difficulty modifier
                current_loc_name = self.player.current_location.name if self.player.current_location else None
                if current_loc_name and current_loc_name in self.locations:
                    # Higher location difficulty increases chance
                    event_chance += self.locations[current_loc_name].difficulty // 2

                # Apply weather effects
                if current_loc_name in self.weather_conditions:
                    weather = self.weather_conditions[current_loc_name]
                    if "Memory Frost" in weather["current"]["name"]:
                        service.performance = max(1, service.performance - 1)

                # Apply difficulty modifier
                if self.difficulty == 'easy':
                    event_chance *= 0.7  # Reduce chance on easy
                elif self.difficulty == 'hard':
                    event_chance *= 1.5  # Increase chance on hard

                # Trigger service event if roll succeeds
                if random.randint(1, 100) <= max(1, int(event_chance)):
                    service_failed = self._trigger_service_event(service)
                    if service_failed:
                        services_to_remove.append(service.instance_id)

            # Apply income/costs
            net_change = total_income - total_costs
            if net_change != 0:  # Only add if there's a change
                self.player.cloud_credits += net_change  # Apply net change

            # Remove services that failed this turn
            for instance_id in services_to_remove:
                self.player.inventory.remove_deployed_service(instance_id)

        # --- Update Player State --- #
        # Update artifacts cooldowns
        if hasattr(self.player.inventory, 'update_all_artifacts'):
            self.player.inventory.update_all_artifacts()

        # Update player status effects
        self.player.update_status_effects()

        # Update event cooldowns
        for event in self.events.values():
            event.update_cooldown()

        # Apply temporary skill boosts/debuffs (decrement duration)
        updated_boosts = []
        for boost in self.player.temp_skill_boosts:
            boost['remaining_days'] -= 1
            if boost['remaining_days'] > 0:
                updated_boosts.append(boost)
            else:
                display_notification(
                    f"Skill boost for {boost['skill']} expired.", "info")
        self.player.temp_skill_boosts = updated_boosts

        # Natural recovery (small amount each day)
        if self.player.health < self.player.max_health:
            self.player.heal(2)  # Small natural healing each day

        if self.player.energy < self.player.max_energy:
            self.player.restore_energy(5)  # Natural energy recovery

        # Check Player Time Limit AFTER updates for the day
        if self.current_day >= self.player.time_left:  # Use >= for clarity
            self.game_over = True
            # Use a more specific reason if player hasn't won
            if not self.game_won:
                self.win_reason = "You have run out of time! The Shadow Admin's plans have succeeded."
            return  # End update if out of time

        # --- Check Quest Progress --- #
        self.check_quest_progress()

    def update_weather(self) -> None:
        """Update weather conditions across all locations."""
        for loc_name, weather in self.weather_conditions.items():
            # Decrease duration counter
            weather["duration"] -= 1

            # Change weather if duration expired
            if weather["duration"] <= 0:
                # Determine location and its region
                region = "unknown"
                if loc_name in self.locations:
                    location = self.locations[loc_name]
                    region = location.region if location.region else "unknown"

                # Choose appropriate weather based on region
                regional_weather = REGIONAL_WEATHER_TENDENCIES.get(region,
                                                                REGIONAL_WEATHER_TENDENCIES["unknown"])

                # Weight toward region-appropriate weather but allow any
                if random.randint(1, 100) <= 70:  # 70% chance for regional weather
                    weather_name = random.choice(regional_weather)
                    new_weather = next((w for w in WEATHER_TYPES if w["name"] == weather_name),
                                      random.choice(WEATHER_TYPES))
                else:
                    new_weather = random.choice(WEATHER_TYPES)

                # Set new weather
                weather["current"] = new_weather
                weather["duration"] = random.randint(2, 5)

                # If this is the player's current location, notify them of the change
                if self.player and self.player.current_location and self.player.current_location.name == loc_name:
                    display_notification(
                        f"Weather changed to: {weather['current']['name']} - {weather['current']['effect']}",
                        "info")

    def check_hazards(self) -> None:
        """Check for hazards at the current location."""
        if not self.player or not self.player.current_location:
            return

        hazards = self.player.current_location.hazards
        if not hazards:
            return

        for hazard in hazards:
            # Check if hazard triggers
            if random.randint(1, 100) <= hazard.get("chance", 10):
                # Check if player can avoid it with skills
                avoidable_skill = hazard.get("avoidable_with_skill")
                if avoidable_skill and avoidable_skill in self.player.skills:
                    skill_level = self.player.skills[avoidable_skill]
                    # Higher skill gives better chance to avoid
                    avoid_chance = skill_level * 10
                    if random.randint(1, 100) <= avoid_chance:
                        display_notification(
                            f"You used your {avoidable_skill} skill to avoid the {hazard['name']}!",
                            "success")
                        continue

                # Hazard hits player
                # Handle string-based damage functions that came from the data file
                damage_func = hazard.get("damage", lambda: 10)
                if isinstance(damage_func, str) and "random.randint" in damage_func:
                    # Parse and evaluate the random damage function
                    # Be very careful with eval - this is safe only because we control the input
                    try:
                        damage = eval(damage_func)
                    except Exception:
                        damage = 10  # Default if evaluation fails
                elif callable(damage_func):
                    damage = damage_func()
                else:
                    # Try to convert to int if it's a fixed value
                    damage = int(damage_func)

                display_notification(
                    f"Hazard encountered: {hazard['name']} - {hazard['description']}",
                    "warning")

                self.player.take_damage(damage, hazard['name'])

                # Possible status effect from hazard
                if "status_effect" in hazard:
                    self.player.add_status_effect(hazard["status_effect"])

                break  # Only one hazard per turn for balance

    def check_quest_progress(self) -> None:
        """Check and update quest progress."""
        if not self.player:
            return

        # Get quests from player's active quests
        active_quests = []
        for quest_id in self.player.active_quests:
            if quest_id in self.quests:
                active_quests.append(self.quests[quest_id])

        # Check each active quest
        for quest in active_quests:
            # Auto-complete location-based objectives
            current_loc = self.player.current_location.name if self.player.current_location else None

            # Tutorial quest special handling
            if quest.id == "tutorial":
                # Check if player visited Cloud City
                if current_loc == "Cloud City" and not quest.objectives[0]["completed"]:
                    quest.objectives[0]["completed"] = True
                    display_notification(
                        "Tutorial Objective Completed: Visit Cloud City", "success")

                # Check if player has acquired an artifact
                if len(self.player.inventory.artifacts) > 0 and not quest.objectives[1]["completed"]:
                    quest.objectives[1]["completed"] = True
                    display_notification(
                        "Tutorial Objective Completed: Acquire your first artifact", "success")

                # Check if player has deployed a service
                if len(self.player.inventory.deployed_services) > 0 and not quest.objectives[2]["completed"]:
                    quest.objectives[2]["completed"] = True
                    display_notification(
                        "Tutorial Objective Completed: Deploy your first service", "success")

            # Mysterious outage quest special handling
            elif quest.id == "mysterious_outage":
                # Check if player visited Database District
                if current_loc == "Database District" and not quest.objectives[0]["completed"]:
                    quest.objectives[0]["completed"] = True
                    display_notification(
                        "Objective Completed: Visit Database District", "success")

                # Check if player reported findings at Security Perimeter
                if current_loc == "Security Perimeter" and quest.objectives[2]["completed"] and not quest.objectives[3]["completed"]:
                    quest.objectives[3]["completed"] = True
                    display_notification(
                        "Objective Completed: Report your findings to Security Perimeter", "success")

            # Check if all objectives are completed
            if all(obj["completed"] for obj in quest.objectives):
                self.complete_quest(quest)

    def complete_quest(self, quest: Quest) -> None:
        """Complete a quest and give rewards."""
        if not self.player:
            return

        # Mark quest as completed
        if quest.id in self.player.active_quests:
            self.player.active_quests.remove(quest.id)
        self.player.completed_quests.append(quest.id)

        # Quest completion notification
        display_notification(f"Quest Completed: {quest.title}!", "success")

        # Apply rewards
        rewards = quest.reward
        if "credits" in rewards:
            self.player.cloud_credits += rewards["credits"]
            display_notification(
                f"Reward: {rewards['credits']} Cloud Credits", "success")

        if "skill" in rewards:
            for skill, amount in rewards["skill"].items():
                self.player.increase_skill(skill, amount)

        if "faction_rep" in rewards:
            for faction, amount in rewards["faction_rep"].items():
                self.player.update_faction_reputation(faction, amount)

        if "artifacts" in rewards:
            for artifact_name in rewards["artifacts"]:
                if artifact_name in self.artifacts:
                    artifact_data = self.artifacts[artifact_name]
                    new_artifact = CloudArtifact(
                        artifact_data["name"],
                        artifact_data["description"],
                        artifact_data["artifact_type"],
                        artifact_data["aws_service"],
                        artifact_data["cost"],
                        artifact_data["power"]
                    )
                    self.player.add_artifact(new_artifact)

        if "consumables" in rewards:
            for item, count in rewards["consumables"].items():
                self.player.inventory.add_consumable(item, count)
                display_notification(f"Reward: {count}x {item}", "success")

        # Check for game-winning quest completion
        if quest.id == "shadow_admin":
            self.game_won = True
            self.game_over = True
            self.win_reason = "You have unmasked the Shadow Admin and saved Cloud City!"

    def _trigger_service_event(self, service: CloudService) -> bool:
        """Triggers a random negative event on a deployed service.

        Args:
            service: The service to trigger an event on

        Returns:
            True if service failed (health reached 0), False otherwise
        """
        if not service.is_deployed:
            return False  # Don't trigger on already offline services

        event_type = random.choice(
            ["health_hit", "performance_drop", "security_breach", "cost_spike"])
        location_difficulty = 0
        if self.player.current_location and self.player.current_location.name in self.locations:
            location_difficulty = self.locations[self.player.current_location.name].difficulty

        # Difficulty scaling for event severity
        severity_multiplier = 1.0
        if self.difficulty == 'easy':
            severity_multiplier = 0.7
        elif self.difficulty == 'hard':
            severity_multiplier = 1.3

        if event_type == "health_hit":
            damage = int((random.randint(5, 15) +
                          location_difficulty) * severity_multiplier)
            damage = max(1, damage)  # Ensure at least 1 damage
            display_notification(
                f"System Anomaly @ {service.name} ({service.instance_id}): Health -{damage}%", "warning")
            # Returns True if service failed
            return service.apply_damage(damage)

        elif event_type == "performance_drop":
            # More likely to be 1
            drop = int(random.choice([1, 1, 2]) * severity_multiplier)
            drop = max(1, drop)
            if service.performance > 1:
                service.performance = max(1, service.performance - drop)
                display_notification(
                    f"Resource Contention @ {service.name} ({service.instance_id}): Performance Degraded (-{drop})", "warning")
            return False  # Service didn't fail

        elif event_type == "security_breach":
            # More likely if security is low
            breach_chance = (10 - service.security_level) + location_difficulty
            if random.randint(1, 20) <= max(1, int(breach_chance * severity_multiplier)):
                severity = int(random.choice([1, 1, 2]) * severity_multiplier)
                severity = max(1, severity)
                if service.security_level > 1:
                    service.security_level = max(
                        1, service.security_level - severity)
                    display_notification(
                        f"Security Alert @ {service.name} ({service.instance_id}): Minor breach detected! Security -{severity}", "error")
                    # Potential for data leak clue?
                    if random.randint(1, 10) <= 3:
                        # Add random int for uniqueness
                        clue_id = f"breach_clue_{service.instance_id}_{random.randint(100, 999)}"
                        self.player.add_clue(clue_id)
                        print(
                            f"{CLR_CLUE}Evidence of data exfiltration found during the breach analysis.{CLR_RESET}")
                else:
                    # Security already minimal, trigger health hit instead
                    damage = int((random.randint(3, 8)) * severity_multiplier)
                    display_notification(
                        f"Security Alert @ {service.name} ({service.instance_id}): Breach attempted on unsecured service! Health -{damage}%", "error")
                    # Returns True if service failed
                    return service.apply_damage(damage)
            return False  # Service didn't fail

        elif event_type == "cost_spike":
            # Simulate unexpected usage spike
            cost_increase_multiplier = random.uniform(
                0.5, 1.5) * (location_difficulty / 5.0) * severity_multiplier
            cost_increase = service.cost_per_hour * cost_increase_multiplier
            # Ensure minimum cost spike
            cost_increase = max(0.1, cost_increase)
            self.player.cloud_credits -= cost_increase
            display_notification(
                f"Usage Spike @ {service.name} ({service.instance_id}): Unexpected costs! (-{cost_increase:.2f} Credits)", "warning")
            return False  # Service didn't fail

    def display_status(self) -> None:
        """Display player status and game information."""
        clear_screen()
        print(
            f"\n{CLR_TITLE}╔══════════════════════ CLOUD RANGER STATUS ══════════════════════╗{CLR_RESET}")
        # Delegate most display to player object
        if self.player:
            print(f"{CLR_TITLE}║{CLR_RESET} Day: {self.current_day} / {self.player.time_left}{' ' * (20 - len(str(self.current_day)) - len(str(self.player.time_left)))}{CLR_TITLE}║{CLR_RESET}")

            # Display current weather if available
            if self.player.current_location and self.player.current_location.name in self.weather_conditions:
                weather = self.weather_conditions[self.player.current_location.name]["current"]
                print(
                    f"{CLR_TITLE}║{CLR_RESET} Weather: {weather['name']} - {weather['effect']}{' ' * max(0, 20 - len(weather['name']) - len(weather['effect']))}{CLR_TITLE}║{CLR_RESET}")
        else:
            print(
                f"{CLR_TITLE}║{CLR_RESET} No active player.{' ' * 17}{CLR_TITLE}║{CLR_RESET}")
        print(
            f"{CLR_TITLE}╚═════════════════════════════════════════════════════════════════╝{CLR_RESET}")

    def display_actions(self) -> None:
        """Display available actions to the player."""
        print(f"\n{CLR_SECTION}[AVAILABLE ACTIONS]{CLR_RESET}")
        print("1. Explore Location")
        print("2. Travel")
        print("3. View Quests")
        print("4. View Inventory/Status")
        print("5. Manage Services")
        print("6. Use Artifact")
        print("7. Rest (skip day)")
        print("8. Interact with Vendors")
        print("9. System Menu (Save/Quit)")

    def get_player_action(self) -> int:
        """Get player's chosen action."""
        return get_valid_input("\nEnter your choice (1-9): ", range(1, 10))

    def process_action(self, choice: int) -> None:
        """Process the player's chosen action."""
        if choice == 1:
            self.explore_location()
        elif choice == 2:
            self.travel()
        elif choice == 3:
            self.view_quests()
        elif choice == 4:
            self.player.display_status()
        elif choice == 5:
            self.manage_services()
        elif choice == 6:
            self.use_artifact()
        elif choice == 7:
            self.rest()
        elif choice == 8:
            self.interact_with_vendors()
        elif choice == 9:
            self.system_menu()

    def explore_location(self) -> None:
        """Explore the current location for discoveries."""
        # Check if player has enough energy
        if not self.player.use_energy(10):
            display_notification(
                "Not enough energy to explore! (10 required)", "error")
            input(PRESS_ENTER)
            return

        print_slow(f"\nExploring {self.player.current_location.name}...")

        # Show exploring animation
        hacker_animation(1)

        # Check for special discoveries based on skills
        investigation_skill = self.player.skills.get("investigation", 0)
        discovery_chance = 30 + (investigation_skill * 5)

        # Location difficulty affects discovery chance
        location_difficulty = self.player.current_location.difficulty
        discovery_chance -= location_difficulty * 2

        # Weather effects on exploration
        if self.player.current_location.name in self.weather_conditions:
            weather = self.weather_conditions[self.player.current_location.name]["current"]
            if "Processing Fog" in weather["name"]:
                discovery_chance -= 15
                print(
                    f"{CLR_WARNING}The Processing Fog makes exploration more difficult.{CLR_RESET}")
            elif "Clear Signals" in weather["name"]:
                discovery_chance += 10
                print(
                    f"{CLR_SUCCESS}The Clear Signals improve your ability to explore.{CLR_RESET}")

        found_something = False

        if random.randint(1, 100) <= discovery_chance:
            # Generate a discovery
            discovery_type = random.choice(
                ["artifact", "clue", "credits", "service", "consumable"])

            if discovery_type == "artifact" and random.randint(1, 100) <= 30:
                # Find a random artifact based on location difficulty
                possible_artifacts = []
                for artifact_id, artifact_data in self.artifacts.items():
                    # Match artifact power to location difficulty
                    if location_difficulty >= 7 and artifact_data["power"] >= 6:
                        possible_artifacts.append((artifact_id, artifact_data))
                    elif 4 <= location_difficulty <= 6 and 3 <= artifact_data["power"] <= 7:
                        possible_artifacts.append((artifact_id, artifact_data))
                    elif location_difficulty <= 3 and artifact_data["power"] <= 4:
                        possible_artifacts.append((artifact_id, artifact_data))

                if possible_artifacts:
                    artifact_id, artifact_data = random.choice(
                        possible_artifacts)

                    new_artifact = CloudArtifact(
                        artifact_data["name"],
                        artifact_data["description"],
                        artifact_data["artifact_type"],
                        artifact_data["aws_service"],
                        artifact_data["cost"],
                        artifact_data["power"]
                    )

                    print(
                        f"\n{CLR_SUCCESS}You discovered a {new_artifact.name}!{CLR_RESET}")
                    print(f"{new_artifact.description}")

                    self.player.add_artifact(new_artifact)
                    found_something = True

            elif discovery_type == "clue":
                # Generate a meaningful clue based on location
                location_name = self.player.current_location.name
                clue_id = f"clue_{location_name}_{random.randint(1000, 9999)}"

                # More interesting clues in higher difficulty areas
                if location_difficulty >= 7:
                    clue_prefix = random.choice([
                        "You found encrypted data pointing to",
                        "A hidden terminal reveals information about",
                        "Secret communications indicate"
                    ])

                    clue_content = random.choice([
                        "the Shadow Admin's next target",
                        "a sophisticated attack pattern",
                        "unauthorized resource provisioning",
                        "a backdoor in critical infrastructure"
                    ])
                else:
                    clue_prefix = random.choice([
                        "You discovered evidence of",
                        "System logs indicate",
                        "You found traces of"
                    ])

                    clue_content = random.choice([
                        "unusual activity",
                        "suspicious logins",
                        "modified configurations",
                        "unauthorized access attempts"
                    ])

                clue_text = f"{clue_prefix} {clue_content} in {location_name}."

                self.player.add_clue(clue_id)
                print(f"\n{CLR_SUCCESS}You discovered a clue!{CLR_RESET}")
                print(f"{clue_text}")
                found_something = True

            elif discovery_type == "credits":
                # Credits scale with location difficulty
                base_credits = 10
                difficulty_bonus = location_difficulty * 5
                credits_found = random.randint(
                    base_credits, base_credits + difficulty_bonus)

                self.player.cloud_credits += credits_found
                print(
                    f"\n{CLR_SUCCESS}You found {credits_found} Cloud Credits!{CLR_RESET}")
                found_something = True

            elif discovery_type == "service":
                # Find a random service suitable for the location
                service_candidates = []
                for svc_id, svc_data in self.services.items():
                    # Check if service is appropriate for location difficulty
                    if (location_difficulty <= 3 and svc_data["deploy_cost"] <= 10) or \
                        (4 <= location_difficulty <= 6 and 5 <= svc_data["deploy_cost"] <= 20) or \
                            (location_difficulty >= 7 and svc_data["deploy_cost"] >= 15):
                        # Check if service is available in this region
                        if "global" in svc_data["region_availability"] or \
                                (self.player.current_location.region in svc_data["region_availability"]):
                            service_candidates.append((svc_id, svc_data))

                if service_candidates:
                    service_id, service_data = random.choice(
                        service_candidates)

                    new_service = CloudService(
                        service_data["name"],
                        service_data["description"],
                        service_data["service_type"],
                        service_data["cost_per_hour"],
                        service_data["deploy_cost"],
                        service_data["region_availability"],
                        service_data["dependencies"]
                    )

                    print(
                        f"\n{CLR_SUCCESS}You discovered {new_service.name} service!{CLR_RESET}")
                    print(f"{new_service.description}")

                    self.player.add_service(new_service)
                    found_something = True

            elif discovery_type == "consumable":
                # Find consumables
                consumable_types = [
                    {"name": "Emergency Patch", "description": "Restores 30 health"},
                    {"name": "Energy Cell", "description": "Restores 50 energy"},
                    {"name": "Firewall Patch",
                        "description": "Increases service security by 2"},
                    {"name": "Performance Tuner",
                        "description": "Increases service performance by 2"}
                ]

                # Higher difficulty areas have better chances for more items
                count = 1
                if location_difficulty >= 5:
                    count = random.randint(1, 2)
                if location_difficulty >= 8:
                    count = random.randint(1, 3)

                consumable = random.choice(consumable_types)
                self.player.inventory.add_consumable(consumable["name"], count)

                print(
                    f"\n{CLR_SUCCESS}You found {count}x {consumable['name']}!{CLR_RESET}")
                print(f"{consumable['description']}")
                found_something = True

        # Only print "nothing of interest" if we truly found nothing
        if not found_something:
            print("\nYou found nothing of interest.")

        # Exploring takes time
        self.current_day += 1
        input("\nPress Enter to continue...")

    def travel(self) -> None:
        """Travel to a different location."""
        current_location = self.player.current_location

        print(
            f"\n{CLR_SECTION}[TRAVEL FROM {current_location.name}]{CLR_RESET}")

        if not current_location.connections:
            print("There are no accessible locations from here.")
            return

        print("Available destinations:")
        for i, destination in enumerate(current_location.connections, 1):
            if destination in self.locations:
                difficulty = self.locations[destination].difficulty
                diff_stars = '★' * difficulty + '☆' * (10 - difficulty)
                print(f"{i}. {destination} - Difficulty: {diff_stars}")
            else:
                print(f"{i}. {destination} - ERROR: Location not found")

        print(f"{len(current_location.connections) + 1}. Cancel")

        choice = get_valid_input("\nEnter your choice: ", range(
            1, len(current_location.connections) + 2))

        if choice == len(current_location.connections) + 1:
            print("Travel canceled.")
            return

        # Add validation before accessing connections
        if not isinstance(choice, int) or choice < 1 or choice > len(current_location.connections):
            print(f"{CLR_ERROR}Invalid choice for travel destination.{CLR_RESET}")
            return

        destination_name = current_location.connections[choice - 1]
        if destination_name not in self.locations:
            print(
                f"{CLR_ERROR}Error: Destination '{destination_name}' not found in game locations!{CLR_RESET}")
            return

        destination = self.locations[destination_name]

        # Check if player has enough energy
        travel_energy = 15 + (destination.difficulty -
                              current_location.difficulty) * 2
        travel_energy = max(10, travel_energy)  # Minimum 10 energy

        if not self.player.use_energy(travel_energy):
            display_notification(
                f"Not enough energy to travel! ({travel_energy} required)", "error")
            input(PRESS_ENTER)
            return

        # Check if player can travel to this location
        if destination.difficulty > max(self.player.skills.values()) + 3:
            print(
                f"\n{CLR_ERROR}This location is too dangerous for your current skill level!{CLR_RESET}")
            print(
                f"You need more experience before traveling to {destination_name}.")

            # Refund energy since travel failed
            self.player.restore_energy(travel_energy)
            input("\nPress Enter to continue...")
            return

        # Travel successful
        self.player.current_location = destination

        # Add to discovered locations
        self.discovered_locations.add(destination_name)

        # Travel takes time
        self.current_day += 1
        print(f"\n{CLR_SUCCESS}You have arrived at {destination_name}.{CLR_RESET}")

        # Display weather at the new location
        if destination_name in self.weather_conditions:
            weather = self.weather_conditions[destination_name]["current"]
            print(
                f"{CLR_CYAN}Current weather: {weather['name']} - {weather['description']}{CLR_RESET}")

            # Apply immediate weather effects
            if "CPU Heatwave" in weather["name"]:
                energy_loss = int(self.player.energy * 0.1)
                if energy_loss > 0:
                    self.player.use_energy(energy_loss)
                    print(
                        f"{CLR_WARNING}The CPU Heatwave drains {energy_loss} energy!{CLR_RESET}")

            elif "Data Storm" in weather["name"]:
                bandwidth_loss = int(self.player.bandwidth * 0.2)
                if bandwidth_loss > 0:
                    self.player.bandwidth -= bandwidth_loss
                    print(
                        f"{CLR_WARNING}The Data Storm reduces your bandwidth by {bandwidth_loss}!{CLR_RESET}")

        input("\nPress Enter to continue...")

    def view_quests(self) -> None:
        """View active and available quests."""
        print(f"\n{CLR_SECTION}[ACTIVE QUESTS]{CLR_RESET}")

        active_quests = []
        for quest_id in self.player.active_quests:
            if quest_id in self.quests:
                active_quests.append(self.quests[quest_id])

        if not active_quests:
            print("You have no active quests.")
        else:
            for i, quest in enumerate(active_quests, 1):
                # Calculate completion percentage
                completed = sum(
                    1 for obj in quest.objectives if obj["completed"])
                total = len(quest.objectives)
                percentage = (completed / total) * 100
                print(
                    f"{i}. {quest.title} - Progress: {completed}/{total} ({percentage:.0f}%)")

            print("\nSelect a quest to view details (0 to return):")
            choice = get_valid_input("Enter quest number: ", range(
                0, len(active_quests) + 1))

            if choice > 0:
                active_quests[choice - 1].display()

        # Check for available quests at this location
        current_loc = self.player.current_location.name
        available_quests = []

        # Logic to determine available quests based on location and player progress
        for quest_id, quest in self.quests.items():
            # Skip quests already active or completed
            if quest_id in self.player.active_quests or quest_id in self.player.completed_quests:
                continue

            # Check location requirements if any
            if quest.location and quest.location != current_loc:
                continue

            # Check if quest prerequisites are met
            if quest.is_available(self.player):
                available_quests.append(quest)

        # Display available quests
        if available_quests:
            print(f"\n{CLR_SECTION}[AVAILABLE QUESTS]{CLR_RESET}")
            for i, quest in enumerate(available_quests, 1):
                if quest.difficulty:
                    print(
                        f"{i}. {quest.title} (Difficulty: {'★' * quest.difficulty}{'☆' * (10 - quest.difficulty)})")
                else:
                    print(f"{i}. {quest.title}")

            print("\nAccept a quest (0 to return):")
            choice = get_valid_input(
                "Enter quest number: ", range(0, len(available_quests) + 1))

            if choice > 0:
                selected_quest = available_quests[choice - 1]
                self.player.active_quests.append(selected_quest.id)
                print(
                    f"\n{CLR_SUCCESS}Quest accepted: {selected_quest.title}{CLR_RESET}")
                selected_quest.display()

        input("\nPress Enter to continue...")

    def manage_services(self) -> None:
        """Deploy or manage cloud services."""
        while True:
            clear_screen()
            print(f"\n{CLR_SECTION}[SERVICE MANAGEMENT]{CLR_RESET}")
            print("1. Deploy a new service")
            print("2. Manage deployed services")
            print("3. View service analytics")
            print("4. Return to main menu")

            choice = get_valid_input(
                "\nEnter your choice (1-4): ", range(1, 5))

            if choice == 1:
                self.deploy_service()
            elif choice == 2:
                self.manage_deployed_services()
            elif choice == 3:
                self.view_service_analytics()
            elif choice == 4:
                break

    def deploy_service(self) -> None:
        """Deploy a service to the cloud."""
        print(f"\n{CLR_SECTION}[DEPLOY SERVICE]{CLR_RESET}")

        if not self.player.inventory.services:
            print("You don't have any services to deploy.")
            input("\nPress Enter to continue...")
            return

        print("Choose a service to deploy:")
        for i, service in enumerate(self.player.inventory.services, 1):
            print(f"{i}. {service.name} (Cost: {service.deploy_cost} credits)")
        print(f"{len(self.player.inventory.services) + 1}. Cancel")

        choice = get_valid_input("\nEnter your choice: ", range(
            1, len(self.player.inventory.services) + 2))

        if choice == len(self.player.inventory.services) + 1:
            print("Deployment canceled.")
            return

        selected_service = self.player.inventory.services[choice - 1]

        # Check if player has enough credits
        if self.player.cloud_credits < selected_service.deploy_cost:
            print(
                f"\n{CLR_ERROR}You don't have enough Cloud Credits to deploy this service.{CLR_RESET}")
            input("\nPress Enter to continue...")
            return

        # Check dependencies
        for dependency in selected_service.dependencies:
            has_dependency = False
            for deployed in self.player.inventory.deployed_services:
                if deployed.name == dependency and deployed.is_deployed:
                    has_dependency = True
                    break

            if not has_dependency:
                print(
                    f"\n{CLR_ERROR}You need to deploy {dependency} before deploying this service.{CLR_RESET}")
                input("\nPress Enter to continue...")
                return

        # Check region availability
        current_region = self.player.current_location.region
        if current_region not in selected_service.region_availability and "global" not in selected_service.region_availability:
            print(
                f"\n{CLR_ERROR}This service is not available in the {current_region} region.{CLR_RESET}")
            input("\nPress Enter to continue...")
            return

        # Deploy the service
        self.player.cloud_credits -= selected_service.deploy_cost
        deployed_service = copy.deepcopy(selected_service)
        deployed_service.is_deployed = True
        deployed_service.deployment_region = current_region
        deployed_service.instance_id = f"{deployed_service.name[:3]}-{str(uuid.uuid4())[:8]}"

        # neon_shadow/game.py (continued)

        self.player.inventory.deployed_services.append(deployed_service)
        self.player.inventory.services.remove(selected_service)

        display_loading_bar("Deploying service...", 1.5)
        display_notification(
            f"Successfully deployed {deployed_service.name} ({deployed_service.instance_id}) in {current_region}!", "success")

        # Deployment takes time
        self.current_day += 1
        input("\nPress Enter to continue...")

    def manage_deployed_services(self) -> None:
        """Manage already deployed services."""
        if not self.player.inventory.deployed_services:
            print("\nYou don't have any deployed services to manage.")
            input("\nPress Enter to continue...")
            return

        while True:
            print(f"\n{CLR_SECTION}[MANAGE DEPLOYED SERVICES]{CLR_RESET}")

            # Display deployed services
            for i, service in enumerate(self.player.inventory.deployed_services, 1):
                status = f"{CLR_SUCCESS}ONLINE{CLR_RESET}" if service.is_deployed else f"{CLR_ERROR}OFFLINE{CLR_RESET}"
                print(f"{i}. {service.name} ({service.instance_id}) - {status}")
                print(f"   Region: {service.deployment_region}")
                print(
                    f"   Health: {service.health}% | Security: {service.security_level}/10 | Performance: {service.performance}/10")

            print(f"{len(self.player.inventory.deployed_services) + 1}. Return")

            choice = get_valid_input("\nSelect a service to manage (or return): ",
                                     range(1, len(self.player.inventory.deployed_services) + 2))

            if choice == len(self.player.inventory.deployed_services) + 1:
                break

            selected_service = self.player.inventory.deployed_services[choice - 1]
            self.service_action_menu(selected_service)

    def service_action_menu(self, service: CloudService) -> None:
        """Show actions for a specific service."""
        while True:
            print(
                f"\n{CLR_SECTION}[MANAGE {service.name} ({service.instance_id})]{CLR_RESET}")
            print(f"Status: {'ONLINE' if service.is_deployed else 'OFFLINE'}")
            print(f"Health: {service.health}%")
            print(f"Security Level: {service.security_level}/10")
            print(f"Performance: {service.performance}/10")
            print(f"Region: {service.deployment_region}")
            print(f"Uptime: {service.uptime_days} days")
            print(f"Revenue: {service.calculate_revenue():.2f} credits/hour")

            if service.status_effects:
                print("\nActive Status Effects:")
                for effect in service.status_effects:
                    print(
                        f"• {effect['name']} ({effect['duration']} turns remaining)")

            print("\nActions:")
            if service.is_deployed:
                print("1. Repair Service (+Health)")
                print("2. Enhance Security (+Security)")
                print("3. Optimize Performance (+Performance)")
                print("4. Undeploy Service")
            else:
                print("1. Redeploy Service")

            print("5. Return")

            # Limit options based on service status
            max_option = 5 if service.is_deployed else 2

            choice = get_valid_input(
                f"\nEnter your choice (1-{max_option}): ", range(1, max_option + 1))

            if service.is_deployed:
                if choice == 1:
                    # Repair service
                    # Cost scales with damage
                    repair_cost = 10 * (100 - service.health) // 10
                    repair_amount = 30

                    print(
                        f"\nRepairing will restore up to {repair_amount}% health.")
                    print(f"Cost: {repair_cost} credits")

                    if confirm_action(f"Repair {service.name} for {repair_cost} credits?"):
                        if self.player.cloud_credits >= repair_cost:
                            self.player.cloud_credits -= repair_cost
                            actual_repair = service.repair(repair_amount)
                            display_notification(
                                f"Repaired {service.name} by {actual_repair}% for {repair_cost} credits", "success")
                        else:
                            display_notification(
                                "Not enough credits for repair!", "error")

                elif choice == 2:
                    # Enhance security
                    security_cost = 15 * (10 - service.security_level)
                    security_amount = 2

                    print(
                        f"\nEnhancing security will increase security level by {security_amount}.")
                    print(f"Cost: {security_cost} credits")

                    if confirm_action(f"Enhance {service.name} security for {security_cost} credits?"):
                        if self.player.cloud_credits >= security_cost:
                            self.player.cloud_credits -= security_cost
                            actual_increase = service.enhance_security(
                                security_amount)
                            display_notification(
                                f"Enhanced {service.name} security by {actual_increase} for {security_cost} credits", "success")
                        else:
                            display_notification(
                                "Not enough credits for security enhancement!", "error")

                elif choice == 3:
                    # Optimize performance
                    perf_cost = 20 * (10 - service.performance)
                    perf_amount = 2

                    print(
                        f"\nOptimizing will increase performance by {perf_amount}.")
                    print(f"Cost: {perf_cost} credits")

                    if confirm_action(f"Optimize {service.name} performance for {perf_cost} credits?"):
                        if self.player.cloud_credits >= perf_cost:
                            self.player.cloud_credits -= perf_cost
                            actual_increase = service.optimize_performance(
                                perf_amount)
                            display_notification(
                                f"Optimized {service.name} performance by {actual_increase} for {perf_cost} credits", "success")
                        else:
                            display_notification(
                                "Not enough credits for performance optimization!", "error")

                elif choice == 4:
                    # Undeploy service
                    if confirm_action(f"Are you sure you want to undeploy {service.name}?"):
                        service.undeploy()
                        display_notification(
                            f"Service {service.name} has been undeployed.", "warning")

            elif choice == 1:
                # Redeploy service
                redeploy_cost = service.deploy_cost // 2  # Half the original cost

                print(f"\nRedeploying will cost {redeploy_cost} credits.")

                if confirm_action(f"Redeploy {service.name} for {redeploy_cost} credits?"):
                    if self.player.cloud_credits >= redeploy_cost:
                        self.player.cloud_credits -= redeploy_cost
                        service.is_deployed = True
                        service.health = 100  # Reset health on redeploy
                        display_notification(
                            f"Successfully redeployed {service.name}!", "success")
                    else:
                        display_notification(
                            "Not enough credits for redeployment!", "error")

            elif choice == 5 or (not service.is_deployed and choice == 2):
                break

    def view_service_analytics(self) -> None:
        """View analytics for deployed services."""
        if not self.player.inventory.deployed_services:
            print("\nYou don't have any deployed services to analyze.")
            input("\nPress Enter to continue...")
            return

        print(f"\n{CLR_SECTION}[SERVICE ANALYTICS]{CLR_RESET}")

        # Calculate total revenue, costs
        total_hourly_revenue = 0
        total_hourly_cost = 0
        total_health = 0
        total_security = 0
        total_performance = 0
        active_services = 0

        services_by_region = defaultdict(int)
        services_by_type = defaultdict(int)

        for service in self.player.inventory.deployed_services:
            if service.is_deployed:
                active_services += 1
                hourly_revenue = service.calculate_revenue()
                hourly_cost = service.cost_per_hour

                total_hourly_revenue += hourly_revenue
                total_hourly_cost += hourly_cost
                total_health += service.health
                total_security += service.security_level
                total_performance += service.performance

                services_by_region[service.deployment_region] += 1
                services_by_type[service.service_type] += 1

        # Display summary statistics
        print(f"\n{CLR_CYAN}Summary Statistics:{CLR_RESET}")
        print(
            f"Total Deployed Services: {len(self.player.inventory.deployed_services)}")
        print(f"Active Services: {active_services}")

        if active_services > 0:
            # Calculate daily values (24 hours)
            daily_revenue = total_hourly_revenue * 24
            daily_cost = total_hourly_cost * 24
            daily_profit = daily_revenue - daily_cost

            print(f"\n{CLR_CREDITS}Financial Analytics:{CLR_RESET}")
            print(f"Total Hourly Revenue: {total_hourly_revenue:.2f} credits")
            print(f"Total Hourly Cost: {total_hourly_cost:.2f} credits")
            print(
                f"Hourly Profit: {total_hourly_revenue - total_hourly_cost:.2f} credits")
            print(f"Estimated Daily Profit: {daily_profit:.2f} credits")

            # Calculate averages
            avg_health = total_health / active_services
            avg_security = total_security / active_services
            avg_performance = total_performance / active_services

            print(f"\n{CLR_CYAN}Performance Metrics:{CLR_RESET}")
            print(f"Average Health: {avg_health:.1f}%")
            print(f"Average Security Level: {avg_security:.1f}/10")
            print(f"Average Performance: {avg_performance:.1f}/10")

            # Distribution by region
            print(f"\n{CLR_CYAN}Regional Distribution:{CLR_RESET}")
            for region, count in services_by_region.items():
                print(
                    f"{region}: {count} services ({count/active_services*100:.1f}%)")

            # Distribution by service type
            print(f"\n{CLR_CYAN}Service Type Distribution:{CLR_RESET}")
            for svc_type, count in services_by_type.items():
                print(
                    f"{svc_type}: {count} services ({count/active_services*100:.1f}%)")

            # Incident history analysis if any services have history
            incidents = []
            for service in self.player.inventory.deployed_services:
                if service.incident_history:
                    for incident in service.incident_history:
                        incidents.append({
                            "service": service.name,
                            "instance": service.instance_id,
                            "type": incident["type"],
                            "amount": incident["amount"],
                            "day": incident["day"]
                        })

            if incidents:
                print(
                    f"\n{CLR_HAZARD}Recent Incidents ({min(5, len(incidents))} of {len(incidents)}):{CLR_RESET}")
                # Sort by most recent
                incidents.sort(key=lambda x: x["day"], reverse=True)

                for incident in incidents[:5]:  # Show 5 most recent
                    print(f"Day {incident['day']}: {incident['service']} ({incident['instance'][:6]}) - " +
                          f"{incident['type'].capitalize()} of {incident['amount']}")

            # Most profitable service
            if active_services > 0:
                most_profitable = max(
                    [s for s in self.player.inventory.deployed_services if s.is_deployed],
                    key=lambda s: s.calculate_revenue() - s.cost_per_hour
                )

                profit = most_profitable.calculate_revenue() - most_profitable.cost_per_hour
                print(f"\n{CLR_BONUS}Most Profitable Service:{CLR_RESET}")
                print(
                    f"{most_profitable.name} ({most_profitable.instance_id[:6]}): {profit:.2f} credits/hour")

        input("\nPress Enter to continue...")

    def use_artifact(self) -> None:
        """Use an artifact from the inventory."""
        if not self.player.inventory.artifacts:
            print("\nYou don't have any artifacts to use.")
            input("\nPress Enter to continue...")
            return

        print(f"\n{CLR_SECTION}[USE ARTIFACT]{CLR_RESET}")

        # Show artifacts with their status
        available_artifacts = []
        for i, artifact in enumerate(self.player.inventory.artifacts, 1):
            cooldown_status = ""
            if artifact.cooldown > 0:
                cooldown_status = f" [COOLDOWN: {artifact.cooldown}]"
                print(
                    f"{i}. {artifact.name} - {artifact.description}{cooldown_status} (UNAVAILABLE)")
            else:
                available_artifacts.append(artifact)
                print(f"{i}. {artifact.name} - {artifact.description}")

        if not available_artifacts:
            print("\nAll your artifacts are on cooldown.")
            input("\nPress Enter to continue...")
            return

        print(f"{len(self.player.inventory.artifacts) + 1}. Cancel")

        choice = get_valid_input("\nSelect an artifact to use: ",
                                 range(1, len(self.player.inventory.artifacts) + 2))

        if choice == len(self.player.inventory.artifacts) + 1:
            print("Cancelled.")
            return

        selected_artifact = self.player.inventory.artifacts[choice - 1]

        if selected_artifact.cooldown > 0:
            print(
                f"\n{CLR_ERROR}This artifact is on cooldown for {selected_artifact.cooldown} more turns.{CLR_RESET}")
            input("\nPress Enter to continue...")
            return

        # Use the artifact
        print(f"\nUsing {selected_artifact.name}...")

        # Different effects based on artifact type
        if selected_artifact.artifact_type == "Scanner":
            self.use_scanner_artifact(selected_artifact)
        elif selected_artifact.artifact_type == "Security":
            self.use_security_artifact(selected_artifact)
        elif selected_artifact.artifact_type == "Network":
            self.use_network_artifact(selected_artifact)
        elif selected_artifact.artifact_type == "Recovery":
            self.use_recovery_artifact(selected_artifact)
        elif selected_artifact.artifact_type == "Database":
            self.use_database_artifact(selected_artifact)
        else:
            # Generic artifact use
            display_loading_bar(f"Activating {selected_artifact.name}", 1.5)

            # Generic benefits scaled by artifact power
            benefit = selected_artifact.power + selected_artifact.upgrade_level

            # Random effect based on artifact power
            effect_type = random.choice(["credits", "skill", "clue", "repair"])

            if effect_type == "credits":
                credits_gained = benefit * 10
                self.player.cloud_credits += credits_gained
                display_notification(
                    f"Generated {credits_gained} credits!", "success")
            elif effect_type == "skill":
                skill = random.choice(list(self.player.skills.keys()))
                self.player.increase_skill(skill, 1)
            elif effect_type == "clue":
                clue_id = f"artifact_clue_{random.randint(1000, 9999)}"
                self.player.add_clue(clue_id)
                print(
                    f"{CLR_CLUE}You discovered a new lead using the {selected_artifact.name}.{CLR_RESET}")
            elif effect_type == "repair":
                if self.player.inventory.deployed_services:
                    # Find service with lowest health
                    service_to_repair = min(
                        [s for s in self.player.inventory.deployed_services if s.is_deployed],
                        key=lambda s: s.health,
                        default=None
                    )
                    if service_to_repair:
                        repair_amount = benefit * 5
                        service_to_repair.repair(repair_amount)

        # Set cooldown
        selected_artifact.cooldown = 1 + (selected_artifact.power // 3)

        # Using an artifact advances time slightly
        self.current_day += 1
        input("\nPress Enter to continue...")

    def use_scanner_artifact(self, artifact: CloudArtifact) -> None:
        """Use a scanner-type artifact."""
        display_loading_bar(f"Scanning with {artifact.name}", 1.5)

        # Scanner artifacts are good for finding clues and security issues
        discovery_chance = 40 + (artifact.power * 5) + \
            (artifact.upgrade_level * 10)

        if random.randint(1, 100) <= discovery_chance:
            # Found something
            current_loc = self.player.current_location.name

            # Generate a meaningful clue
            clue_id = f"scan_clue_{current_loc}_{random.randint(1000, 9999)}"

            # Create descriptive clue based on location and artifact
            if "S3" in artifact.name:
                clue_text = f"Your scan revealed unauthorized access to S3 buckets in {current_loc}."
            elif "EC2" in artifact.name:
                clue_text = f"Your scan detected unusual processes running on EC2 instances in {current_loc}."
            elif "RDS" in artifact.name or "Aurora" in artifact.name:
                clue_text = f"Your scan found suspicious database queries originating from {current_loc}."
            elif "DynamoDB" in artifact.name:
                clue_text = f"Your scan identified abnormal access patterns to DynamoDB tables from {current_loc}."
            else:
                clue_text = f"Your scan uncovered evidence of suspicious activity in {current_loc}."

            self.player.add_clue(clue_id)
            print(f"\n{CLR_SUCCESS}Scan Complete!{CLR_RESET}")
            print(f"{CLR_CLUE}{clue_text}{CLR_RESET}")

            # Chance to find vulnerabilities in deployed services
            if self.player.inventory.deployed_services and random.randint(1, 100) <= 30:
                service = random.choice(
                    self.player.inventory.deployed_services)
                if service.is_deployed:
                    print(
                        f"\n{CLR_WARNING}The scan also detected a vulnerability in {service.name} ({service.instance_id}).{CLR_RESET}")
                    print(f"You should enhance the security of this service soon.")

                    # Add small security penalty if ignored
                    if service.security_level > 1:
                        service.security_level -= 1
                        service.add_status_effect({
                            "name": "Security Vulnerability",
                            "duration": 3,
                            "per_turn_effect": lambda svc: svc.apply_damage(2)
                        })
        else:
            print(f"\n{CLR_SUCCESS}Scan Complete!{CLR_RESET}")
            print("No anomalies detected during this scan.")

    def use_security_artifact(self, artifact: CloudArtifact) -> None:
        """Use a security-type artifact."""
        display_loading_bar(f"Activating {artifact.name}", 1.5)

        # Security artifacts enhance security and can prevent attacks
        security_bonus = artifact.power + artifact.upgrade_level

        if self.player.inventory.deployed_services:
            # Ask which service to enhance
            print("\nSelect a service to enhance security:")
            deployed_services = [
                s for s in self.player.inventory.deployed_services if s.is_deployed]

            if not deployed_services:
                print("No active services to enhance.")
                return

            for i, service in enumerate(deployed_services, 1):
                print(
                    f"{i}. {service.name} ({service.instance_id}) - Security: {service.security_level}/10")

            print(f"{len(deployed_services) + 1}. Cancel")

            choice = get_valid_input(
                "Select a service: ", range(1, len(deployed_services) + 2))

            if choice == len(deployed_services) + 1:
                print("Cancelled.")
                return

            selected_service = deployed_services[choice - 1]

            # Enhance security
            security_increase = min(
                10 - selected_service.security_level, security_bonus)
            selected_service.security_level += security_increase

            # Also repair some damage
            repair_amount = security_bonus * 3
            health_increase = min(100 - selected_service.health, repair_amount)
            selected_service.health += health_increase

            display_notification(
                f"Enhanced {selected_service.name} security by {security_increase} and repaired {health_increase}% health!",
                "success"
            )

            # Add protection status effect
            selected_service.add_status_effect({
                "name": "Enhanced Security",
                "duration": 3,
                "per_turn_effect": lambda svc: None  # No ongoing effect
            })
        else:
            # Apply to player if no services
            print(
                f"\n{CLR_SUCCESS}Security enhanced for your personal systems!{CLR_RESET}")

            # Temporary protection status effect for player
            self.player.add_status_effect({
                "name": "Security Shield",
                "duration": 3,
                "per_turn_effect": lambda player: None  # Just protection
            })

            # Maybe heal some damage
            if self.player.health < self.player.max_health:
                heal_amount = security_bonus * 3
                self.player.heal(heal_amount)

    def use_network_artifact(self, artifact: CloudArtifact) -> None:
        """Use a network-type artifact."""
        display_loading_bar(f"Initializing {artifact.name}", 1.5)

        # Network artifacts are good for monitoring traffic, finding connections
        network_power = artifact.power + artifact.upgrade_level

        # Chance to discover new connections or locations
        if len(self.discovered_locations) < len(self.locations):
            undiscovered = [loc for loc in self.locations.keys(
            ) if loc not in self.discovered_locations]

            if undiscovered and random.randint(1, 100) <= 30 + (network_power * 5):
                discovered_loc = random.choice(undiscovered)
                self.discovered_locations.add(discovered_loc)

                # Add connection if reasonable
                if random.randint(1, 100) <= 50:
                    current_loc_name = self.player.current_location.name
                    if discovered_loc not in self.player.current_location.connections:
                        self.player.current_location.add_connection(
                            discovered_loc)
                        self.locations[discovered_loc].add_connection(
                            current_loc_name)
                        display_notification(
                            f"Discovered new route to {discovered_loc}!", "success")
                else:
                    display_notification(
                        f"Detected presence of {discovered_loc} in network traffic!", "info")

        # Network analysis
        print(f"\n{CLR_SUCCESS}Network analysis complete!{CLR_RESET}")

        # Show some network statistics
        most_connected = max(self.locations.items(),
                             key=lambda x: len(x[1].connections))
        print(
            f"Most connected node: {most_connected[0]} ({len(most_connected[1].connections)} connections)")

        # Bandwidth boost
        bandwidth_boost = network_power * 5
        old_bandwidth = self.player.bandwidth
        self.player.bandwidth += bandwidth_boost
        print(
            f"Bandwidth optimized: {old_bandwidth} → {self.player.bandwidth} (+{bandwidth_boost})")

        # Chance to find suspicious traffic
        if random.randint(1, 100) <= 20 + (network_power * 3):
            print(
                f"\n{CLR_WARNING}Alert: Suspicious traffic pattern detected!{CLR_RESET}")
            suspicious_location = random.choice(list(self.locations.keys()))
            print(f"Origin appears to be {suspicious_location}.")

            # Add clue
            clue_id = f"network_clue_{random.randint(1000, 9999)}"
            self.player.add_clue(clue_id)

            # Chance to find Shadow Admin trace
            if random.randint(1, 100) <= 10:
                print(
                    f"\n{CLR_SHADOW_ADMIN}You detected a trace signature matching the Shadow Admin!{CLR_RESET}")
                self.player.update_faction_reputation("ShadowNetwork", 2)

    def use_recovery_artifact(self, artifact: CloudArtifact) -> None:
        """Use a recovery-type artifact."""
        display_loading_bar(f"Initializing {artifact.name}", 1.5)

        recovery_power = artifact.power + artifact.upgrade_level

        # Recovery artifacts restore health to services or player
        if self.player.inventory.deployed_services:
            # Choose between healing services or player
            targets = ["services", "player"]
            weights = [0.7, 0.3]  # 70% chance for services, 30% for player
            target = random.choices(targets, weights=weights)[0]

            if target == "services":
                # Find all damaged services
                damaged_services = [s for s in self.player.inventory.deployed_services
                                    if s.is_deployed and s.health < 100]

                if damaged_services:
                    # Heal all damaged services partially
                    heal_amount = recovery_power * 10

                    for service in damaged_services:
                        actual_heal = service.repair(heal_amount)
                        print(
                            f"{CLR_SUCCESS}Repaired {service.name} by {actual_heal}%{CLR_RESET}")

                    display_notification(
                        f"Recovery complete! Services restored.", "success")
                else:
                    print(
                        f"{CLR_SUCCESS}No damaged services found. All systems nominal.{CLR_RESET}")
                    # Heal player instead
                    heal_amount = recovery_power * 5
                    self.player.heal(heal_amount)
                    display_notification(
                        f"Redirected recovery to personal systems. +{heal_amount} health", "info")
            else:
                # Heal player
                heal_amount = recovery_power * 15
                actual_heal = self.player.heal(heal_amount)
                display_notification(
                    f"Recovery complete! +{actual_heal} health", "success")
        else:
            # No services, heal player
            heal_amount = recovery_power * 20
            actual_heal = self.player.heal(heal_amount)
            display_notification(
                f"Recovery complete! +{actual_heal} health", "success")

            # Also boost energy
            energy_boost = recovery_power * 10
            actual_boost = self.player.restore_energy(energy_boost)
            if actual_boost > 0:
                display_notification(
                    f"Energy systems optimized! +{actual_boost} energy", "success")

    def use_database_artifact(self, artifact: CloudArtifact) -> None:
        """Use a database-type artifact."""
        display_loading_bar(f"Querying with {artifact.name}", 1.5)

        db_power = artifact.power + artifact.upgrade_level

        # Database artifacts are good for analysis, gaining knowledge, finding clues
        intelligence_gain = db_power * 5
        credits_gain = db_power * 15

        # Generate some random insights
        print(f"\n{CLR_CYAN}Database analysis complete!{CLR_RESET}")

        insights = [
            f"Analyzed {intelligence_gain} records for patterns.",
            f"Optimized database queries saving an estimated {credits_gain} credits.",
            f"Knowledge extraction complete."
        ]

        for insight in random.sample(insights, k=min(2, len(insights))):
            print(insight)

        # Award credits from optimization
        self.player.cloud_credits += credits_gain
        print(
            f"{CLR_CREDITS}+{credits_gain} credits from query optimization{CLR_RESET}")

        # Chance for skill increase
        if random.randint(1, 100) <= 20 + (db_power * 5):
            skill = random.choice(["database", "investigation", "cloud"])
            self.player.increase_skill(skill, 1)

        # Chance to find important information
        if random.randint(1, 100) <= 30 + (db_power * 3):
            clue_id = f"db_clue_{random.randint(1000, 9999)}"
            self.player.add_clue(clue_id)
            print(
                f"\n{CLR_CLUE}Your database analysis uncovered a hidden connection!{CLR_RESET}")

    def rest(self) -> None:
        """Rest to recover energy and health."""
        print(f"\n{CLR_SECTION}[REST]{CLR_RESET}")
        print("You decide to take some time to rest and recover.")

        # Check if player is in a safe location
        current_loc = self.player.current_location
        is_safe = current_loc.difficulty <= 3

        if is_safe:
            print(f"{current_loc.name} is a relatively safe place to rest.")
            health_recovery = 20
            energy_recovery = 70
        else:
            print(f"{current_loc.name} is not the safest place to rest.")
            print("You'll need to stay alert, limiting your recovery.")
            health_recovery = 10
            energy_recovery = 40

        # Check for weather effects
        if current_loc.name in self.weather_conditions:
            weather = self.weather_conditions[current_loc.name]["current"]
            if "CPU Heatwave" in weather["name"]:
                energy_recovery = int(energy_recovery * 0.7)
                print(
                    f"{CLR_WARNING}The CPU Heatwave makes rest less effective.{CLR_RESET}")
            elif "Clear Signals" in weather["name"]:
                health_recovery = int(health_recovery * 1.2)
                energy_recovery = int(energy_recovery * 1.2)
                print(
                    f"{CLR_SUCCESS}The Clear Signals help you rest more effectively.{CLR_RESET}")

        # Apply recovery
        health_gained = self.player.heal(health_recovery)
        energy_gained = self.player.restore_energy(energy_recovery)

        print_slow("Resting...", delay=0.1)
        time.sleep(1)

        # Display results
        print(f"\n{CLR_SUCCESS}You've rested and recovered:{CLR_RESET}")
        print(f"Health: +{health_gained}")
        print(f"Energy: +{energy_gained}")

        # Check for random events during rest
        event_chance = 20 if is_safe else 40

        if random.randint(1, 100) <= event_chance:
            print(
                f"\n{CLR_WARNING}However, your rest was interrupted...{CLR_RESET}")
            time.sleep(1)

            # Trigger a random event
            self.trigger_random_event()

        # Resting advances time
        self.current_day += 1

        input("\nPress Enter to continue...")

    def trigger_random_event(self) -> None:
        """Trigger a random event during rest."""
        event_types = ["discovery", "encounter", "dream"]
        event_type = random.choice(event_types)

        if event_type == "discovery":
            print(f"While resting, you notice something you hadn't seen before.")

            discoveries = [
                {"text": "A hidden terminal that seems to have been recently used.",
                 "reward": "clue"},
                {"text": "A discarded data chip with intact information.",
                 "reward": "credits"},
                {"text": "A concealed cache of emergency supplies.",
                 "reward": "health"}
            ]

            discovery = random.choice(discoveries)
            print(discovery["text"])

            if discovery["reward"] == "clue":
                clue_id = f"rest_clue_{random.randint(1000, 9999)}"
                self.player.add_clue(clue_id)
            elif discovery["reward"] == "credits":
                credits = random.randint(10, 30)
                self.player.cloud_credits += credits
                print(f"{CLR_CREDITS}You found {credits} cloud credits!{CLR_RESET}")
            elif discovery["reward"] == "health":
                health = random.randint(10, 25)
                actual_heal = self.player.heal(health)
                print(
                    f"{CLR_SUCCESS}You found medical supplies! +{actual_heal} health{CLR_RESET}")

        elif event_type == "encounter":
            encounters = [
                {"text": "You're awakened by a passing security patrol.",
                 "effect": "reputation"},
                {"text": "A wandering data miner stops to chat.",
                 "effect": "skill"},
                {"text": "You spot someone suspicious watching you from the shadows.",
                 "effect": "shadow"}
            ]

            encounter = random.choice(encounters)
            print(encounter["text"])

            if encounter["effect"] == "reputation":
                self.player.update_faction_reputation("CorpSec", 2)
            elif encounter["effect"] == "skill":
                skill = random.choice(list(self.player.skills.keys()))
                self.player.increase_skill(skill, 1)
            elif encounter["effect"] == "shadow":
                self.player.update_faction_reputation("ShadowNetwork", 1)
                print(
                    f"{CLR_SHADOW_ADMIN}They disappear before you can approach them.{CLR_RESET}")

        elif event_type == "dream":
            print("While resting, you have a vivid dream...")

            dreams = [
                "You dream of vast data centers, humming with activity. In the dream, you can see the flow of information like rivers of light.",
                "You dream you're being pursued through a digital landscape by a shadowy figure who always stays just out of sight.",
                "You dream of standing atop a mountain of servers, overlooking the entire cloud infrastructure."
            ]

            dream_text = random.choice(dreams)
            print_slow(dream_text, color=CLR_BRIGHT + CLR_CYAN)

            # Dreams can provide insights or small bonuses
            print(
                f"\n{CLR_SUCCESS}The dream leaves you with new insights.{CLR_RESET}")

            # Small random bonus
            effect = random.choice(["energy", "skill_temp", "shadow_insight"])

            if effect == "energy":
                energy = random.randint(10, 30)
                self.player.restore_energy(energy)
                print(f"You feel more energized. +{energy} energy")
            elif effect == "skill_temp":
                skill = random.choice(list(self.player.skills.keys()))
                boost = {
                    "skill": skill,
                    "amount": 1,
                    "remaining_days": 2
                }
                self.player.temp_skill_boosts.append(boost)
                print(
                    f"You have a temporary insight into {skill}. +1 for 2 days")
            elif effect == "shadow_insight":
                print(
                    f"{CLR_SHADOW_ADMIN}You feel you've glimpsed something important about the Shadow Admin...{CLR_RESET}")
                clue_id = f"shadow_dream_{random.randint(1000, 9999)}"
                self.player.add_clue(clue_id)

    def interact_with_vendors(self) -> None:
        """Interact with vendors at the current location."""
        current_loc = self.player.current_location

        if not current_loc.vendors:
            print(f"\n{CLR_ERROR}There are no vendors at this location.{CLR_RESET}")
            input("\nPress Enter to continue...")
            return

        print(f"\n{CLR_SECTION}[VENDORS AT {current_loc.name}]{CLR_RESET}")

        # List available vendors
        available_vendors = []
        for i, vendor in enumerate(current_loc.vendors, 1):
            # Check reputation requirements
            can_access = True
            if "reputation_required" in vendor:
                for faction, level in vendor["reputation_required"].items():
                    if faction in self.player.faction_reputation:
                        if self.player.faction_reputation[faction] < level:
                            can_access = False
                            print(f"{i}. {vendor['name']} - {vendor['description']} " +
                                  f"({CLR_ERROR}Requires {faction} reputation {level}{CLR_RESET})")
                            break

            if can_access:
                available_vendors.append(vendor)
                print(f"{i}. {vendor['name']} - {vendor['description']}")

        if not available_vendors:
            print(
                f"\n{CLR_ERROR}You don't have sufficient reputation to access any vendors here.{CLR_RESET}")
            input("\nPress Enter to continue...")
            return

        print(f"{len(current_loc.vendors) + 1}. Cancel")

        choice = get_valid_input("Select a vendor: ",
                                 range(1, len(current_loc.vendors) + 2))

        if choice == len(current_loc.vendors) + 1:
            return

        # Find the selected vendor
        selected_vendor = None
        for i, vendor in enumerate(current_loc.vendors, 1):
            if i == choice:
                selected_vendor = vendor
                break

        if not selected_vendor:
            print(f"{CLR_ERROR}Error selecting vendor.{CLR_RESET}")
            return

        # Check if player can access this vendor
        can_access = True
        if "reputation_required" in selected_vendor:
            for faction, level in selected_vendor["reputation_required"].items():
                if faction in self.player.faction_reputation:
                    if self.player.faction_reputation[faction] < level:
                        can_access = False
                        print(
                            f"{CLR_ERROR}You need {faction} reputation of at least {level} to access this vendor.{CLR_RESET}")
                        input("\nPress Enter to continue...")
                        return

        # Show vendor menu
        self.vendor_menu(selected_vendor)

    def vendor_menu(self, vendor) -> None:
        """Display the vendor's menu."""
        while True:
            print(f"\n{CLR_SECTION}[{vendor['name']}]{CLR_RESET}")
            print(f"Your Credits: {self.player.cloud_credits}")
            print("\nWhat would you like to do?")
            print("1. Buy Artifacts")
            print("2. Buy Services")
            print("3. Buy Consumables")
            print("4. Sell Items")
            print("5. Return")

            options = []
            if "inventory" in vendor and "artifacts" in vendor["inventory"] and vendor["inventory"]["artifacts"]:
                options.append(1)
            if "inventory" in vendor and "services" in vendor["inventory"] and vendor["inventory"]["services"]:
                options.append(2)
            if "inventory" in vendor and "consumables" in vendor["inventory"] and vendor["inventory"]["consumables"]:
                options.append(3)
            if self.player.inventory.artifacts or self.player.inventory.services:
                options.append(4)
            options.append(5)

            choice = get_valid_input("Enter your choice: ", options)

            if choice == 1 and 1 in options:
                self.buy_artifacts(vendor)
            elif choice == 2 and 2 in options:
                self.buy_services(vendor)
            elif choice == 3 and 3 in options:
                self.buy_consumables(vendor)
            elif choice == 4 and 4 in options:
                self.sell_items(vendor)
            elif choice == 5:
                break

    def buy_artifacts(self, vendor) -> None:
        """Buy artifacts from a vendor."""
        if "inventory" not in vendor or "artifacts" not in vendor["inventory"] or not vendor["inventory"]["artifacts"]:
            print(f"{CLR_ERROR}This vendor doesn't sell artifacts.{CLR_RESET}")
            return

        print(f"\n{CLR_SECTION}[BUY ARTIFACTS]{CLR_RESET}")
        print(f"Your Credits: {self.player.cloud_credits}")

        available_artifacts = []
        for artifact_name in vendor["inventory"]["artifacts"]:
            if artifact_name in self.artifacts:
                artifact_data = self.artifacts[artifact_name]
                cost = artifact_data["cost"]
                available_artifacts.append(
                    (artifact_name, artifact_data, cost))

        if not available_artifacts:
            print(f"{CLR_ERROR}No artifacts available.{CLR_RESET}")
            return

        # Display available artifacts
        for i, (name, data, cost) in enumerate(available_artifacts, 1):
            print(
                f"{i}. {name} - {data['description']} (Cost: {cost} credits)")

        print(f"{len(available_artifacts) + 1}. Cancel")

        choice = get_valid_input("Select an artifact to buy: ",
                                 range(1, len(available_artifacts) + 2))

        if choice == len(available_artifacts) + 1:
            return

        # Get selected artifact
        selected_name, selected_data, cost = available_artifacts[choice - 1]

        # Check if player has enough credits
        if self.player.cloud_credits < cost:
            print(
                f"{CLR_ERROR}You don't have enough credits to buy this artifact.{CLR_RESET}")
            return

        # Check if player has room in inventory
        if len(self.player.inventory.artifacts) >= self.player.inventory.max_artifacts:
            print(f"{CLR_ERROR}Your artifact inventory is full.{CLR_RESET}")
            return

        # Purchase the artifact
        self.player.cloud_credits -= cost

        new_artifact = CloudArtifact(
            selected_data["name"],
            selected_data["description"],
            selected_data["artifact_type"],
            selected_data["aws_service"],
            selected_data["cost"],
            selected_data["power"]
        )

        self.player.add_artifact(new_artifact)
        display_notification(
            f"Purchased {selected_name} for {cost} credits!", "success")

    def buy_services(self, vendor) -> None:
        """Buy services from a vendor."""
        if "inventory" not in vendor or "services" not in vendor["inventory"] or not vendor["inventory"]["services"]:
            print(f"{CLR_ERROR}This vendor doesn't sell services.{CLR_RESET}")
            return

        print(f"\n{CLR_SECTION}[BUY SERVICES]{CLR_RESET}")
        print(f"Your Credits: {self.player.cloud_credits}")

        available_services = []
        for service_name in vendor["inventory"]["services"]:
            if service_name in self.services:
                service_data = self.services[service_name]
                # Buying blueprint costs more than deployment
                cost = service_data["deploy_cost"] * 2
                available_services.append((service_name, service_data, cost))

        if not available_services:
            print(f"{CLR_ERROR}No services available.{CLR_RESET}")
            return

        # Display available services
        for i, (name, data, cost) in enumerate(available_services, 1):
            print(
                f"{i}. {name} - {data['description']} (Cost: {cost} credits)")

        print(f"{len(available_services) + 1}. Cancel")

        choice = get_valid_input("Select a service to buy: ",
                                 range(1, len(available_services) + 2))

        if choice == len(available_services) + 1:
            return

        # Get selected service
        selected_name, selected_data, cost = available_services[choice - 1]

        # Check if player has enough credits
        if self.player.cloud_credits < cost:
            print(
                f"{CLR_ERROR}You don't have enough credits to buy this service.{CLR_RESET}")
            return

        # Check if player has room in inventory
        if len(self.player.inventory.services) >= self.player.inventory.max_services:
            print(f"{CLR_ERROR}Your service inventory is full.{CLR_RESET}")
            return

        # Purchase the service
        self.player.cloud_credits -= cost

        new_service = CloudService(
            selected_data["name"],
            selected_data["description"],
            selected_data["service_type"],
            selected_data["cost_per_hour"],
            selected_data["deploy_cost"],
            selected_data["region_availability"],
            selected_data["dependencies"]
        )

        self.player.add_service(new_service)
        display_notification(
            f"Purchased {selected_name} for {cost} credits!", "success")

    def buy_consumables(self, vendor) -> None:
        """Buy consumables from a vendor."""
        if "inventory" not in vendor or "consumables" not in vendor["inventory"] or not vendor["inventory"]["consumables"]:
            print(f"{CLR_ERROR}This vendor doesn't sell consumables.{CLR_RESET}")
            return

        print(f"\n{CLR_SECTION}[BUY CONSUMABLES]{CLR_RESET}")
        print(f"Your Credits: {self.player.cloud_credits}")

        consumables = []
        for name, data in vendor["inventory"]["consumables"].items():
            consumables.append((name, data))

        # Display available consumables
        for i, (name, data) in enumerate(consumables, 1):
            print(
                f"{i}. {name} - {data['description']} (Cost: {data['price']} credits)")

        print(f"{len(consumables) + 1}. Cancel")

        choice = get_valid_input("Select a consumable to buy: ",
                                 range(1, len(consumables) + 2))

        if choice == len(consumables) + 1:
            return

        # Get selected consumable
        selected_name, selected_data = consumables[choice - 1]

        # Ask for quantity
        quantity = get_valid_input(
            "How many would you like to buy? ", range(1, 11))

        total_cost = selected_data['price'] * quantity

        # Check if player has enough credits
        if self.player.cloud_credits < total_cost:
            print(
                f"{CLR_ERROR}You don't have enough credits to buy {quantity} {selected_name}.{CLR_RESET}")
            return

        # Purchase the consumables
        self.player.cloud_credits -= total_cost
        self.player.inventory.add_consumable(selected_name, quantity)

        display_notification(
            f"Purchased {quantity}x {selected_name} for {total_cost} credits!",
            "success"
        )

    def sell_items(self, vendor) -> None:
        """Sell items to a vendor."""
        print(f"\n{CLR_SECTION}[SELL ITEMS]{CLR_RESET}")
        print("What would you like to sell?")
        print("1. Artifacts")
        print("2. Services")
        print("3. Cancel")

        choice = get_valid_input("Enter your choice: ", range(1, 4))

        if choice == 1:
            self.sell_artifacts(vendor)
        elif choice == 2:
            self.sell_services(vendor)
        elif choice == 3:
            return

    def sell_artifacts(self, vendor) -> None:
        """Sell artifacts to a vendor."""
        if not self.player.inventory.artifacts:
            print(f"{CLR_ERROR}You don't have any artifacts to sell.{CLR_RESET}")
            return

        print(f"\n{CLR_SECTION}[SELL ARTIFACTS]{CLR_RESET}")

        # Display artifacts
        for i, artifact in enumerate(self.player.inventory.artifacts, 1):
            # Selling price is half the original cost
            sell_price = artifact.cost // 2
            print(
                f"{i}. {artifact.name} - {artifact.description} (Sell price: {sell_price} credits)")

        print(f"{len(self.player.inventory.artifacts) + 1}. Cancel")

        choice = get_valid_input("Select an artifact to sell: ",
                                 range(1, len(self.player.inventory.artifacts) + 2))

        if choice == len(self.player.inventory.artifacts) + 1:
            return

        # Get selected artifact
        selected_artifact = self.player.inventory.artifacts[choice - 1]
        sell_price = selected_artifact.cost // 2

        # Confirmation
        if not confirm_action(f"Are you sure you want to sell {selected_artifact.name} for {sell_price} credits?"):
            return

        # Sell the artifact
        self.player.inventory.artifacts.pop(choice - 1)
        self.player.cloud_credits += sell_price

        display_notification(
            f"Sold {selected_artifact.name} for {sell_price} credits!",
            "success"
        )

    def sell_services(self, vendor) -> None:
        """Sell services to a vendor."""
        if not self.player.inventory.services:
            print(f"{CLR_ERROR}You don't have any services to sell.{CLR_RESET}")
            return

        print(f"\n{CLR_SECTION}[SELL SERVICES]{CLR_RESET}")

        # Display services
        for i, service in enumerate(self.player.inventory.services, 1):
            # Selling price is half the deploy cost
            sell_price = service.deploy_cost
            print(
                f"{i}. {service.name} - {service.description} (Sell price: {sell_price} credits)")

        print(f"{len(self.player.inventory.services) + 1}. Cancel")

        choice = get_valid_input("Select a service to sell: ",
                                 range(1, len(self.player.inventory.services) + 2))

        if choice == len(self.player.inventory.services) + 1:
            return

        # Get selected service
        selected_service = self.player.inventory.services[choice - 1]
        sell_price = selected_service.deploy_cost

        # Confirmation
        if not confirm_action(f"Are you sure you want to sell {selected_service.name} for {sell_price} credits?"):
            return

        # Sell the service
        self.player.inventory.services.pop(choice - 1)
        self.player.cloud_credits += sell_price

        display_notification(
            f"Sold {selected_service.name} for {sell_price} credits!",
            "success"
        )

    def system_menu(self) -> None:
        """Display system menu for game options."""
        while True:
            print(f"\n{CLR_SECTION}[SYSTEM MENU]{CLR_RESET}")
            print("1. Save Game")
            print("2. Load Game")
            print("3. Game Options")
            print("4. View Help")
            print("5. Credits")
            print("6. Quit Game")
            print("7. Return to Game")

            choice = get_valid_input("Enter your choice: ", range(1, 8))

            if choice == 1:
                print("Save game functionality not implemented in this version.")
                input("\nPress Enter to continue...")
            elif choice == 2:
                print("Load game functionality not implemented in this version.")
                input("\nPress Enter to continue...")
            elif choice == 3:
                self.game_options()
            elif choice == 4:
                self.view_help()
            elif choice == 5:
                self.show_credits()
            elif choice == 6:
                if confirm_action("Are you sure you want to quit? All unsaved progress will be lost."):
                    self.game_over = True
                    self.win_reason = "You decided to quit the game."
                    return
            elif choice == 7:
                return

    def game_options(self) -> None:
        """Display game options menu."""
        print(f"\n{CLR_SECTION}[GAME OPTIONS]{CLR_RESET}")
        print(f"1. Difficulty: {self.difficulty.capitalize()}")
        print("2. Toggle Debug Mode")
        print("3. Return")

        choice = get_valid_input("Enter your choice: ", range(1, 4))

        if choice == 1:
            print("\nSelect difficulty:")
            print("1. Easy")
            print("2. Normal")
            print("3. Hard")

            diff_choice = get_valid_input("Enter your choice: ", range(1, 4))

            if diff_choice == 1:
                self.difficulty = "easy"
            elif diff_choice == 2:
                self.difficulty = "normal"
            elif diff_choice == 3:
                self.difficulty = "hard"

            print(f"Difficulty set to {self.difficulty.capitalize()}.")
        elif choice == 2:
            self.debug_mode = not self.debug_mode
            status = "enabled" if self.debug_mode else "disabled"
            print(f"Debug mode {status}.")

        input("\nPress Enter to continue...")

    def view_help(self) -> None:
        """Display help information."""
        print(f"\n{CLR_SECTION}[HELP]{CLR_RESET}")

        help_topics = [
            "1. Basic Controls",
            "2. Combat",
            "3. Services & Artifacts",
            "4. Factions & Reputation",
            "5. Return"
        ]

        for topic in help_topics:
            print(topic)

        choice = get_valid_input(
            "Select a topic: ", range(1, len(help_topics) + 1))

        if choice == 1:
            print(f"\n{CLR_CYAN}Basic Controls:{CLR_RESET}")
            print("- Use number keys to navigate menus and make choices.")
            print("- Explore locations to find resources and advance the story.")
            print("- Travel between locations to discover new areas.")
            print("- Manage your services to generate income.")
            print("- Use artifacts to gain advantages and uncover secrets.")
            print("- Complete quests to gain rewards and advance the storyline.")
        elif choice == 2:
            print(f"\n{CLR_CYAN}Combat:{CLR_RESET}")
            print("- Combat occurs when facing digital threats or hostile entities.")
            print("- Use your artifacts as weapons and defenses.")
            print("- Different threats are vulnerable to different artifacts.")
            print("- Your skills affect your combat effectiveness.")
            print(
                "- Health is depleted during combat - restore it by resting or using items.")
        elif choice == 3:
            print(f"\n{CLR_CYAN}Services & Artifacts:{CLR_RESET}")
            print("- Services generate passive income when deployed.")
            print("- Services can be damaged and require maintenance.")
            print("- Artifacts are tools that provide special abilities.")
            print("- Artifacts have cooldowns after use.")
            print("- Some artifacts can be upgraded to increase their effectiveness.")
        elif choice == 4:
            print(f"\n{CLR_CYAN}Factions & Reputation:{CLR_RESET}")
            print("- CorpSec: Corporate security forces maintaining order.")
            print("- DataBrokers: Information traders and database specialists.")
            print(
                "- ServerlessCollective: Progressive cloud engineers focused on serverless tech.")
            print(
                "- ShadowNetwork: Underground network of hackers with mysterious motives.")
            print("- Higher reputation grants access to better quests and vendors.")

        input("\nPress Enter to continue...")

    def show_credits(self) -> None:
        """Show game credits."""
        print(f"\n{CLR_SECTION}[CREDITS]{CLR_RESET}")
        print("Cloud Ranger: Digital Frontier")
        print("\nDeveloped by:")
        print("- Python Gaming Studio")
        print("\nSpecial thanks to:")
        print("- AWS for cloud inspiration")
        print("- Text-based adventure games everywhere")

        input("\nPress Enter to continue...")

    def check_events(self) -> bool:
        """Check for events at the current location.
        
        Returns:
            True if an event was triggered, False otherwise
        """
        if not self.player or not self.player.current_location:
            return False

        # Get events that could trigger
        triggerable_events = []
        for event_id, event in self.events.items():
            if event.can_trigger(self.player):
                triggerable_events.append(event)

        # Randomly trigger one event if available
        # 30% chance for an event
        if triggerable_events and random.randint(1, 100) <= 30:
            event = random.choice(triggerable_events)
            event.trigger(self.player)
            return True

        return False

    def check_game_over(self) -> bool:
        """Check win/lose conditions.
        
        Returns:
            True if game is over, False otherwise
        """
        if not self.player:
            return True

        # Check if player has run out of time
        if self.current_day >= self.player.time_left:
            self.game_over = True
            self.win_reason = "You have run out of time! The Shadow Admin's plans have succeeded."
            return True

        # Check if player has no health
        if self.player.health <= 0:
            self.game_over = True
            self.win_reason = "You have been critically injured and can no longer continue."
            return True

        # Check if player is completely broke with no services
        if (self.player.cloud_credits <= 0 and
            not self.player.inventory.deployed_services and
                not self.player.inventory.artifacts):
            self.game_over = True
            self.win_reason = "You've run out of resources and can no longer continue your mission."
            return True

        # Check if game is already in a win state
        if self.game_won:
            return True

        # Check for win condition - shadow admin quest
        if "shadow_admin" in self.player.completed_quests:
            self.game_won = True
            self.game_over = True
            self.win_reason = "You have unmasked the Shadow Admin and saved Cloud City!"
            return True

        return False

    def end_game(self) -> None:
        """Display end game screen and final stats."""
        clear_screen()

        if self.game_won:
            # Victory screen
            print(
                f"\n{CLR_SUCCESS}╔══════════════════════════════════════════════════════════╗{CLR_RESET}")
            print(
                f"{CLR_SUCCESS}║                       VICTORY!                           ║{CLR_RESET}")
            print(
                f"{CLR_SUCCESS}╚══════════════════════════════════════════════════════════╝{CLR_RESET}")
        else:
            # Game over screen
            print(
                f"\n{CLR_ERROR}╔══════════════════════════════════════════════════════════╗{CLR_RESET}")
            print(
                f"{CLR_ERROR}║                      GAME OVER                           ║{CLR_RESET}")
            print(
                f"{CLR_ERROR}╚══════════════════════════════════════════════════════════╝{CLR_RESET}")

        print(f"\n{self.win_reason}")

        # Display final stats if player exists
        if self.player:
            print(f"\n{CLR_SECTION}[FINAL STATS]{CLR_RESET}")
            print(f"Days Played: {self.current_day}")
            print(f"Final Cloud Credits: {self.player.cloud_credits}")
            print(
                f"Deployed Services: {len(self.player.inventory.deployed_services)}")
            print(
                f"Artifacts Collected: {len(self.player.inventory.artifacts)}")
            print(f"Quests Completed: {len(self.player.completed_quests)}")
            print(f"Locations Discovered: {len(self.discovered_locations)}")

            # Display skill levels
            print(f"\n{CLR_SECTION}[FINAL SKILLS]{CLR_RESET}")
            for skill, level in self.player.skills.items():
                stars = '★' * level + '☆' * (10 - level)
                print(f"{skill.capitalize()}: {stars}")

            # Display faction reputations
            print(f"\n{CLR_SECTION}[FACTION STANDINGS]{CLR_RESET}")
            for faction, rep in self.player.faction_reputation.items():
                standing = "Allied" if rep >= 75 else "Friendly" if rep >= 50 else "Neutral" if rep >= 25 else "Hostile"
                print(f"{faction}: {rep}/100 ({standing})")

        print(
            f"\n{CLR_TITLE}Thanks for playing Cloud Ranger: Digital Frontier!{CLR_RESET}")
        input("\nPress Enter to exit...")
