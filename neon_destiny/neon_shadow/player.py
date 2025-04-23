"""
Player and CloudRanger classes for the Neon Shadow game.
"""

from typing import Dict, Optional, List, Set
from .constants import *
from .utils import display_notification
from .inventory import Inventory


class Player:
    def __init__(self, name: str, initial_skills: Optional[Dict[str, int]] = None) -> None:
        """Initialize player with name and skills.

        Args:
            name: Player's name
            initial_skills: Optional dictionary of initial skill levels
        """
        self.name: str = name
        self.faction_reputation: Dict[str, int] = {
            "CorpSec": 50,
            "DataBrokers": 50,
            "ServerlessCollective": 50,
            "ShadowNetwork": 10
        }
        self.skill_levels: Dict[str, int] = initial_skills if initial_skills else {
            "cloud": 1,
            "security": 1,
            "database": 1,
            "investigation": 1,
            "networking": 1,
            "serverless": 1
        }


class CloudRanger:
    """Player character class representing a cloud security specialist."""

    def __init__(self, name, specialty, initial_skills=None):
        """Initialize a new CloudRanger character.

        Args:
            name (str): Character name
            specialty (str): Character's specialty/focus area
            initial_skills (dict, optional): Initial skill levels
        """
        self.name = name
        self.specialty = specialty
        self.inventory = Inventory()
        self.current_location = None
        self.completed_missions = []
        self.active_missions = []
        self.reputation = {
            "general": 0,  # General reputation score
            "missions": {}  # Mission-specific reputation scores
        }
        self.skills = initial_skills if initial_skills else {
            'hacking': 1,
            'networking': 1,
            'security': 1,
            'cloud': 1,
            'database': 1,
            'investigation': 1,
            'serverless': 1
        }
        self.bandwidth = 100      # Starting bandwidth
        self.time_left = 365      # Days remaining
        self.clues = set()        # Set of discovered clue IDs
        self.faction_reputation = {
            "CorpSec": 50,
            "DataBrokers": 50,
            "ServerlessCollective": 50,
            "ShadowNetwork": 10  # Start low with the antagonist
        }
        self.completed_quests = []  # List of completed quest IDs
        self.active_quests = []     # List of active quest IDs
        self.temp_skill_boosts = []  # List of temporary skill boosts
        self.logs = []              # Game event logs
        self.achievements = set()   # Set of achievement IDs
        self.health = 100           # Player health
        self.max_health = 100       # Maximum player health
        self.energy = 100           # Current energy level
        self.max_energy = 100       # Maximum energy
        self.status_effects = []    # List of temporary status effects

    @property
    def cloud_credits(self):
        """Get player's cloud credits."""
        return self.inventory.cloud_credits

    @cloud_credits.setter
    def cloud_credits(self, value):
        """Set player's cloud credits."""
        self.inventory.cloud_credits = max(0, value)

    def add_artifact(self, artifact):
        """Add an artifact to inventory."""
        if self.inventory.add_artifact(artifact):
            display_notification(
                f"Acquired artifact: {artifact.name}", "success")
            return True
        else:
            display_notification(
                "Inventory full! Cannot acquire artifact.", "error")
            return False

    def has_artifact(self, artifact_name):
        """Check if player has an artifact."""
        return self.inventory.has_artifact(artifact_name)

    def get_artifact(self, artifact_name):
        """Get an artifact by name."""
        return self.inventory.get_artifact(artifact_name)

    def add_service(self, service):
        """Add a service to inventory."""
        if self.inventory.add_service(service):
            display_notification(
                f"Acquired service: {service.name}", "success")
            return True
        else:
            display_notification(
                "Service limit reached! Cannot acquire service.", "error")
            return False

    def has_service(self, service_name):
        """Check if player has a service."""
        return self.inventory.has_service(service_name)

    def get_service(self, service_name):
        """Get a service by name."""
        return self.inventory.get_service(service_name)

    def add_clue(self, clue_id):
        """Add a clue to the player's collection."""
        if clue_id not in self.clues:
            self.clues.add(clue_id)
            display_notification(f"New Clue Added! ({clue_id})", "info")
            return True
        return False

    def add_quest(self, quest_id):
        """Add a quest to the player's active quests."""
        if quest_id not in self.active_quests and quest_id not in self.completed_quests:
            self.active_quests.append(quest_id)
            display_notification(f"New Quest Added! ({quest_id})", "info")
            return True
        return False

    def complete_quest(self, quest_id):
        """Mark a quest as completed."""
        if quest_id in self.active_quests:
            self.active_quests.remove(quest_id)
            self.completed_quests.append(quest_id)
            self.cloud_credits += 50  # Quest completion bonus
            display_notification(
                f"Quest Completed! ({quest_id}) +50 credits", "success")
            return True
        return False

    def increase_skill(self, skill, amount=1):
        """Increase a skill level."""
        if skill in self.skills:
            self.skills[skill] = min(
                10, self.skills[skill] + amount)
            display_notification(
                f"Skill Increased: {skill} is now level {self.skills[skill]}", "success")
            return True
        return False

    def log_event(self, event):
        """Log a game event."""
        import time  # Import here to avoid circular imports
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"[{timestamp}] {event}")

    def award_achievement(self, achievement_id, name):
        """Award an achievement to the player."""
        if achievement_id not in self.achievements:
            self.achievements.add(achievement_id)
            display_notification(f"Achievement Unlocked: {name}", "success")
            return True
        return False

    def display_status(self):
        """Display player status information."""
        from .utils import clear_screen  # Import here to avoid circular imports

        clear_screen()
        print(
            f"\n{CLR_BRIGHT}{CLR_CYAN}╔════════ PLAYER STATUS ════════╗{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Name: {self.name}{' ' * (27 - len(self.name))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Specialty: {self.specialty}{' ' * (23 - len(self.specialty))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Location: {self.current_location.name if self.current_location else 'Unknown'}{' ' * (20 - len(self.current_location.name) if self.current_location else 13)}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Cloud Credits: {self.cloud_credits}{' ' * (16 - len(str(self.cloud_credits)))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Health: {self.health}/{self.max_health}{' ' * (22 - len(str(self.health)) - len(str(self.max_health)))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Energy: {self.energy}/{self.max_energy}{' ' * (22 - len(str(self.energy)) - len(str(self.max_energy)))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Bandwidth: {self.bandwidth}{' ' * (20 - len(str(self.bandwidth)))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Time Left: {self.time_left} days{' ' * (16 - len(str(self.time_left)))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Clues: {len(self.clues)} collected{' ' * (15 - len(str(len(self.clues))))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")

        print(f"{CLR_BRIGHT}{CLR_CYAN}╠═════ FACTION REPUTATION ══════╣{CLR_RESET}")
        for faction, rep in self.faction_reputation.items():
            rep_str = f"{faction}: {rep}/100"
            print(
                f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} {rep_str}{' ' * (29 - len(rep_str))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")

        print(f"{CLR_BRIGHT}{CLR_CYAN}╠════════ SKILL LEVELS ══════════╣{CLR_RESET}")

        for skill, level in self.skills.items():
            stars = '★' * level + '☆' * (10 - level)
            skill_with_boost = ""
            # Check for temp boosts
            for boost in self.temp_skill_boosts:
                if boost['skill'] == skill:
                    skill_with_boost = f" (+{boost['amount']} for {boost['remaining_days']}d)"
                    break

            print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} {skill.capitalize()}: {stars}{skill_with_boost}{' ' * max(0, 10 - len(skill) - len(skill_with_boost))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")

        print(f"{CLR_BRIGHT}{CLR_CYAN}╠════════ ACTIVE QUESTS ═════════╣{CLR_RESET}")
        if self.active_quests:
            for quest in self.active_quests[:3]:  # Show max 3 quests
                print(
                    f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} • {quest}{' ' * (28 - len(str(quest)))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
            if len(self.active_quests) > 3:
                print(
                    f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} ... and {len(self.active_quests) - 3} more{' ' * 17}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        else:
            print(
                f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} No active quests{' ' * 15}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")

        if self.status_effects:
            print(
                f"{CLR_BRIGHT}{CLR_CYAN}╠════════ STATUS EFFECTS ════════╣{CLR_RESET}")
            for effect in self.status_effects:
                effect_text = f"{effect['name']} ({effect['duration']} turns)"
                print(
                    f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} • {effect_text}{' ' * (28 - len(effect_text))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")

        print(f"{CLR_BRIGHT}{CLR_CYAN}╚══════════════════════════════════╝{CLR_RESET}")

        # Show full inventory
        self.inventory.display()

        input(f"{CLR_PROMPT}Press Enter to continue...{CLR_RESET}")

    def update_faction_reputation(self, faction: str, change: int) -> None:
        """Update reputation with a faction."""
        old_rep = self.faction_reputation.get(faction, 0)
        self.faction_reputation[faction] = max(0, min(100, old_rep + change))

        if change > 0:
            display_notification(
                f"{faction} reputation increased by {change} (Now: {self.faction_reputation[faction]})", "success")
        else:
            display_notification(
                f"{faction} reputation decreased by {-change} (Now: {self.faction_reputation[faction]})", "warning")

    def heal(self, amount: int) -> int:
        """Heal the player by the specified amount."""
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        actual_heal = self.health - old_health
        if actual_heal > 0:
            display_notification(f"Recovered {actual_heal} health", "success")
        return actual_heal

    def take_damage(self, amount: int, source: str = "unknown") -> bool:
        """Take damage from a source. Returns True if player is still alive."""
        self.health = max(0, self.health - amount)
        display_notification(f"Took {amount} damage from {source}!", "error")

        if self.health <= 0:
            display_notification("You have been critically injured!", "error")
            return False
        return True

    def add_status_effect(self, effect: Dict) -> None:
        """Add a status effect to the player."""
        # Example effect: {"name": "Digital Burn", "duration": 3, "per_turn_effect": lambda player: player.take_damage(5, "burn")}
        self.status_effects.append(effect)
        display_notification(
            f"Status effect applied: {effect['name']}", "warning")

    def update_status_effects(self) -> None:
        """Update all status effects and remove expired ones."""
        remaining_effects = []
        for effect in self.status_effects:
            # Apply per-turn effect if defined
            if 'per_turn_effect' in effect and callable(effect['per_turn_effect']):
                effect['per_turn_effect'](self)

            effect['duration'] -= 1
            if effect['duration'] > 0:
                remaining_effects.append(effect)
            else:
                display_notification(
                    f"Status effect expired: {effect['name']}", "info")
                # Apply end effect if defined
                if 'end_effect' in effect and callable(effect['end_effect']):
                    effect['end_effect'](self)

        self.status_effects = remaining_effects

    def restore_energy(self, amount: int) -> int:
        """Restore player energy. Returns amount actually restored."""
        old_energy = self.energy
        self.energy = min(self.max_energy, self.energy + amount)
        return self.energy - old_energy

    def use_energy(self, amount: int) -> bool:
        """Use player energy. Returns False if not enough energy."""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
