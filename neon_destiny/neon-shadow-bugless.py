import os
import sys
import time
import json
import copy
import random
import uuid
from collections import defaultdict
from typing import Dict, Optional, List, Union, Set, Any, Tuple

# --- Player Class ---


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


# Constants section at top
GAME_CONSTANTS = {
    'MAX_REPUTATION': 100,
    'MIN_REPUTATION': 0,
    'DEFAULT_SKILL_LEVEL': 1
}

# Type definitions
LocationType = Dict[str, Union[str, List[str], int]]
ReputationType = Dict[str, int]

# --- Attempt to import and initialize colorama ---
try:
    import colorama
    colorama.init(autoreset=True)  # Autoreset resets color after each print
    CLR_RESET = colorama.Style.RESET_ALL
    # Define Foreground Colors
    CLR_BLACK = colorama.Fore.BLACK
    CLR_RED = colorama.Fore.RED
    CLR_GREEN = colorama.Fore.GREEN
    CLR_YELLOW = colorama.Fore.YELLOW
    CLR_BLUE = colorama.Fore.BLUE
    CLR_MAGENTA = colorama.Fore.MAGENTA
    CLR_CYAN = colorama.Fore.CYAN
    CLR_WHITE = colorama.Fore.WHITE
    CLR_LIGHTBLACK_EX = colorama.Fore.LIGHTBLACK_EX
    CLR_LIGHTRED_EX = colorama.Fore.LIGHTRED_EX
    CLR_LIGHTGREEN_EX = colorama.Fore.LIGHTGREEN_EX
    CLR_LIGHTYELLOW_EX = colorama.Fore.LIGHTYELLOW_EX
    CLR_LIGHTBLUE_EX = colorama.Fore.LIGHTBLUE_EX
    CLR_LIGHTMAGENTA_EX = colorama.Fore.LIGHTMAGENTA_EX
    CLR_LIGHTCYAN_EX = colorama.Fore.LIGHTCYAN_EX
    CLR_LIGHTWHITE_EX = colorama.Fore.LIGHTWHITE_EX
    # Define Background Colors
    CLR_BACK_RED = colorama.Back.RED
    CLR_BACK_GREEN = colorama.Back.GREEN
    CLR_BACK_BLUE = colorama.Back.BLUE
    CLR_BACK_BLACK = colorama.Back.BLACK
    CLR_BACK_CYAN = colorama.Back.CYAN
    # Define Styles
    CLR_BRIGHT = colorama.Style.BRIGHT
    CLR_DIM = colorama.Style.DIM
    CLR_NORMAL = colorama.Style.NORMAL
except ImportError:
    print("Warning: Colorama library not found. Colors will not be used.")
    CLR_RESET = ""
    CLR_BLACK = CLR_RED = CLR_GREEN = CLR_YELLOW = CLR_BLUE = CLR_MAGENTA = CLR_CYAN = CLR_WHITE = ""
    CLR_LIGHTBLACK_EX = CLR_LIGHTRED_EX = CLR_LIGHTGREEN_EX = CLR_LIGHTYELLOW_EX = CLR_LIGHTBLUE_EX = ""
    CLR_LIGHTMAGENTA_EX = CLR_LIGHTCYAN_EX = CLR_LIGHTWHITE_EX = ""
    CLR_BACK_RED = CLR_BACK_GREEN = CLR_BACK_BLUE = CLR_BACK_BLACK = CLR_BACK_CYAN = ""
    CLR_BRIGHT = CLR_DIM = CLR_NORMAL = ""

# --- Constants for Game Elements ---
CLR_NARRATOR = CLR_LIGHTCYAN_EX
CLR_PLAYER_INPUT = CLR_WHITE
CLR_PROMPT = CLR_YELLOW
CLR_LOCATION_NAME = CLR_BRIGHT + CLR_GREEN
CLR_LOCATION_DESC = CLR_GREEN
CLR_INTERACTION = CLR_BRIGHT + CLR_YELLOW
CLR_CLUE = CLR_BRIGHT + CLR_YELLOW
CLR_ERROR = CLR_BRIGHT + CLR_RED
CLR_SUCCESS = CLR_BRIGHT + CLR_GREEN
CLR_SYSTEM = CLR_BLUE
CLR_SHADOW_ADMIN = CLR_BRIGHT + CLR_MAGENTA
CLR_ARTIFACT = CLR_LIGHTMAGENTA_EX
CLR_CLOUD_SERVICE = CLR_LIGHTBLUE_EX
CLR_TUTORIAL = CLR_BRIGHT + CLR_CYAN
CLR_TERMINAL = CLR_BRIGHT + CLR_BLACK
CLR_TERMINAL_TEXT = CLR_BRIGHT + CLR_GREEN
CLR_CREDITS = CLR_BRIGHT + CLR_YELLOW
CLR_HAZARD = CLR_BRIGHT + CLR_RED
CLR_SECTION = CLR_BRIGHT + CLR_CYAN
CLR_BONUS = CLR_BRIGHT + CLR_GREEN
CLR_WARNING = CLR_BRIGHT + CLR_YELLOW

CLR_TITLE = CLR_BRIGHT + CLR_BLUE

# Common message constants
PRESS_ENTER = "\nPress Enter to continue..."

# --- Helper Functions ---


def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_slow(text: str, delay: float = 0.03, color: str = CLR_RESET, newline: bool = True) -> None:
    """Prints text character by character with optional color."""
    for char in text:
        sys.stdout.write(color + char + CLR_RESET)
        sys.stdout.flush()
        time.sleep(delay)
    if newline:
        print()  # Newline at the end


def display_ascii_art(art, color=CLR_WHITE):
    """Prints multi-line ASCII art string with specified color."""
    print(color)
    print(art)
    print(CLR_RESET)


def display_loading_bar(text, duration=2, segments=20):
    """Display a loading bar with text."""
    print(text, end='')
    sys.stdout.flush()
    for i in range(segments + 1):
        time.sleep(duration / segments)
        completed = '█' * i
        remaining = '░' * (segments - i)
        percent = int((i / segments) * 100)
        print(
            f"\r{text} [{CLR_BRIGHT}{CLR_GREEN}{completed}{CLR_RESET}{remaining}] {percent}%", end='')
        sys.stdout.flush()
    print("\r" + " " * (len(text) + segments + 10), end="\r")  # Clear the line


def terminal_effect(text, delay=0.005):
    """Creates a terminal typing effect."""
    print(f"{CLR_TERMINAL}{CLR_BACK_BLACK}╔════ TERMINAL SESSION ════╗{CLR_RESET}")
    print(f"{CLR_TERMINAL}{CLR_BACK_BLACK}║                          ║{CLR_RESET}")

    lines = text.split('\n')
    for line in lines:
        print(f"{CLR_TERMINAL}{CLR_BACK_BLACK}║ {CLR_RESET}", end="")
        print_slow(line, delay=delay, color=CLR_TERMINAL_TEXT, newline=False)
        # Calculate padding
        padding = 24 - len(line)  # 24 is the width of our terminal
        print(" " * padding, end="")
        print(f"{CLR_TERMINAL}{CLR_BACK_BLACK} ║{CLR_RESET}")

    print(f"{CLR_TERMINAL}{CLR_BACK_BLACK}║                          ║{CLR_RESET}")
    print(f"{CLR_TERMINAL}{CLR_BACK_BLACK}╚══════════════════════════╝{CLR_RESET}")


def hacker_animation(duration=2):
    """Display a hacking animation for the given duration."""
    characters = ['/', '-', '\\', '|']
    operations = ['DECRYPTING', 'BYPASSING',
                  'ACCESSING', 'INJECTING', 'EXTRACTING']
    targets = ['FIREWALL', 'MAINFRAME', 'DATABASE', 'NETWORK', 'SECURITY']

    start_time = time.time()
    i = 0
    while time.time() - start_time < duration:
        operation = random.choice(operations)
        target = random.choice(targets)
        print(
            f"\r{CLR_BRIGHT}{CLR_GREEN}{characters[i % len(characters)]} {operation} {target}... {CLR_RESET}", end='')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    print("\r" + " " * 50, end="\r")  # Clear the line


def display_choices(choices):
    """Display a list of choices with options."""
    for idx, choice in enumerate(choices, 1):
        print(f"{CLR_PROMPT}[{idx}] {choice}{CLR_RESET}")
    print(f"{CLR_PROMPT}Enter your choice (1-{len(choices)}): {CLR_RESET}", end='')
    return input()


def display_aws_info(service, description, uses):
    """Display AWS service information in a formatted box."""
    print(f"\n{CLR_BRIGHT}{CLR_BACK_BLUE}┌─{'─' * (len(service) + 2)}─┐{CLR_RESET}")
    print(f"{CLR_BRIGHT}{CLR_BACK_BLUE}│ {CLR_WHITE}{service} │{CLR_RESET}")
    print(f"{CLR_BRIGHT}{CLR_BACK_BLUE}└─{'─' * (len(service) + 2)}─┘{CLR_RESET}")
    print(f"{CLR_CLOUD_SERVICE}Description: {description}{CLR_RESET}")
    print(f"{CLR_CLOUD_SERVICE}Common Uses: {uses}{CLR_RESET}")


def display_notification(message, type="info"):
    """Display a notification banner."""
    if type == "success":
        color = CLR_BRIGHT + CLR_GREEN
        prefix = "✓ SUCCESS"
    elif type == "warning":
        color = CLR_BRIGHT + CLR_YELLOW
        prefix = "⚠ WARNING"
    elif type == "error":
        color = CLR_BRIGHT + CLR_RED
        prefix = "✗ ERROR"
    elif type == "info":
        color = CLR_BRIGHT + CLR_BLUE
        prefix = "ℹ INFO"
    else:
        color = CLR_RESET
        prefix = "NOTIFICATION"

    # Calculate required width based on message length
    content_length = len(prefix) + 2 + len(message)  # 2 for ": "
    box_width = max(50, content_length + 4)  # minimum 50 chars, +4 for margins
    padding = box_width - 2  # -2 for the box edges

    # Create the box
    top_border = "═" * (box_width - 2)
    print(f"\n{color}╔{top_border}╗{CLR_RESET}")

    # Print message with dynamic padding
    remaining_space = padding - (len(prefix) + 2 + len(message))
    print(f"{color}║ {prefix}: {message}{' ' * remaining_space} ║{CLR_RESET}")

    # Bottom border
    print(f"{color}╚{top_border}╝{CLR_RESET}")


def display_mini_map(current_location, locations):
    """Display a mini map of nearby locations."""
    print(f"\n{CLR_BRIGHT}{CLR_CYAN}╔══ MINI MAP ══╗{CLR_RESET}")
    for location in locations:
        if location == current_location:
            print(
                f"{CLR_BRIGHT}{CLR_CYAN}║ {CLR_BRIGHT}{CLR_YELLOW}[*] {location}{CLR_RESET}{' ' * (12 - len(location))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        else:
            print(
                f"{CLR_BRIGHT}{CLR_CYAN}║ {CLR_RESET}[ ] {location}{' ' * (12 - len(location))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
    print(f"{CLR_BRIGHT}{CLR_CYAN}╚═══════════════╝{CLR_RESET}")


def confirm_action(prompt):
    """Ask for confirmation before proceeding."""
    response = input(f"{CLR_PROMPT}{prompt} (y/n): {CLR_RESET}").lower()
    return response == 'y' or response == 'yes'


def display_tutorial_tip(tip):
    """Display a tutorial tip."""
    print(
        f"\n{CLR_TUTORIAL}┌─ TIP ───────────────────────────────────────┐{CLR_RESET}")
    print(f"{CLR_TUTORIAL}│ {tip}{' ' * (44 - len(tip))} │{CLR_RESET}")
    print(f"{CLR_TUTORIAL}└──────────────────────────────────────────────┘{CLR_RESET}")

# --- Core Classes ---


class CloudArtifact:
    """Represents an AWS service or tool the player can use."""

    def __init__(self, name: str, description: str, artifact_type: str, aws_service: str, cost: int, power: int):
        self.name = name
        self.description = description
        self.artifact_type = artifact_type  # Define this properly
        self.aws_service = aws_service
        self.cost = cost
        self.power = power
        self.upgrade_level = 0  # Current upgrade level
        self.max_upgrade = 3  # Maximum upgrade level
        self.cooldown = 0  # Turns until artifact can be used again

    def __str__(self):
        upgrade_stars = '★' * self.upgrade_level + \
            '☆' * (self.max_upgrade - self.upgrade_level)
        return f"{CLR_ARTIFACT}{self.name} {upgrade_stars}{CLR_RESET} ({self.artifact_type})"

    def upgrade(self):
        """Upgrade the artifact if possible."""
        if self.upgrade_level < self.max_upgrade:
            self.upgrade_level += 1
            self.power += 2
            return True
        return False

    def use(self, target=None):
        """Use the artifact on an optional target."""
        if self.cooldown > 0:
            display_notification(
                f"{self.name} is on cooldown for {self.cooldown} more turns", "warning")
            return False

        print(f"Using {self.name}...")
        # Set cooldown based on power - more powerful artifacts have longer cooldowns
        self.cooldown = 1 + (self.power // 3)
        return True

    def update_cooldown(self):
        """Update the artifact cooldown timer."""
        if self.cooldown > 0:
            self.cooldown -= 1
            return True
        return False


class CloudService:
    """Represents an AWS service that can be deployed by the player."""

    def __init__(self, name: str, description: str, service_type: str,
                 cost_per_hour: float, deploy_cost: int,
                 region_availability: List[str],
                 dependencies: Optional[List[str]] = None) -> None:
        self.name = name
        self.description = description
        self.service_type = service_type  # e.g., 'Compute', 'Storage', 'Database'
        self.cost_per_hour = cost_per_hour
        self.deploy_cost = deploy_cost
        self.region_availability = region_availability  # List of regions
        self.dependencies = dependencies if dependencies else []  # List of required services
        self.is_deployed = False
        self.deployment_region = None
        self.health = 100  # Health of the service
        self.security_level = 1  # Security level (1-10)
        self.performance = 5  # Performance level (1-10)
        self.revenue_per_hour = cost_per_hour * 1.5  # Base revenue
        self.instance_id = str(uuid.uuid4())[:8]  # Generate unique instance ID
        self.uptime_days = 0  # Track how long service has been running
        self.last_maintenance = 0  # Day of last maintenance
        self.incident_history = []  # Track past incidents
        self.status_effects = []  # List of active effects on the service

    def __str__(self):
        status = "DEPLOYED" if self.is_deployed else "NOT DEPLOYED"
        return f"{CLR_CLOUD_SERVICE}{self.name}{CLR_RESET} ({self.service_type}) - {status}"

    def deploy(self, region):
        """Deploy the service to a region."""
        if region in self.region_availability:
            self.is_deployed = True
            self.deployment_region = region
            self.uptime_days = 0
            display_notification(
                f"Deployed {self.name} to {region}", "success")
            return True
        else:
            display_notification(
                f"{self.name} not available in {region}", "error")
            return False

    def undeploy(self):
        """Undeploy the service."""
        if self.is_deployed:
            self.is_deployed = False
            self.deployment_region = None
            display_notification(f"Undeployed {self.name}", "info")
            return True
        return False

    def calculate_revenue(self):
        """Calculate revenue generated by this service."""
        if not self.is_deployed:
            return 0

        # Base revenue
        revenue = self.revenue_per_hour

        # Adjust for performance and security
        performance_multiplier = 0.8 + (self.performance / 10) * 0.4
        security_multiplier = 0.9 + (self.security_level / 10) * 0.2

        # Health affects revenue
        health_penalty = 1 - ((100 - self.health) / 100) * 0.5

        # Apply uptime bonus - services become more valuable as they remain stable
        uptime_bonus = min(1.5, 1 + (self.uptime_days / 100))

        return revenue * performance_multiplier * security_multiplier * health_penalty * uptime_bonus

    def apply_damage(self, amount):
        """Apply damage to the service."""
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.is_deployed = False
            display_notification(
                f"{self.name} has failed and is now offline!", "error")
            self.incident_history.append({
                "type": "failure",
                "amount": amount,
                "day": self.uptime_days
            })
            return True  # Indicate service failure

        # Record incident
        self.incident_history.append({
            "type": "damage",
            "amount": amount,
            "day": self.uptime_days
        })
        return False  # Service still operational

    def repair(self, amount):
        """Repair the service."""
        old_health = self.health
        self.health = min(100, self.health + amount)
        self.last_maintenance = self.uptime_days
        display_notification(
            f"Repaired {self.name} (+{self.health - old_health} health)", "success")
        return self.health - old_health  # Return actual amount repaired

    def enhance_security(self, amount):
        """Enhance the security of the service."""
        old_security = self.security_level
        self.security_level = min(10, self.security_level + amount)
        display_notification(
            f"Enhanced {self.name} security (+{self.security_level - old_security})", "success")
        return self.security_level - old_security  # Return actual security increase

    def optimize_performance(self, amount):
        """Optimize the performance of the service."""
        old_performance = self.performance
        self.performance = min(10, self.performance + amount)
        display_notification(
            f"Optimized {self.name} performance (+{self.performance - old_performance})", "success")
        return self.performance - old_performance  # Return actual performance increase

    def add_status_effect(self, effect):
        """Add a temporary status effect to the service."""
        self.status_effects.append(effect)
        display_notification(
            f"{self.name} is now affected by: {effect['name']}", "warning")

    def update_status_effects(self):
        """Update all status effects and remove expired ones."""
        active_effects = []
        for effect in self.status_effects:
            effect['duration'] -= 1
            if effect['duration'] > 0:
                active_effects.append(effect)
                # Apply ongoing effect
                if 'per_turn_effect' in effect and callable(effect['per_turn_effect']):
                    effect['per_turn_effect'](self)
            else:
                display_notification(
                    f"{effect['name']} effect has expired on {self.name}", "info")
                # Apply end effect if defined
                if 'end_effect' in effect and callable(effect['end_effect']):
                    effect['end_effect'](self)

        self.status_effects = active_effects


class Inventory:
    """Handles the player's inventory of artifacts and cloud services."""

    def __init__(self):
        self.artifacts = []
        self.services = []  # Undeployed service blueprints
        self.deployed_services = []  # Currently deployed service instances
        self.cloud_credits = 500
        self.max_artifacts = 10
        self.max_services = 5
        self.consumables = {}  # Dictionary of consumable items with counts

    def add_artifact(self, artifact):
        """Add an artifact to inventory if there's space."""
        if len(self.artifacts) < self.max_artifacts:
            self.artifacts.append(artifact)
            return True
        return False

    def remove_artifact(self, artifact_name):
        """Remove an artifact by name."""
        for i, art in enumerate(self.artifacts):
            if art.name == artifact_name:
                return self.artifacts.pop(i)
        return None

    def get_artifact(self, artifact_name):
        """Get an artifact by name."""
        for art in self.artifacts:
            if art.name == artifact_name:
                return art
        return None

    def has_artifact(self, artifact_name):
        """Check if player has an artifact."""
        return any(art.name == artifact_name for art in self.artifacts)

    def add_service(self, service):
        """Add a service to inventory if there's space."""
        if len(self.services) < self.max_services:
            self.services.append(service)
            return True
        return False

    def remove_service(self, service_name):
        """Remove a service by name."""
        for i, svc in enumerate(self.services):
            if svc.name == service_name:
                return self.services.pop(i)
        return None

    def get_service(self, service_name):
        """Get a service by name."""
        for svc in self.services:
            if svc.name == service_name:
                return svc
        return None

    def has_service(self, service_name):
        """Check if player has a service."""
        return any(svc.name == service_name for svc in self.services)

    def display(self):
        """Display the inventory contents."""
        print(f"\n{CLR_BRIGHT}{CLR_CYAN}══════ INVENTORY ══════{CLR_RESET}")
        print(f"{CLR_CREDITS}Cloud Credits: {self.cloud_credits}{CLR_RESET}")

        print(
            f"\n{CLR_ARTIFACT}Artifacts ({len(self.artifacts)}/{self.max_artifacts}):{CLR_RESET}")
        if self.artifacts:
            for idx, artifact in enumerate(self.artifacts, 1):
                cooldown_status = f" [COOLDOWN: {artifact.cooldown}]" if artifact.cooldown > 0 else ""
                print(f"{idx}. {artifact} - {artifact.description}{cooldown_status}")
        else:
            print("No artifacts in inventory.")

        print(
            f"\n{CLR_CLOUD_SERVICE}Cloud Services ({len(self.services)}/{self.max_services}):{CLR_RESET}")
        if self.services:
            for idx, service in enumerate(self.services, 1):
                print(f"{idx}. {service.name} - {service.description}")
        else:
            print("No cloud services in inventory.")

        print(f"\n{CLR_CLOUD_SERVICE}Deployed Services:{CLR_RESET}")
        if self.deployed_services:
            for idx, service in enumerate(self.deployed_services, 1):
                status = f"{CLR_GREEN}ONLINE{CLR_RESET}" if service.is_deployed else f"{CLR_RED}OFFLINE{CLR_RESET}"
                print(f"{idx}. {service.name} ({service.instance_id}) - {status}")
                if service.is_deployed:
                    print(f"   Region: {service.deployment_region}")
                    print(
                        f"   Health: {service.health}% | Security: {service.security_level}/10 | Performance: {service.performance}/10")
                    print(
                        f"   Revenue: {service.calculate_revenue():.2f} credits/hour | Uptime: {service.uptime_days} days")
                    if service.status_effects:
                        effects = ", ".join(
                            [f"{e['name']} ({e['duration']})" for e in service.status_effects])
                        print(f"   Status Effects: {effects}")
        else:
            print("No deployed services.")

        # Display consumables if any
        if self.consumables:
            print(f"\n{CLR_ARTIFACT}Consumables:{CLR_RESET}")
            for item_name, count in self.consumables.items():
                print(f"• {item_name} x{count}")

    def remove_deployed_service(self, instance_id):
        """Remove a deployed service by its instance ID."""
        for i, service in enumerate(self.deployed_services):
            if service.instance_id == instance_id:
                removed = self.deployed_services.pop(i)
                display_notification(
                    f"Service {removed.name} ({instance_id}) has been removed.", "warning")
                return removed
        return None

    def get_deployed_service(self, instance_id):
        """Get a deployed service by its instance ID."""
        for service in self.deployed_services:
            if service.instance_id == instance_id:
                return service
        return None

    def add_deployed_service(self, service):
        """Add a service to deployed services."""
        if service not in self.deployed_services:
            self.deployed_services.append(service)
            return True
        return False

    def add_consumable(self, item_name, count=1):
        """Add consumable items to inventory."""
        if item_name in self.consumables:
            self.consumables[item_name] += count
        else:
            self.consumables[item_name] = count
        return True

    def use_consumable(self, item_name):
        """Use a consumable item if available."""
        if item_name in self.consumables and self.consumables[item_name] > 0:
            self.consumables[item_name] -= 1
            if self.consumables[item_name] <= 0:
                del self.consumables[item_name]
            return True
        return False

    def update_all_artifacts(self):
        """Update cooldowns for all artifacts."""
        for artifact in self.artifacts:
            artifact.update_cooldown()


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


class Quest:
    """Represents a quest or mission that the player can undertake."""

    def __init__(self, id, title, description, objectives, reward, prereq_quests=None,
                 min_skill_level=None, min_faction_rep=None, location=None):
        self.id = id
        self.title = title
        self.description = description
        # List of objective dicts with 'id', 'description', 'completed'
        self.objectives = objectives
        # Dict with 'credits', 'artifacts', 'faction_rep', 'skill', etc.
        self.reward = reward
        self.prereq_quests = prereq_quests if prereq_quests else []  # List of quest IDs
        self.min_skill_level = min_skill_level if min_skill_level else {}  # Dict of skill: level
        # Example: {'CorpSec': 60, 'DataBrokers': 40}
        self.min_faction_rep = min_faction_rep if min_faction_rep else {}
        self.location = location  # Location where quest is available
        self.time_limit = None  # Optional time limit in days
        self.difficulty = 1  # Quest difficulty (1-10)
        self.hidden = False  # Is this a hidden quest?
        self.completion_date = None  # When the quest was completed

    def is_available(self, player) -> bool:
        """Check if the quest is available to the player."""
        # Check prerequisites
        for quest_id in self.prereq_quests:
            if quest_id not in player.completed_quests:
                return False

        # Check skill requirements
        for skill, level in self.min_skill_level.items():
            if player.skills.get(skill, 0) < level:
                return False

        # Check faction reputation requirements
        for faction, level in self.min_faction_rep.items():
            if player.faction_reputation.get(faction, 0) < level:
                return False

        return True

    def start(self, player) -> bool:
        """Start the quest."""
        if self.is_available(player):
            player.add_quest(self.id)
            return True
        return False

    def complete_objective(self, objective_id) -> bool:
        """Mark an objective as completed."""
        for obj in self.objectives:
            if obj['id'] == objective_id:
                obj['completed'] = True
                return True
        return False

    def check_completion(self) -> bool:
        """Check if all objectives are completed."""
        return all(obj['completed'] for obj in self.objectives)

    def display(self) -> None:
        """Display quest details."""
        print(
            f"\n{CLR_BRIGHT}{CLR_YELLOW}╔══════ QUEST: {self.title} ══════╗{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} {self.description}{CLR_RESET}")

        if self.difficulty:
            diff_stars = '★' * self.difficulty + '☆' * (10 - self.difficulty)
            print(
                f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} Difficulty: {diff_stars}{CLR_RESET}")

        if self.time_limit:
            print(
                f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} Time Limit: {self.time_limit} days{CLR_RESET}")

        print(f"{CLR_BRIGHT}{CLR_YELLOW}╠══════ OBJECTIVES ══════╣{CLR_RESET}")

        for obj in self.objectives:
            status = f"{CLR_GREEN}✓{CLR_RESET}" if obj['completed'] else f"{CLR_RED}□{CLR_RESET}"
            print(
                f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} {status} {obj['description']}")

        print(f"{CLR_BRIGHT}{CLR_YELLOW}╠══════ REWARDS ══════╣{CLR_RESET}")
        if 'credits' in self.reward:
            print(
                f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • {self.reward['credits']} Cloud Credits")
        if 'artifacts' in self.reward:
            for artifact in self.reward['artifacts']:
                print(f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • Artifact: {artifact}")
        if 'faction_rep' in self.reward:
            for faction, change in self.reward['faction_rep'].items():
                print(f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • {faction}: +{change}")
        if 'skill' in self.reward:
            for skill, amount in self.reward['skill'].items():
                print(
                    f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • Skill: {skill.capitalize()} +{amount}")
        if 'consumables' in self.reward:
            for item, count in self.reward['consumables'].items():
                print(
                    f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • {item} x{count}")

        print(f"{CLR_BRIGHT}{CLR_YELLOW}╚═════════════════════════╝{CLR_RESET}")


class Location:
    """Represents a location in the game world."""

    def __init__(self, name, description, region=None, connections=None,
                 events=None, services=None, difficulty=1):
        self.name = name
        self.description = description
        self.region = region  # AWS region this location is in
        # List of connected location names
        self.connections = connections if connections else []
        # List of possible events at this location
        self.events = events if events else []
        # List of available services at this location
        self.services = services if services else []
        self.difficulty = difficulty  # Difficulty level (1-10)
        self.visited = False
        self.discovered_secrets = set()  # Set of discovered secret IDs
        self.unlocked_areas = set()  # Set of unlocked sub-areas
        self.hazards = []  # List of potential hazards at this location
        self.vendors = []  # List of vendors at this location
        self.local_reputation = 0  # Location-specific reputation (0-100)

    def __str__(self):
        return f"{self.name}"

    def display(self):
        """Display location details."""
        if not self.visited:
            self.visited = True
            print(
                f"\n{CLR_LOCATION_NAME}[ NEW LOCATION DISCOVERED: {self.name} ]{CLR_RESET}")
        else:
            print(f"\n{CLR_LOCATION_NAME}[ {self.name} ]{CLR_RESET}")

        print(f"{CLR_LOCATION_DESC}{self.description}{CLR_RESET}")

        if self.region:
            print(f"{CLR_LOCATION_DESC}AWS Region: {self.region}{CLR_RESET}")

        if self.difficulty:
            diff_stars = '★' * self.difficulty + '☆' * (10 - self.difficulty)
            print(f"{CLR_LOCATION_DESC}Difficulty: {diff_stars}{CLR_RESET}")

        print(f"\n{CLR_INTERACTION}Connections:{CLR_RESET}")
        for connection in self.connections:
            print(f"• {connection}")

        if self.hazards:
            print(f"\n{CLR_HAZARD}Potential Hazards:{CLR_RESET}")
            for hazard in self.hazards:
                print(f"• {hazard['name']} - {hazard['description']}")

        if self.vendors:
            print(f"\n{CLR_CLOUD_SERVICE}Local Vendors:{CLR_RESET}")
            for vendor in self.vendors:
                print(f"• {vendor['name']} - {vendor['description']}")

    def add_connection(self, location_name):
        """Add a connection to another location."""
        if location_name not in self.connections:
            self.connections.append(location_name)

    def has_secret(self, secret_id):
        """Check if a particular secret has been discovered."""
        return secret_id in self.discovered_secrets

    def discover_secret(self, secret_id):
        """Discover a secret at this location."""
        if secret_id not in self.discovered_secrets:
            self.discovered_secrets.add(secret_id)
            return True
        return False

    def add_hazard(self, hazard):
        """Add a hazard to this location."""
        self.hazards.append(hazard)

    def add_vendor(self, vendor):
        """Add a vendor to this location."""
        self.vendors.append(vendor)

    def unlock_area(self, area_id):
        """Unlock a sub-area within this location."""
        if area_id not in self.unlocked_areas:
            self.unlocked_areas.add(area_id)
            display_notification(
                f"Unlocked new area in {self.name}: {area_id}", "success")
            return True
        return False

    def increase_reputation(self, amount):
        """Increase local reputation at this location."""
        old_rep = self.local_reputation
        self.local_reputation = min(100, self.local_reputation + amount)
        return self.local_reputation - old_rep


class CloudEvent:
    """Represents an event that can occur at a location."""

    def __init__(self, id, name, description, event_type,
                 effects=None, requirements=None, chance=100, repeatable=False):
        self.id = id
        self.name = name
        self.description = description
        # 'encounter', 'discovery', 'disaster', 'reward', etc.
        self.event_type = event_type
        # Effects on player (health, credits, faction_rep, etc.)
        self.effects = effects if effects else {}
        # Requirements: min_skill, artifacts, clues, min_faction_rep
        self.requirements = requirements if requirements else {}  # Requirements to trigger
        self.chance = chance  # Chance of occurring (percentage)
        self.repeatable = repeatable  # Can this event occur multiple times?
        self.has_occurred = False
        self.cooldown = 0  # Turns until event can trigger again
        self.cooldown_duration = 0  # How long the cooldown should be when triggered

    def can_trigger(self, player) -> bool:
        """Check if the event can be triggered."""
        if self.cooldown > 0:
            return False

        if not self.repeatable and self.has_occurred:
            return False

        # Check player requirements
        if 'min_skill' in self.requirements:
            for skill, level in self.requirements['min_skill'].items():
                if player.skills.get(skill, 0) < level:
                    return False

        if 'artifacts' in self.requirements:
            for artifact in self.requirements['artifacts']:
                if not player.has_artifact(artifact):
                    return False

        if 'clues' in self.requirements:
            for clue in self.requirements['clues']:
                if clue not in player.clues:
                    return False

        # Check faction reputation requirements
        if 'min_faction_rep' in self.requirements:
            for faction, level in self.requirements['min_faction_rep'].items():
                if player.faction_reputation.get(faction, 0) < level:
                    return False

        # Random chance
        if random.randint(1, 100) > self.chance:
            return False

        return True

    def trigger(self, player) -> bool:
        """Trigger the event and apply its effects."""
        print(f"\n{CLR_BRIGHT}{CLR_CYAN}══════ EVENT: {self.name} ══════{CLR_RESET}")
        print_slow(self.description, color=CLR_CYAN)

        # Apply effects
        if 'credits' in self.effects:
            player.cloud_credits += self.effects['credits']
            if self.effects['credits'] > 0:
                print(
                    f"{CLR_SUCCESS}Gained {self.effects['credits']} Cloud Credits{CLR_RESET}")
            else:
                print(
                    f"{CLR_ERROR}Lost {-self.effects['credits']} Cloud Credits{CLR_RESET}")

        if 'skill' in self.effects:
            for skill, amount in self.effects['skill'].items():
                player.increase_skill(skill, amount)

        # Apply faction reputation changes
        if 'faction_rep' in self.effects:
            for faction, change in self.effects['faction_rep'].items():
                if faction in player.faction_reputation:
                    old_rep = player.faction_reputation[faction]
                    player.faction_reputation[faction] = max(
                        0, min(100, old_rep + change))
                    if change > 0:
                        print(
                            f"{CLR_SUCCESS}{faction} reputation increased by {change} (Now: {player.faction_reputation[faction]}){CLR_RESET}")
                    else:
                        print(
                            f"{CLR_ERROR}{faction} reputation decreased by {-change} (Now: {player.faction_reputation[faction]}){CLR_RESET}")
                else:
                    print(
                        f"{CLR_WARNING}Warning: Unknown faction '{faction}' in event effect.{CLR_RESET}")

        if 'artifact' in self.effects:
            artifact = CloudArtifact(
                self.effects['artifact']['name'],
                self.effects['artifact']['description'],
                self.effects['artifact']['artifact_type'],  # Was 'type'
                self.effects['artifact'].get('aws_service'),
                self.effects['artifact'].get('cost', 0),
                self.effects['artifact'].get('power', 1)
            )
            player.add_artifact(artifact)

        if 'clue' in self.effects:
            player.add_clue(self.effects['clue'])

        if 'service' in self.effects:
            service = CloudService(
                name=self.effects['service']['name'],
                description=self.effects['service']['description'],
                service_type=self.effects['service'].get(
                    'service_type', self.effects['service']['type']),
                cost_per_hour=self.effects['service'].get('cost_per_hour', 1),
                deploy_cost=self.effects['service'].get('deploy_cost', 10),
                region_availability=self.effects['service'].get(
                    'region_availability', ['us-east-1']),
                dependencies=self.effects['service'].get('dependencies', [])
            )
            player.add_service(service)

        if 'time' in self.effects:
            player.time_left += self.effects['time']
            if self.effects['time'] > 0:
                print(
                    f"{CLR_SUCCESS}Gained {self.effects['time']} days{CLR_RESET}")
            else:
                print(
                    f"{CLR_ERROR}Lost {-self.effects['time']} days{CLR_RESET}")

        if 'health' in self.effects:
            if self.effects['health'] > 0:
                player.heal(self.effects['health'])
            else:
                player.take_damage(-self.effects['health'], self.name)

        if 'energy' in self.effects:
            if self.effects['energy'] > 0:
                amt = player.restore_energy(self.effects['energy'])
                print(f"{CLR_SUCCESS}Restored {amt} energy{CLR_RESET}")
            else:
                if player.use_energy(-self.effects['energy']):
                    print(
                        f"{CLR_WARNING}Used {-self.effects['energy']} energy{CLR_RESET}")
                else:
                    print(f"{CLR_ERROR}Not enough energy!{CLR_RESET}")

        if 'status_effect' in self.effects:
            player.add_status_effect(self.effects['status_effect'])

        if 'consumable' in self.effects:
            item_name = self.effects['consumable']['name']
            count = self.effects['consumable'].get('count', 1)
            player.inventory.add_consumable(item_name, count)
            print(f"{CLR_SUCCESS}Acquired {count}x {item_name}{CLR_RESET}")

        self.has_occurred = True
        # Set cooldown if defined
        if self.cooldown_duration > 0:
            self.cooldown = self.cooldown_duration
        return True

    def update_cooldown(self):
        """Update the cooldown timer for this event."""
        if self.cooldown > 0:
            self.cooldown -= 1
            return True
        return False


class Game:
    """Main game class that manages the game state and flow."""

    def __init__(self, difficulty="normal"):
        self.current_location = None  # This was missing
        self.locations = {}
        self._create_locations()

        # Initialize these properly
        self.completed_quests: List[str] = []
        self.faction: str = ""
        self.name: str = ""
        self.description: str = ""
        self.type: str = ""
        self.current_loc_name: str = ""
        self.starting_location: Optional[Location] = None

        # Initialize other game components
        self.quests = {}  # Dict of quest ID -> Quest
        self.events = {}  # Dict of event ID -> CloudEvent
        self.artifacts = {}  # Dict of artifact templates
        self.services = {}  # Dict of service templates
        self.current_day = 1
        self.game_over = False
        self.game_won = False
        self.difficulty = difficulty
        self.win_reason = ""
        self.paused = False
        self.battle_mode = False
        self.debug_mode = False
        self.current_enemy = None
        self.discovered_locations = set()
        self.weather_conditions = {}  # Current weather at different locations
        self.global_events = []  # List of active global events

        # Create game content
        self._create_artifacts()
        self._create_services()
        self._create_quests()
        self._create_events()
        self._create_weather_conditions()
        self._create_vendors()

        # Add these initializations
        self.player = None

    def _create_locations(self):
        """Create game world locations."""
        # Cloud City Region - Main Hub
        self.locations["Cloud City"] = Location(
            name="Cloud City",
            description="The central hub for cloud engineers and digital nomads. Towering server racks form the cityscape.",
            region="us-east-1",
            connections=["Serverless Valley",
                         "Database District", "Security Perimeter"],
            difficulty=1
        )

        self.locations["Serverless Valley"] = Location(
            name="Serverless Valley",
            description="A vast landscape where computation resources materialize on demand. Lambda functions flow like rivers.",
            region="us-east-1",
            connections=["Cloud City", "Edge Outpost", "Function Junction"],
            difficulty=2
        )

        self.locations["Database District"] = Location(
            name="Database District",
            description="Rows of data warehouses and database servers line the streets. Queries flow through the air.",
            region="us-east-1",
            connections=["Cloud City", "Analytics Archipelago", "Cache Cove"],
            difficulty=2
        )

        self.locations["Security Perimeter"] = Location(
            name="Security Perimeter",
            description="The defensive wall surrounding Cloud City. Firewalls and security groups monitor all traffic.",
            region="us-east-1",
            connections=["Cloud City", "Identity Federation", "Network Nexus"],
            difficulty=3
        )

        # US-WEST Region
        self.locations["Edge Outpost"] = Location(
            name="Edge Outpost",
            description="A frontier outpost at the edge of the network. CDN caches and edge computing nodes operate here.",
            region="us-west-2",
            connections=["Serverless Valley", "Container Canyon"],
            difficulty=3
        )

        self.locations["Container Canyon"] = Location(
            name="Container Canyon",
            description="Deep ravines filled with container orchestration systems. Docker images flow down the canyon walls.",
            region="us-west-2",
            connections=["Edge Outpost", "Kubernetes Plateau"],
            difficulty=4
        )

        self.locations["Kubernetes Plateau"] = Location(
            name="Kubernetes Plateau",
            description="A vast elevated plain where container pods roam freely. Control planes monitor the horizon.",
            region="us-west-2",
            connections=["Container Canyon", "DevOps Desert"],
            difficulty=5
        )

        # EU Region
        self.locations["Function Junction"] = Location(
            name="Function Junction",
            description="A bustling crossroads where serverless functions are exchanged. Code snippets float through the air.",
            region="eu-west-1",
            connections=["Serverless Valley", "Event Bridge"],
            difficulty=3
        )

        self.locations["Event Bridge"] = Location(
            name="Event Bridge",
            description="A massive bridge spanning a digital chasm. Events flow across it, triggering reactions.",
            region="eu-west-1",
            connections=["Function Junction", "State Machine Forest"],
            difficulty=4
        )

        self.locations["State Machine Forest"] = Location(
            name="State Machine Forest",
            description="A dense forest of workflow trees. Step Functions guide you along predefined paths.",
            region="eu-west-1",
            connections=["Event Bridge", "Microservice Meadows"],
            difficulty=5
        )

        # ASIA Region
        self.locations["Cache Cove"] = Location(
            name="Cache Cove",
            description="A hidden bay where cached data washes ashore. ElastiCache instances bob in the water.",
            region="ap-southeast-1",
            connections=["Database District", "Query Quicksand"],
            difficulty=3
        )

        self.locations["Query Quicksand"] = Location(
            name="Query Quicksand",
            description="Treacherous grounds where poorly optimized queries sink without a trace. Indexes provide safe paths.",
            region="ap-southeast-1",
            connections=["Cache Cove", "NoSQL Nullspace"],
            difficulty=4
        )

        self.locations["NoSQL Nullspace"] = Location(
            name="NoSQL Nullspace",
            description="A strange dimensionless void where traditional database rules don't apply. Document models float freely.",
            region="ap-southeast-1",
            connections=["Query Quicksand", "Blockchain Bazaar"],
            difficulty=5
        )

        # Additional Locations for Advanced Players
        self.locations["Network Nexus"] = Location(
            name="Network Nexus",
            description="The central routing facility for all cloud traffic. VPCs intersect and packets zoom through routers.",
            region="global",
            connections=["Security Perimeter", "Hybrid Harbor"],
            difficulty=6
        )

        self.locations["Hybrid Harbor"] = Location(
            name="Hybrid Harbor",
            description="Where on-premises connections dock with cloud services. Direct Connect cables stretch into the distance.",
            region="global",
            connections=["Network Nexus", "Multi-Cloud Maelstrom"],
            difficulty=7
        )

        self.locations["Analytics Archipelago"] = Location(
            name="Analytics Archipelago",
            description="A collection of islands each dedicated to a different data analytics service.",
            region="us-east-2",
            connections=["Database District", "Machine Learning Marsh"],
            difficulty=6
        )

        self.locations["Machine Learning Marsh"] = Location(
            name="Machine Learning Marsh",
            description="A mysterious wetland where models train and infer. Neural networks form like lily pads.",
            region="us-east-2",
            connections=["Analytics Archipelago", "AI Abyss"],
            difficulty=8
        )

        self.locations["DevOps Desert"] = Location(
            name="DevOps Desert",
            description="A harsh landscape where CI/CD pipelines form oases. CodeBuild and CodeDeploy caravans cross the dunes.",
            region="us-west-1",
            connections=["Kubernetes Plateau", "Infrastructure Wastes"],
            difficulty=7
        )

        self.locations["Infrastructure Wastes"] = Location(
            name="Infrastructure Wastes",
            description="The ancient ruins of manual infrastructure. CloudFormation templates help rebuild civilization.",
            region="us-west-1",
            connections=["DevOps Desert"],
            difficulty=8
        )

        self.locations["Microservice Meadows"] = Location(
            name="Microservice Meadows",
            description="Rolling fields filled with small, specialized service flowers. API Gateways stand like fences.",
            region="eu-central-1",
            connections=["State Machine Forest", "Service Mesh Mountain"],
            difficulty=6
        )

        self.locations["Service Mesh Mountain"] = Location(
            name="Service Mesh Mountain",
            description="A towering peak where services are interconnected in complex meshes. Traffic flows along monitored paths.",
            region="eu-central-1",
            connections=["Microservice Meadows"],
            difficulty=8
        )

        self.locations["Blockchain Bazaar"] = Location(
            name="Blockchain Bazaar",
            description="A bustling marketplace built on distributed ledger technology. Smart contracts seal every deal.",
            region="ap-northeast-1",
            connections=["NoSQL Nullspace", "Quantum Quarry"],
            difficulty=9
        )

        self.locations["Quantum Quarry"] = Location(
            name="Quantum Quarry",
            description="The deepest, most mysterious location. Quantum computing experiments create reality-bending effects.",
            region="ap-northeast-1",
            connections=["Blockchain Bazaar"],
            difficulty=10
        )

        self.locations["Multi-Cloud Maelstrom"] = Location(
            name="Multi-Cloud Maelstrom",
            description="A churning storm where multiple cloud providers' services mix together. Only the most skilled can navigate it.",
            region="global",
            connections=["Hybrid Harbor", "Shadow Admin's Lair"],
            difficulty=9
        )

        self.locations["AI Abyss"] = Location(
            name="AI Abyss",
            description="An unfathomable depth where sentient AI systems evolve. Complex algorithms create emergent behaviors.",
            region="us-east-2",
            connections=["Machine Learning Marsh", "Shadow Admin's Lair"],
            difficulty=9
        )

        self.locations["Shadow Admin's Lair"] = Location(
            name="Shadow Admin's Lair",
            description="The hidden headquarters of the mysterious Shadow Admin who controls the cloud from behind the scenes.",
            region="unknown",
            connections=["Multi-Cloud Maelstrom", "AI Abyss"],
            difficulty=10
        )

        # Add some hazards to higher difficulty locations
        self.locations["Query Quicksand"].add_hazard({
            "name": "Query Collapse",
            "description": "Unstable data structures may collapse, causing damage.",
            "chance": 20,
            "damage": lambda: random.randint(5, 15),
            "avoidable_with_skill": "database"
        })

        self.locations["DevOps Desert"].add_hazard({
            "name": "Broken Pipeline",
            "description": "Damaged CI/CD pipelines can cause deployment failures.",
            "chance": 30,
            "damage": lambda: random.randint(8, 20),
            "avoidable_with_skill": "cloud"
        })

        self.locations["Shadow Admin's Lair"].add_hazard({
            "name": "Security Countermeasures",
            "description": "Powerful defense systems that target intruders.",
            "chance": 50,
            "damage": lambda: random.randint(15, 30),
            "avoidable_with_skill": "security"
        })

        # Add secret areas to some locations
        for loc in ["Cloud City", "Database District", "Function Junction", "Shadow Admin's Lair"]:
            self.locations[loc].unlocked_areas = set()  # Initialize as empty

    def _create_weather_conditions(self):
        """Create weather conditions for locations."""
        weather_types = [
            {"name": "Data Storm", "effect": "Bandwidth -20%",
                "description": "A storm of corrupted data packets"},
            {"name": "Processing Fog", "effect": "Investigation -2",
                "description": "Dense fog reducing visibility"},
            {"name": "CPU Heatwave", "effect": "Energy -10%",
                "description": "Extreme computational heat"},
            {"name": "Memory Frost", "effect": "Service performance -2",
                "description": "Cold conditions slowing memory access"},
            {"name": "Clear Signals", "effect": "All stats +5%",
                "description": "Perfect conditions with clear connections"}
        ]

        # Initialize each location with a random weather condition
        for loc_name, location in self.locations.items():
            # Higher difficulty locations have more extreme weather
            if location.difficulty > 5:
                # Choose one of the harsher conditions
                weather = random.choice(weather_types[:4])
            else:
                weather = random.choice(weather_types)  # Any condition

            self.weather_conditions[loc_name] = {
                "current": weather,
                # Weather will change after this many days
                "duration": random.randint(2, 5),
                "severity": min(10, max(1, location.difficulty // 2 + random.randint(1, 3)))
            }

    def _create_vendors(self):
        """Create vendors for various locations."""
        # Cloud City vendors
        self.locations["Cloud City"].add_vendor({
            "name": "CloudTech Supplies",
            "description": "General store selling basic artifacts and consumables",
            "inventory": {
                "artifacts": ["S3 Scanner", "EC2 Inspector"],
                "consumables": {
                    "Emergency Patch": {
                        "description": "Restores 30 health",
                        "price": 25,
                        "effect": lambda player: player.heal(30)
                    },
                    "Energy Cell": {
                        "description": "Restores 50 energy",
                        "price": 20,
                        "effect": lambda player: player.restore_energy(50)
                    }
                }
            }
        })

        # Security Perimeter vendor
        self.locations["Security Perimeter"].add_vendor({
            "name": "CorpSec Defense Systems",
            "description": "High-quality security artifacts",
            "reputation_required": {"CorpSec": 20},
            "inventory": {
                "artifacts": ["IAM Auditor", "GuardDuty Lens", "WAF Shield"],
                "consumables": {
                    "Firewall Patch": {
                        "description": "Increases service security by 2",
                        "price": 40,
                        "effect": lambda service: service.enhance_security(2)
                    }
                }
            }
        })

        # Database District vendor
        self.locations["Database District"].add_vendor({
            "name": "DataStore Solutions",
            "description": "Database services and optimization tools",
            "inventory": {
                "artifacts": ["RDS Analyzer", "Aurora Analyzer", "DynamoDB Query Engine"],
                "services": ["RDS Database", "DynamoDB Table"]
            }
        })

        # Serverless Valley vendor
        self.locations["Serverless Valley"].add_vendor({
            "name": "FunctionForge",
            "description": "Serverless computing specialists",
            "reputation_required": {"ServerlessCollective": 10},
            "inventory": {
                "artifacts": ["Lambda Invoker"],
                "services": ["Lambda Function", "API Gateway"]
            }
        })

    def _create_artifacts(self):
        """Create artifact templates."""
        # Basic Scanner Artifacts
        self.artifacts["S3 Scanner"] = {
            "name": "S3 Scanner",
            "description": "Scans and analyzes S3 buckets for vulnerabilities.",
            "artifact_type": "Scanner",
            "aws_service": "Amazon S3",
            "cost": 10,
            "power": 1
        }

        self.artifacts["EC2 Inspector"] = {
            "name": "EC2 Inspector",
            "description": "Checks EC2 instances for security issues.",
            "artifact_type": "Scanner",
            "aws_service": "Amazon EC2",
            "cost": 15,
            "power": 2
        }

        self.artifacts["RDS Analyzer"] = {
            "name": "RDS Analyzer",
            "description": "Analyzes database configurations for vulnerabilities.",
            "artifact_type": "Scanner",
            "aws_service": "Amazon RDS",
            "cost": 20,
            "power": 2
        }

        # Network Artifacts
        self.artifacts["VPC Tracer"] = {
            "name": "VPC Tracer",
            "description": "Traces network traffic through Virtual Private Clouds.",
            "artifact_type": "Network",
            "aws_service": "Amazon VPC",
            "cost": 25,
            "power": 3
        }

        self.artifacts["Route53 Resolver"] = {
            "name": "Route53 Resolver",
            "description": "Resolves domain names and finds hidden endpoints.",
            "artifact_type": "Network",
            "aws_service": "Amazon Route 53",
            "cost": 30,
            "power": 3
        }

        # Security Artifacts
        self.artifacts["IAM Auditor"] = {
            "name": "IAM Auditor",
            "description": "Audits IAM permissions and finds policy flaws.",
            "artifact_type": "Security",
            "aws_service": "AWS IAM",
            "cost": 35,
            "power": 4
        }

        self.artifacts["GuardDuty Lens"] = {
            "name": "GuardDuty Lens",
            "description": "Detects threats and suspicious activities.",
            "artifact_type": "Security",
            "aws_service": "Amazon GuardDuty",
            "cost": 40,
            "power": 4
        }

        self.artifacts["WAF Shield"] = {
            "name": "WAF Shield",
            "description": "Protects against web attacks and intrusions.",
            "artifact_type": "Security",
            "aws_service": "AWS WAF",
            "cost": 50,
            "power": 5
        }

        # Compute Artifacts
        self.artifacts["Lambda Invoker"] = {
            "name": "Lambda Invoker",
            "description": "Invokes Lambda functions safely for testing.",
            "artifact_type": "Compute",
            "aws_service": "AWS Lambda",
            "cost": 20,
            "power": 2
        }

        self.artifacts["ECS Orchestrator"] = {
            "name": "ECS Orchestrator",
            "description": "Controls container deployments and scaling.",
            "artifact_type": "Compute",
            "aws_service": "Amazon ECS",
            "cost": 35,
            "power": 3
        }

        # Storage Artifacts
        self.artifacts["Glacier Drill"] = {
            "name": "Glacier Drill",
            "description": "Retrieves archived data from Glacier storage.",
            "artifact_type": "Storage",
            "aws_service": "Amazon S3 Glacier",
            "cost": 30,
            "power": 3
        }

        self.artifacts["EFS Mount"] = {
            "name": "EFS Mount",
            "description": "Mounts shared file systems for data analysis.",
            "artifact_type": "Storage",
            "aws_service": "Amazon EFS",
            "cost": 25,
            "power": 2
        }

        # Database Artifacts
        self.artifacts["DynamoDB Query Engine"] = {
            "name": "DynamoDB Query Engine",
            "description": "Performs complex queries on NoSQL data.",
            "artifact_type": "Database",
            "aws_service": "Amazon DynamoDB",
            "cost": 35,
            "power": 3
        }

        self.artifacts["Aurora Analyzer"] = {
            "name": "Aurora Analyzer",
            "description": "Analyzes and optimizes Aurora databases.",
            "artifact_type": "Database",
            "aws_service": "Amazon Aurora",
            "cost": 45,
            "power": 4
        }

        # Legendary Artifacts
        self.artifacts["CloudFormation Architect"] = {
            "name": "CloudFormation Architect",
            "description": "Reverse engineers cloud infrastructure and creates templates.",
            "artifact_type": "IaC",
            "aws_service": "AWS CloudFormation",
            "cost": 100,
            "power": 8
        }

        self.artifacts["Console Master Key"] = {
            "name": "Console Master Key",
            "description": "Grants elevated access to AWS console functions.",
            "artifact_type": "Security",
            "aws_service": "AWS Management Console",
            "cost": 150,
            "power": 9
        }

        self.artifacts["Quantum Decryptor"] = {
            "name": "Quantum Decryptor",
            "description": "Uses quantum computing to break encryption.",
            "artifact_type": "Security",
            "aws_service": "AWS Key Management Service",
            "cost": 200,
            "power": 10
        }

        # --- NEW ARTIFACTS --- #

        # More Troubleshooting/Security Tools
        self.artifacts["VPC Flow Log Analyzer"] = {
            "name": "VPC Flow Log Analyzer",
            "description": "Analyzes VPC flow logs to trace network connections and detect anomalies.",
            "artifact_type": "Network",  # Could also be Security
            "aws_service": "Amazon VPC",
            "cost": 45,
            "power": 5
        }

        self.artifacts["CloudWatch Metrics Dashboard"] = {
            "name": "CloudWatch Metrics Dashboard",
            "description": "Visualizes CloudWatch metrics to diagnose performance issues and resource utilization.",
            "artifact_type": "Monitoring",  # New type, or maybe 'Cloud'
            "aws_service": "Amazon CloudWatch",
            "cost": 40,
            "power": 4
        }

        self.artifacts["IAM Access Analyzer"] = {
            "name": "IAM Access Analyzer",
            "description": "Identifies unintended resource access and validates security policies.",
            "artifact_type": "Security",
            "aws_service": "AWS IAM Access Analyzer",
            "cost": 55,
            "power": 6
        }

        # Log Analysis Tool
        self.artifacts["Log Analyzer Toolkit"] = {
            "name": "Log Analyzer Toolkit",
            "description": "A suite of tools for parsing and analyzing various system and application logs.",
            "artifact_type": "Investigation",  # New type, or 'Tool'
            "aws_service": None,  # Not tied to a specific AWS service
            "cost": 30,
            "power": 3
        }

        # New battle artifacts
        self.artifacts["Digital Shield Generator"] = {
            "name": "Digital Shield Generator",
            "description": "Creates a protective barrier against digital attacks.",
            "artifact_type": "Defense",
            "aws_service": "AWS Shield Advanced",
            "cost": 75,
            "power": 7
        }

        self.artifacts["Network Pulse Emitter"] = {
            "name": "Network Pulse Emitter",
            "description": "Disrupts hostile connections and network intrusions.",
            "artifact_type": "Offense",
            "aws_service": "AWS Network Firewall",
            "cost": 80,
            "power": 7
        }

        self.artifacts["Vulnerability Scanner Pro"] = {
            "name": "Vulnerability Scanner Pro",
            "description": "Advanced scanning tool that identifies system weaknesses.",
            "artifact_type": "Scanner",
            "aws_service": "Amazon Inspector",
            "cost": 65,
            "power": 6
        }

        # Recovery artifacts
        self.artifacts["Backup & Restore Module"] = {
            "name": "Backup & Restore Module",
            "description": "Quickly restores service health from backup snapshots.",
            "artifact_type": "Recovery",
            "aws_service": "AWS Backup",
            "cost": 50,
            "power": 5
        }

    def _create_services(self):
        """Create service templates."""
        # Compute Services
        self.services["EC2 Instance"] = {
            "name": "EC2 Instance",
            "description": "Virtual server in the cloud.",
            "service_type": "Compute",
            "cost_per_hour": 0.10,
            "deploy_cost": 5,
            "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
            "dependencies": []
        }

        self.services["Lambda Function"] = {
            "name": "Lambda Function",
            "description": "Serverless compute service.",
            "service_type": "Compute",
            "cost_per_hour": 0.01,
            "deploy_cost": 2,
            "region_availability": ["us-east-1", "us-west-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
            "dependencies": []
        }

        # Storage Services
        self.services["S3 Bucket"] = {
            "name": "S3 Bucket",
            "description": "Object storage service.",
            "service_type": "Storage",
            "cost_per_hour": 0.02,
            "deploy_cost": 1,
            "region_availability": ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1", "ap-northeast-1"],
            "dependencies": []
        }

        self.services["EBS Volume"] = {
            "name": "EBS Volume",
            "description": "Block storage for EC2 instances.",
            "service_type": "Storage",
            "cost_per_hour": 0.08,
            "deploy_cost": 3,
            "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
            "dependencies": ["EC2 Instance"]
        }

        # Database Services
        self.services["RDS Database"] = {
            "name": "RDS Database",
            "description": "Relational database service.",
            "service_type": "Database",
            "cost_per_hour": 0.20,
            "deploy_cost": 15,
            "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1"],
            "dependencies": ["VPC"]
        }

        self.services["DynamoDB Table"] = {
            "name": "DynamoDB Table",
            "description": "NoSQL database service.",
            "service_type": "Database",
            "cost_per_hour": 0.15,
            "deploy_cost": 8,
            "region_availability": ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1", "ap-northeast-1"],
            "dependencies": []
        }

        # Network Services
        self.services["VPC"] = {
            "name": "VPC",
            "description": "Virtual private cloud network.",
            "service_type": "Network",
            "cost_per_hour": 0.01,
            "deploy_cost": 5,
            "region_availability": ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1", "ap-northeast-1"],
            "dependencies": []
        }

        self.services["API Gateway"] = {
            "name": "API Gateway",
            "description": "API creation and management service.",
            "service_type": "Network",
            "cost_per_hour": 0.12,
            "deploy_cost": 7,
            "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
            "dependencies": []
        }

        # Security Services
        self.services["IAM Policy"] = {
            "name": "IAM Policy",
            "description": "Identity and access management.",
            "service_type": "Security",
            "cost_per_hour": 0.00,
            "deploy_cost": 0,
            "region_availability": ["global"],
            "dependencies": []
        }

        self.services["Security Group"] = {
            "name": "Security Group",
            "description": "Virtual firewall for services.",
            "service_type": "Security",
            "cost_per_hour": 0.00,
            "deploy_cost": 0,
            "region_availability": ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1", "ap-northeast-1"],
            "dependencies": ["VPC"]
        }

        # New high-level services
        self.services["Elastic Kubernetes Service"] = {
            "name": "Elastic Kubernetes Service",
            "description": "Managed Kubernetes service for container orchestration.",
            "service_type": "Compute",
            "cost_per_hour": 0.30,
            "deploy_cost": 25,
            "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
            "dependencies": ["VPC"]
        }

        self.services["SageMaker Instance"] = {
            "name": "SageMaker Instance",
            "description": "Managed machine learning service.",
            "service_type": "AI/ML",
            "cost_per_hour": 0.50,
            "deploy_cost": 35,
            "region_availability": ["us-east-1", "us-west-2", "eu-west-1"],
            "dependencies": ["S3 Bucket"]
        }

        self.services["CloudFront Distribution"] = {
            "name": "CloudFront Distribution",
            "description": "Content delivery network service.",
            "service_type": "Network",
            "cost_per_hour": 0.10,
            "deploy_cost": 12,
            "region_availability": ["global"],
            "dependencies": ["S3 Bucket"]
        }

        self.services["Elastic Load Balancer"] = {
            "name": "Elastic Load Balancer",
            "description": "Automatically distributes traffic across multiple targets.",
            "service_type": "Network",
            "cost_per_hour": 0.08,
            "deploy_cost": 10,
            "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
            "dependencies": ["VPC", "EC2 Instance"]
        }

    def _create_quests(self):
        """Create game quests."""
        # Tutorial Quest
        self.quests["tutorial"] = Quest(
            id="tutorial",
            title="Cloud Ranger Training",
            description="Complete basic training to become a certified Cloud Ranger.",
            objectives=[
                {"id": "tutorial_1", "description": "Visit Cloud City",
                    "completed": False},
                {"id": "tutorial_2", "description": "Acquire your first artifact",
                    "completed": False},
                {"id": "tutorial_3", "description": "Deploy your first service",
                    "completed": False}
            ],
            reward={
                "credits": 50,
                "faction_rep": {"CorpSec": 5}
            }
        )

        # Main Story Quests
        self.quests["mysterious_outage"] = Quest(
            id="mysterious_outage",
            title="The Mysterious Outage",
            description="Investigate a service outage reported in the Database District.",
            objectives=[
                {"id": "outage_1", "description": "Visit Database District",
                    "completed": False},
                {"id": "outage_2", "description": "Scan the affected RDS instance",
                    "completed": False},
                {"id": "outage_3", "description": "Find evidence of the attack",
                    "completed": False},
                {"id": "outage_4", "description": "Report your findings to Security Perimeter",
                    "completed": False}
            ],
            # Continuing from the mysterious_outage quest reward
            reward={
                "credits": 100,
                "skill": {"investigation": 1, "security": 1},
                "faction_rep": {"CorpSec": 10}
            }
        )

        self.quests["shadow_admin"] = Quest(
            id="shadow_admin",
            title="Trail of the Shadow Admin",
            description="Follow the clues left by the mysterious Shadow Admin who seems to be behind recent incidents.",
            objectives=[
                {"id": "shadow_1", "description": "Collect all Shadow Admin clues",
                    "completed": False},
                {"id": "shadow_2", "description": "Decrypt the secret message",
                    "completed": False},
                {"id": "shadow_3", "description": "Find the Shadow Admin's hidden access point",
                    "completed": False},
                {"id": "shadow_4", "description": "Confront the Shadow Admin",
                    "completed": False}
            ],
            reward={
                "credits": 500,
                "artifacts": ["Console Master Key"],
                "skill": {"security": 3, "cloud": 3},
                "faction_rep": {"CorpSec": 15, "ShadowNetwork": -10}
            }
        )

        # Side Quests
        self.quests["data_recovery"] = Quest(
            id="data_recovery",
            title="Critical Data Recovery",
            description="Help recover crucial data from a failed database cluster in Cache Cove.",
            objectives=[
                {"id": "recovery_1", "description": "Travel to Cache Cove",
                    "completed": False},
                {"id": "recovery_2", "description": "Assess database damage",
                    "completed": False},
                {"id": "recovery_3", "description": "Deploy RDS with recovery mode",
                    "completed": False},
                {"id": "recovery_4", "description": "Restore data from backup",
                    "completed": False}
            ],
            reward={
                "credits": 150,
                "artifacts": ["Aurora Analyzer"],
                "skill": {"database": 2},
                "faction_rep": {"DataBrokers": 10}
            }
        )

        self.quests["serverless_pioneer"] = Quest(
            id="serverless_pioneer",
            title="Serverless Pioneer",
            description="Master serverless technologies by completing a series of challenges in Serverless Valley.",
            objectives=[
                {"id": "serverless_1",
                    "description": "Deploy 3 Lambda functions", "completed": False},
                {"id": "serverless_2",
                    "description": "Create API Gateway endpoints", "completed": False},
                {"id": "serverless_3",
                    "description": "Set up event-driven architecture", "completed": False},
                {"id": "serverless_4",
                    "description": "Complete the Serverless Challenge", "completed": False}
            ],
            reward={
                "credits": 200,
                "artifacts": ["Lambda Invoker"],
                "skill": {"serverless": 3, "cloud": 1},
                "faction_rep": {"ServerlessCollective": 15}
            }
        )

        self.quests["secure_the_perimeter"] = Quest(
            id="secure_the_perimeter",
            title="Secure the Perimeter",
            description="Help strengthen Cloud City's security by addressing vulnerabilities in Security Perimeter.",
            objectives=[
                {"id": "secure_1", "description": "Audit IAM policies",
                    "completed": False},
                {"id": "secure_2", "description": "Configure Security Groups",
                    "completed": False},
                {"id": "secure_3", "description": "Deploy WAF rules", "completed": False},
                {"id": "secure_4", "description": "Test security with penetration test",
                    "completed": False}
            ],
            reward={
                "credits": 175,
                "artifacts": ["IAM Auditor"],
                "skill": {"security": 2, "network": 1},
                "faction_rep": {"CorpSec": 12}
            }
        )

        # New advanced quests
        self.quests["shadow_network_infiltration"] = Quest(
            id="shadow_network_infiltration",
            title="Shadow Network Infiltration",
            description="Gain the trust of the Shadow Network by completing a series of covert operations.",
            objectives=[
                {"id": "infiltrate_1", "description": "Meet the Shadow Network contact in Blockchain Bazaar",
                    "completed": False},
                {"id": "infiltrate_2", "description": "Complete a test mission to prove your skills",
                    "completed": False},
                {"id": "infiltrate_3", "description": "Extract data from a secure facility",
                    "completed": False},
                {"id": "infiltrate_4", "description": "Deliver the data to gain Shadow Network trust",
                    "completed": False}
            ],
            reward={
                "credits": 300,
                "artifacts": ["Vulnerability Scanner Pro"],
                "skill": {"security": 2, "investigation": 2},
                "faction_rep": {"ShadowNetwork": 20, "CorpSec": -10}
            },
            min_skill_level={"security": 5, "investigation": 4},
            min_faction_rep={"ShadowNetwork": 20},
            difficulty=7
        )

        self.quests["quantum_algorithm"] = Quest(
            id="quantum_algorithm",
            title="The Quantum Algorithm",
            description="Develop a quantum computing algorithm in the Quantum Quarry to break an unbreakable cipher.",
            objectives=[
                {"id": "quantum_1", "description": "Study quantum computing principles",
                    "completed": False},
                {"id": "quantum_2", "description": "Gather quantum computing resources",
                    "completed": False},
                {"id": "quantum_3", "description": "Develop the algorithm prototype",
                    "completed": False},
                {"id": "quantum_4", "description": "Test the algorithm against the cipher",
                    "completed": False}
            ],
            reward={
                "credits": 400,
                "artifacts": ["Quantum Decryptor"],
                "skill": {"cloud": 3, "security": 2},
                "faction_rep": {"DataBrokers": 15, "ServerlessCollective": 10}
            },
            min_skill_level={"cloud": 6},
            difficulty=9
        )

    def _create_events(self):
        """Create game events."""
        # Tutorial Events
        self.events["welcome_to_cloud_city"] = CloudEvent(
            id="welcome_to_cloud_city",
            name="Welcome to Cloud City",
            description="As you arrive in Cloud City, a veteran Cloud Ranger greets you and offers guidance.",
            event_type="tutorial",
            effects={
                "credits": 25,
                "clue": "The Cloud Rangers protect the digital infrastructure from threats.",
                "faction_rep": {"CorpSec": 2}
            },
            chance=100,
            repeatable=False
        )

        self.events["artifact_discovery"] = CloudEvent(
            id="artifact_discovery",
            name="First Artifact Discovery",
            description="You stumble upon a discarded S3 Scanner. It seems functional after some minor repairs.",
            event_type="discovery",
            effects={
                "artifact": self.artifacts["S3 Scanner"]
            },
            chance=100,
            repeatable=False
        )

        # Location-specific Events
        self.events["database_breach"] = CloudEvent(
            id="database_breach",
            name="Database Breach",
            description="You discover signs of unauthorized access to a critical database cluster.",
            event_type="encounter",
            effects={
                "skill": {"security": 1, "investigation": 1},
                "clue": "The intruder used a sophisticated SQL injection technique.",
                "faction_rep": {"CorpSec": -3, "ShadowNetwork": 2}
            },
            requirements={
                "min_skill": {"investigation": 1}
            },
            chance=75
        )

        self.events["serverless_challenge"] = CloudEvent(
            id="serverless_challenge",
            name="Serverless Challenge",
            description="A group of developers invites you to participate in their serverless architecture contest.",
            event_type="challenge",
            effects={
                "credits": 50,
                "skill": {"serverless": 1, "cloud": 1},
                "faction_rep": {"ServerlessCollective": 5}
            },
            chance=60
        )

        self.events["network_storm"] = CloudEvent(
            id="network_storm",
            name="Network Storm",
            description="A sudden surge in network traffic creates chaos. Your quick response helps maintain stability.",
            event_type="disaster",
            effects={
                "skill": {"network": 1},
                "faction_rep": {"CorpSec": 3}
            },
            chance=40
        )

        # Shadow Admin Events
        self.events["shadow_admin_message"] = CloudEvent(
            id="shadow_admin_message",
            name="Message from the Shadow",
            description="You find a cryptic message on a terminal: 'Not all services are what they seem. Look deeper.'",
            event_type="discovery",
            effects={
                "clue": "The Shadow Admin leaves cryptic messages on compromised systems.",
                "faction_rep": {"ShadowNetwork": 1}
            },
            chance=30
        )

        self.events["admin_sighting"] = CloudEvent(
            id="admin_sighting",
            name="Shadow Admin Sighting",
            description="You catch a glimpse of a hooded figure disappearing into the digital void, leaving traces of advanced code.",
            event_type="encounter",
            effects={
                "skill": {"investigation": 1},
                "clue": "The Shadow Admin uses custom tools to move through the cloud undetected.",
                "faction_rep": {"ShadowNetwork": 2, "CorpSec": -1}
            },
            requirements={
                "min_skill": {"investigation": 2}
            },
            chance=20
        )

        # Rare Events
        self.events["quantum_fluctuation"] = CloudEvent(
            id="quantum_fluctuation",
            name="Quantum Fluctuation",
            description="A strange quantum fluctuation occurs, temporarily enhancing your abilities.",
            event_type="phenomenon",
            effects={
                "skill": {"cloud": 1, "security": 1, "networking": 1},
                "time": 1,
                "faction_rep": {random.choice(["CorpSec", "DataBrokers", "ServerlessCollective"]): 1}
            },
            chance=10
        )

        self.events["legendary_artifact"] = CloudEvent(
            id="legendary_artifact",
            name="Legendary Artifact Discovery",
            description="Hidden in an encrypted data vault, you discover plans for a legendary CloudFormation Architect.",
            event_type="discovery",
            effects={
                "artifact": self.artifacts["CloudFormation Architect"]
            },
            requirements={
                "min_skill": {"investigation": 5}
            },
            chance=5
        )

        # New events with health/energy effects
        self.events["digital_virus"] = CloudEvent(
            id="digital_virus",
            name="Digital Virus Exposure",
            description="You encounter a malicious piece of code that attempts to infect your systems.",
            event_type="hazard",
            effects={
                "health": -15,
                "status_effect": {
                    "name": "Digital Infection",
                    "duration": 3,
                    "per_turn_effect": lambda player: player.take_damage(5, "virus")
                }
            },
            requirements={
                # Chance to avoid with security skill
                "min_skill": {"security": 3}
            },
            chance=30,
            repeatable=True,
            cooldown_duration=5
        )

        self.events["energy_surge"] = CloudEvent(
            id="energy_surge",
            name="Energy Grid Surge",
            description="A power surge in the system temporarily boosts your energy reserves.",
            event_type="beneficial",
            effects={
                "energy": 30,
                "credits": 15
            },
            chance=25,
            repeatable=True,
            cooldown_duration=7
        )

        self.events["emergency_supplies"] = CloudEvent(
            id="emergency_supplies",
            name="Emergency Supply Cache",
            description="You discover a hidden cache of emergency supplies.",
            event_type="discovery",
            effects={
                "health": 20,
                "energy": 20,
                "consumable": {
                    "name": "Emergency Patch",
                    "count": 2
                }
            },
            chance=20,
            repeatable=True,
            cooldown_duration=10
        )

        # Global events that can happen anywhere
        self.events["system_update"] = CloudEvent(
            id="system_update",
            name="System-Wide Update",
            description="A major update is being rolled out across all AWS services, causing temporary disruption.",
            event_type="global",
            effects={
                "credits": -20,
                "time": -1,
                "status_effect": {
                    "name": "System Lag",
                    "duration": 2,
                    "per_turn_effect": lambda player: player.use_energy(5)
                }
            },
            chance=15,
            repeatable=True,
            cooldown_duration=20
        )

        self.events["cloud_conference"] = CloudEvent(
            id="cloud_conference",
            name="Cloud Tech Conference",
            description="A major cloud technology conference is happening. Attend to learn new skills and make connections.",
            event_type="opportunity",
            effects={
                "credits": -50,  # Cost to attend
                "skill": {"cloud": 1, "networking": 1},
                "faction_rep": {"CorpSec": 3, "ServerlessCollective": 3, "DataBrokers": 3}
            },
            chance=10,
            repeatable=False
        )

    def start_game(self):
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
            self.player.active_quests.append(tutorial_quest)
        else:
            print(f"{CLR_WARNING}Warning: Tutorial quest not found!{CLR_RESET}")

        # Set game parameters based on difficulty
        if self.difficulty == "easy":
            self.player.cloud_credits = 750
            self.player.time_left = 400
            s3_scanner_data = self.artifacts.get("S3 Scanner")
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

    def game_loop(self):
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

    def update_game_state(self):
        """Update game state at the beginning of each turn."""
        if not self.player or self.game_over:
            return

        self.current_day += 1  # Advance time first
        # print(f"\n--- Day {self.current_day} --- ") # Optional Debug

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
                income_str = f"{CLR_BONUS}+{net_change:.2f}{CLR_RESET}" if net_change > 0 else f"{CLR_HAZARD}{net_change:.2f}{CLR_RESET}"
                # Optional: Display daily net, can be spammy
                # display_notification(f"Daily Service Net: {income_str} Credits", "info")

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

    def update_weather(self):
        """Update weather conditions across all locations."""
        for loc_name, weather in self.weather_conditions.items():
            # Decrease duration counter
            weather["duration"] -= 1

            # Change weather if duration expired
            if weather["duration"] <= 0:
                weather_types = [
                    {"name": "Data Storm", "effect": "Bandwidth -20%",
                        "description": "A storm of corrupted data packets"},
                    {"name": "Processing Fog", "effect": "Investigation -2",
                        "description": "Dense fog reducing visibility"},
                    {"name": "CPU Heatwave", "effect": "Energy -10%",
                        "description": "Extreme computational heat"},
                    {"name": "Memory Frost", "effect": "Service performance -2",
                        "description": "Cold conditions slowing memory access"},
                    {"name": "Clear Signals", "effect": "All stats +5%",
                        "description": "Perfect conditions with clear connections"}
                ]

                # Select new weather condition
                weather["current"] = random.choice(weather_types)
                weather["duration"] = random.randint(2, 5)

                # If this is the player's current location, notify them of the change
                if self.player and self.player.current_location and self.player.current_location.name == loc_name:
                    display_notification(
                        f"Weather changed to: {weather['current']['name']} - {weather['current']['effect']}",
                        "info")

    def check_hazards(self):
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
                damage_func = hazard.get("damage", lambda: 10)
                damage = damage_func() if callable(damage_func) else damage_func

                display_notification(
                    f"Hazard encountered: {hazard['name']} - {hazard['description']}",
                    "warning")

                self.player.take_damage(damage, hazard['name'])

                # Possible status effect from hazard
                if "status_effect" in hazard:
                    self.player.add_status_effect(hazard["status_effect"])

                break  # Only one hazard per turn for balance

    def check_quest_progress(self):
        """Check and update quest progress."""
        if not self.player:
            return

        # Check each active quest
        for quest in self.player.active_quests:
            if isinstance(quest, str):
                # If quest is stored as ID string, get the quest object
                if quest in self.quests:
                    quest_obj = self.quests[quest]
                else:
                    continue  # Skip if quest not found
            else:
                quest_obj = quest

            # Auto-complete location-based objectives
            current_loc = self.player.current_location.name if self.player.current_location else None

            # Tutorial quest special handling
            if quest_obj.id == "tutorial":
                # Check if player visited Cloud City
                if current_loc == "Cloud City" and not quest_obj.objectives[0]["completed"]:
                    quest_obj.objectives[0]["completed"] = True
                    display_notification(
                        "Tutorial Objective Completed: Visit Cloud City", "success")

                # Check if player has acquired an artifact
                if len(self.player.inventory.artifacts) > 0 and not quest_obj.objectives[1]["completed"]:
                    quest_obj.objectives[1]["completed"] = True
                    display_notification(
                        "Tutorial Objective Completed: Acquire your first artifact", "success")

                # Check if player has deployed a service
                if len(self.player.inventory.deployed_services) > 0 and not quest_obj.objectives[2]["completed"]:
                    quest_obj.objectives[2]["completed"] = True
                    display_notification(
                        "Tutorial Objective Completed: Deploy your first service", "success")

            # Mysterious outage quest special handling
            elif quest_obj.id == "mysterious_outage":
                # Check if player visited Database District
                if current_loc == "Database District" and not quest_obj.objectives[0]["completed"]:
                    quest_obj.objectives[0]["completed"] = True
                    display_notification(
                        "Objective Completed: Visit Database District", "success")

                # Check if player reported findings at Security Perimeter
                if current_loc == "Security Perimeter" and quest_obj.objectives[2]["completed"] and not quest_obj.objectives[3]["completed"]:
                    quest_obj.objectives[3]["completed"] = True
                    display_notification(
                        "Objective Completed: Report your findings to Security Perimeter", "success")

            # Check if all objectives are completed
            if all(obj["completed"] for obj in quest_obj.objectives):
                self.complete_quest(quest_obj)

    def complete_quest(self, quest):
        """Complete a quest and give rewards."""
        if not self.player:
            return

        # If quest is string ID, get the quest object
        if isinstance(quest, str):
            if quest in self.quests:
                quest = self.quests[quest]
            else:
                return  # Quest not found

        # Mark quest as completed
        if quest.id in self.player.active_quests:
            self.player.active_quests.remove(quest.id)
        elif quest in self.player.active_quests:
            self.player.active_quests.remove(quest)

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

    def _trigger_service_event(self, service):
        """Triggers a random negative event on a deployed service."""
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

    def display_status(self):
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

        # The player's full status (skills, rep, inventory) is displayed
        # by calling self.player.display_status() in the game loop.

    def display_actions(self):
        """Display available actions to the player."""
        print(f"\n{CLR_INTERACTION}Available Actions:{CLR_RESET}")
        print("1. Explore Location")
        print("2. Travel")
        print("3. View Quests")
        print("4. View Inventory/Status")
        print("5. Manage Services")
        print("6. Use Artifact")
        print("7. Rest (skip day)")
        print("8. Interact with Vendors")
        print("9. System Menu (Save/Quit)")

    def get_player_action(self):
        """Get player's chosen action."""
        return get_valid_input("\nEnter your choice (1-9): ", range(1, 10))

    def process_action(self, choice):
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

    def explore_location(self):
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
                # Find a random artifact
                # Higher difficulty locations have better artifacts
                if location_difficulty >= 7:
                    possible_artifacts = [
                        a for a in self.artifacts.keys() if self.artifacts[a]["power"] >= 6]
                elif location_difficulty >= 4:
                    possible_artifacts = [a for a in self.artifacts.keys(
                    ) if 3 <= self.artifacts[a]["power"] <= 7]
                else:
                    possible_artifacts = [
                        a for a in self.artifacts.keys() if self.artifacts[a]["power"] <= 4]

                if possible_artifacts:
                    artifact_name = random.choice(possible_artifacts)
                    artifact_data = self.artifacts[artifact_name]

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
                for svc_name, svc_data in self.services.items():
                    # Check if service is appropriate for location difficulty
                    if (location_difficulty <= 3 and svc_data["deploy_cost"] <= 10) or \
                        (4 <= location_difficulty <= 6 and 5 <= svc_data["deploy_cost"] <= 20) or \
                            (location_difficulty >= 7 and svc_data["deploy_cost"] >= 15):
                        # Check if service is available in this region
                        if "global" in svc_data["region_availability"] or \
                                (self.player.current_location.region in svc_data["region_availability"]):
                            service_candidates.append(svc_name)

                if service_candidates:
                    service_name = random.choice(service_candidates)
                    service_data = self.services[service_name]

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

    def travel(self):
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

    def view_quests(self):
        """View active and available quests."""
        print(f"\n{CLR_SECTION}[ACTIVE QUESTS]{CLR_RESET}")

        active_quests = []
        for quest_id in self.player.active_quests:
            if isinstance(quest_id, str) and quest_id in self.quests:
                active_quests.append(self.quests[quest_id])
            elif not isinstance(quest_id, str):
                active_quests.append(quest_id)

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

    def manage_services(self):
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

    def deploy_service(self):
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

        self.player.inventory.deployed_services.append(deployed_service)
        self.player.inventory.services.remove(selected_service)

        display_loading_bar("Deploying service...", 1.5)
        display_notification(
            f"Successfully deployed {deployed_service.name} ({deployed_service.instance_id}) in {current_region}!", "success")

        # Deployment takes time
        self.current_day += 1
        input("\nPress Enter to continue...")

    def manage_deployed_services(self):
        """Manage already deployed services."""
        if not self.player.inventory.deployed_services:
            print("\nYou don't have any deployed services to manage.")
            input("\nPress Enter to continue...")
            return

        while True:
            print(f"\n{CLR_SECTION}[MANAGE DEPLOYED SERVICES]{CLR_RESET}")

            # Display deployed services
            for i, service in enumerate(self.player.inventory.deployed_services, 1):
                status = f"{CLR_GREEN}ONLINE{CLR_RESET}" if service.is_deployed else f"{CLR_RED}OFFLINE{CLR_RESET}"
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

    def service_action_menu(self, service):
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

    def view_service_analytics(self):
        """View analytics for deployed services."""
        if not self.player.inventory.deployed_services:
            print("\nYou don't have any deployed services to analyze.")
            input("\nPress Enter to continue...")
            return

        print(f"\n{CLR_SECTION}[SERVICE ANALYTICS]{CLR_RESET}")

        # Calculate total revenue, costs
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
    print(f"\n{CLR_CLOUD_SERVICE}Summary Statistics:{CLR_RESET}")
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

        print(f"\n{CLR_CLOUD_SERVICE}Performance Metrics:{CLR_RESET}")
        print(f"Average Health: {avg_health:.1f}%")
        print(f"Average Security Level: {avg_security:.1f}/10")
        print(f"Average Performance: {avg_performance:.1f}/10")

        # Distribution by region
        print(f"\n{CLR_CLOUD_SERVICE}Regional Distribution:{CLR_RESET}")
        for region, count in services_by_region.items():
            print(f"{region}: {count} services ({count/active_services*100:.1f}%)")

        # Distribution by service type
        print(f"\n{CLR_CLOUD_SERVICE}Service Type Distribution:{CLR_RESET}")
        for svc_type, count in services_by_type.items():
            print(f"{svc_type}: {count} services ({count/active_services*100:.1f}%)")

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

    def use_artifact(self):
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

    def use_scanner_artifact(self, artifact):
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

    def use_security_artifact(self, artifact):
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

    def use_network_artifact(self, artifact):
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

    def use_recovery_artifact(self, artifact):
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

    def use_database_artifact(self, artifact):
        """Use a database-type artifact."""
        display_loading_bar(f"Querying with {artifact.name}", 1.5)

        db_power = artifact.power + artifact.upgrade_level

        # Database artifacts are good for analysis, gaining knowledge, finding clues
        intelligence_gain = db_power * 5
        credits_gain = db_power * 15

        # Generate some random insights
        print(f"\n{CLR_CLOUD_SERVICE}Database analysis complete!{CLR_RESET}")

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

    def rest(self):
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

    def trigger_random_event(self):
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
            print_slow(dream_text, color=CLR_BRIGHT + CLR_BLUE)

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

    def interact_with_vendors(self):
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

    def vendor_menu(self, vendor):
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

    def buy_artifacts(self, vendor):
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

    def buy_services(self, vendor):
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

    def buy_consumables(self, vendor):
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

    def sell_items(self, vendor):
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

    def sell_artifacts(self, vendor):
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

    def sell_services(self, vendor):
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

    def system_menu(self):
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

    def game_options(self):
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

    def view_help(self):
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
            print(f"\n{CLR_TUTORIAL}Basic Controls:{CLR_RESET}")
            print("- Use number keys to navigate menus and make choices.")
            print("- Explore locations to find resources and advance the story.")
            print("- Travel between locations to discover new areas.")
            print("- Manage your services to generate income.")
            print("- Use artifacts to gain advantages and uncover secrets.")
            print("- Complete quests to gain rewards and advance the storyline.")
        elif choice == 2:
            print(f"\n{CLR_TUTORIAL}Combat:{CLR_RESET}")
            print("- Combat occurs when facing digital threats or hostile entities.")
            print("- Use your artifacts as weapons and defenses.")
            print("- Different threats are vulnerable to different artifacts.")
            print("- Your skills affect your combat effectiveness.")
            print(
                "- Health is depleted during combat - restore it by resting or using items.")
        elif choice == 3:
            print(f"\n{CLR_TUTORIAL}Services & Artifacts:{CLR_RESET}")
            print("- Services generate passive income when deployed.")
            print("- Services can be damaged and require maintenance.")
            print("- Artifacts are tools that provide special abilities.")
            print("- Artifacts have cooldowns after use.")
            print("- Some artifacts can be upgraded to increase their effectiveness.")
        elif choice == 4:
            print(f"\n{CLR_TUTORIAL}Factions & Reputation:{CLR_RESET}")
            print("- CorpSec: Corporate security forces maintaining order.")
            print("- DataBrokers: Information traders and database specialists.")
            print(
                "- ServerlessCollective: Progressive cloud engineers focused on serverless tech.")
            print(
                "- ShadowNetwork: Underground network of hackers with mysterious motives.")
            print("- Higher reputation grants access to better quests and vendors.")

        input("\nPress Enter to continue...")

    def show_credits(self):
        """Show game credits."""
        print(f"\n{CLR_SECTION}[CREDITS]{CLR_RESET}")
        print("Cloud Ranger: Digital Frontier")
        print("\nDeveloped by:")
        print("- Simulated by Claude AI")
        print("\nSpecial thanks to:")
        print("- AWS for cloud inspiration")
        print("- Text-based adventure games everywhere")

        input("\nPress Enter to continue...")

    def check_events(self):
        """Check for events at the current location."""
        if not self.player or not self.player.current_location:
            return

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

    def check_game_over(self):
        """Check win/lose conditions."""
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

    def end_game(self):
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

    def get_valid_input(prompt, valid_range):
        """Get user input within a valid range."""
        while True:
            try:
                user_input = input(prompt)
                value = int(user_input)
                if value in valid_range:
                    return value
                else:
                    print(
                        f"{CLR_ERROR}Please enter a number between {min(valid_range)} and {max(valid_range)}{CLR_RESET}")
            except ValueError:
                print(f"{CLR_ERROR}Please enter a valid number{CLR_RESET}")

    def view_service_analytics(self):
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
        print(f"\n{CLR_CLOUD_SERVICE}Summary Statistics:{CLR_RESET}")
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

            print(f"\n{CLR_CLOUD_SERVICE}Performance Metrics:{CLR_RESET}")
            print(f"Average Health: {avg_health:.1f}%")
            print(f"Average Security Level: {avg_security:.1f}/10")
            print(f"Average Performance: {avg_performance:.1f}/10")

            # Distribution by region
            print(f"\n{CLR_CLOUD_SERVICE}Regional Distribution:{CLR_RESET}")
            for region, count in services_by_region.items():
                print(
                    f"{region}: {count} services ({count/active_services*100:.1f}%)")

            # Distribution by service type
            print(f"\n{CLR_CLOUD_SERVICE}Service Type Distribution:{CLR_RESET}")
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
            most_profitable = max(
                [s for s in self.player.inventory.deployed_services if s.is_deployed],
                key=lambda s: s.calculate_revenue() - s.cost_per_hour
            )

            profit = most_profitable.calculate_revenue() - most_profitable.cost_per_hour
            print(f"\n{CLR_BONUS}Most Profitable Service:{CLR_RESET}")
            print(
                f"{most_profitable.name} ({most_profitable.instance_id[:6]}): {profit:.2f} credits/hour")

        input("\nPress Enter to continue...")

    def use_artifact(self):
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

    def rest(self):
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

    def interact_with_vendors(self):
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

    def system_menu(self):
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

    def check_events(self):
        """Check for events at the current location."""
        if not self.player or not self.player.current_location:
            return

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

    def check_game_over(self):
        """Check win/lose conditions."""
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

    def end_game(self):
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

    def get_valid_input(prompt, valid_range):
        """Get user input within a valid range."""
        while True:
            try:
                user_input = input(prompt)
                value = int(user_input)
                if value in valid_range:
                    return value
                else:
                    print(
                        f"{CLR_ERROR}Please enter a number between {min(valid_range)} and {max(valid_range)}{CLR_RESET}")
            except ValueError:
                print(f"{CLR_ERROR}Please enter a valid number{CLR_RESET}")

    def trigger_random_event(self):
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
            "You dream of vast data centers, humming with activity. In the dream, you understand how they're all connected.",
            "In your dream, the Shadow Admin speaks to you directly, but their words fade as you wake.",
            "You dream of code flowing like rivers, and for a moment, you see patterns that weren't clear before.",
            "A dream of serverless functions dancing across cloud formations gives you new insights."
        ]

        dream = random.choice(dreams)
        print_slow(dream, color=CLR_SHADOW_ADMIN)

        # Dreams provide small skill boosts
        skill = random.choice(list(self.player.skills.keys()))
        self.player.increase_skill(skill, 1)

        # Sometimes dreams reveal clues
        if random.randint(1, 100) <= 25:  # 25% chance
            clue_id = f"dream_clue_{random.randint(1000, 9999)}"
            self.player.add_clue(clue_id)
            print(
                f"{CLR_CLUE}The dream seems to have revealed something important...{CLR_RESET}")

    def game_options(self):
        """Display and modify game options."""
        print(f"\n{CLR_SECTION}[GAME OPTIONS]{CLR_RESET}")
        print(f"1. Difficulty: {self.difficulty}")
        print("2. Toggle Debug Mode:", "ON" if self.debug_mode else "OFF")
        print("3. Return")

        choice = get_valid_input("Enter your choice: ", range(1, 4))

        if choice == 1:
            print("\nSelect difficulty:")
            print("1. Easy")
            print("2. Normal")
            print("3. Hard")

            diff_choice = get_valid_input("Enter choice: ", range(1, 4))

            if diff_choice == 1:
                self.difficulty = "easy"
            elif diff_choice == 2:
                self.difficulty = "normal"
            elif diff_choice == 3:
                self.difficulty = "hard"

            print(f"Difficulty set to: {self.difficulty}")

        elif choice == 2:
            self.debug_mode = not self.debug_mode
            print(f"Debug Mode: {'ON' if self.debug_mode else 'OFF'}")

        input("\nPress Enter to continue...")

    def view_help(self):
        """Display game help information."""
        print(f"\n{CLR_SECTION}[GAME HELP]{CLR_RESET}")

        help_topics = [
            {
                "title": "Game Basics",
                "content": [
                    "Cloud Ranger is a text-based RPG where you protect cloud infrastructure.",
                    "Explore locations, complete quests, and deploy services to earn credits.",
                    "Your main goal is to uncover the identity of the Shadow Admin."
                ]
            },
            {
                "title": "Character Development",
                "content": [
                    "Skills improve as you use them and complete quests.",
                    "Higher skills unlock new opportunities and make challenges easier.",
                    "Faction reputation affects which vendors and quests are available to you."
                ]
            },
            {
                "title": "Cloud Services",
                "content": [
                    "Deploy services to generate passive income.",
                    "Services require maintenance and can be damaged by events.",
                    "Higher performance and security increase service revenue."
                ]
            },
            {
                "title": "Artifacts",
                "content": [
                    "Artifacts are special tools that provide various benefits.",
                    "Each artifact has a cooldown period after use.",
                    "Artifacts can be upgraded to improve their effectiveness."
                ]
            }
        ]

        # Display help topics
        for i, topic in enumerate(help_topics, 1):
            print(f"{i}. {topic['title']}")

        print(f"{len(help_topics) + 1}. Return")

        choice = get_valid_input(
            "Select a topic: ", range(1, len(help_topics) + 2))

        if choice <= len(help_topics):
            topic = help_topics[choice - 1]
            print(f"\n{CLR_TITLE}{topic['title']}{CLR_RESET}")
            for line in topic["content"]:
                print(f"• {line}")

        input("\nPress Enter to continue...")

    def show_credits(self):
        """Display game credits."""
        print(
            f"\n{CLR_TITLE}╔══════════════════════════════════════════════════════════╗{CLR_RESET}")
        print(
            f"{CLR_TITLE}║                  CLOUD RANGER CREDITS                    ║{CLR_RESET}")
        print(
            f"{CLR_TITLE}╚══════════════════════════════════════════════════════════╝{CLR_RESET}")

        print("\nDeveloped by: Python Gaming Team")
        print("Original Concept: AWS Cloud Adventure")
        print("\nSpecial Thanks:")
        print("• All cloud engineers and digital rangers out there")
        print("• The Python community")
        print("• Players like you")

        input("\nPress Enter to continue...")

    def use_scanner_artifact(self, artifact):
        """Use a scanner type artifact."""
        print(f"\n{CLR_SECTION}[SCANNING]{CLR_RESET}")

        display_loading_bar(f"Scanning with {artifact.name}", 2)

        # Scanner artifacts have a chance to discover things
        discovery_chance = 60 + (artifact.power * 5) + \
            (self.player.skills.get("investigation", 0) * 3)

        if random.randint(1, 100) <= discovery_chance:
            # Success - find something
            discovery_type = random.choices(
                ["clue", "vulnerability", "optimization", "credits"],
                weights=[40, 30, 20, 10],
                k=1
            )[0]

            if discovery_type == "clue":
                clue_id = f"scan_clue_{random.randint(1000, 9999)}"
                self.player.add_clue(clue_id)

                aws_service = artifact.aws_service or "AWS"
                print(
                    f"{CLR_CLUE}The {artifact.name} detected unusual activity in {aws_service}.{CLR_RESET}")
                print("This could be related to recent incidents.")

            elif discovery_type == "vulnerability":
                print(
                    f"{CLR_WARNING}The scan detected a security vulnerability!{CLR_RESET}")

                # If player has deployed services, apply to one of them
                if self.player.inventory.deployed_services:
                    service = random.choice(
                        self.player.inventory.deployed_services)
                    if service.is_deployed:
                        # Either fix the vulnerability or find information
                        if confirm_action("Attempt to fix the vulnerability?"):
                            if service.security_level < 10:
                                service.enhance_security(1)
                                display_notification(
                                    f"Successfully patched {service.name}", "success")
                            else:
                                print(
                                    f"{service.name} is already at maximum security.")
                        else:
                            # Learn from the vulnerability
                            self.player.increase_skill("security", 1)
                            credits = random.randint(10, 30)
                            self.player.cloud_credits += credits
                            print(
                                f"{CLR_CREDITS}Analyzing the vulnerability earned you {credits} credits!{CLR_RESET}")
                else:
                    # No services, just gain skill
                    self.player.increase_skill("security", 1)
                    print("You've learned more about securing cloud resources.")

            elif discovery_type == "optimization":
                print(
                    f"{CLR_SUCCESS}The scan revealed potential optimizations!{CLR_RESET}")

                # If player has deployed services, apply to one of them
                if self.player.inventory.deployed_services:
                    service = random.choice(
                        self.player.inventory.deployed_services)
                    if service.is_deployed:
                        if service.performance < 10:
                            service.optimize_performance(1)
                            display_notification(
                                f"Optimized {service.name} performance", "success")
                        else:
                            print(
                                f"{service.name} is already at peak performance.")
                else:
                    # No services, gain skill and credits
                    self.player.increase_skill("cloud", 1)
                    credits = random.randint(15, 35)
                    self.player.cloud_credits += credits
                    print(
                        f"{CLR_CREDITS}Your optimization knowledge earned you {credits} credits!{CLR_RESET}")

            elif discovery_type == "credits":
                credits = (10 * artifact.power) + random.randint(10, 50)
                self.player.cloud_credits += credits
                print(
                    f"{CLR_CREDITS}The scan discovered {credits} unclaimed cloud credits!{CLR_RESET}")

        else:
            # Failure - nothing found
            print(
                f"{CLR_WARNING}The scan completed but found nothing of interest.{CLR_RESET}")

        artifact.cooldown = 2  # Scanner artifacts have shorter cooldown

    def use_security_artifact(self, artifact):
        """Use a security type artifact."""
        print(f"\n{CLR_SECTION}[SECURITY OPERATIONS]{CLR_RESET}")

        display_loading_bar(f"Activating {artifact.name}", 2)

        # Security artifacts can enhance security or deal with threats
        security_skill = self.player.skills.get("security", 0)
        effectiveness = artifact.power + (security_skill // 2)

        # Choose an effect based on artifact
        effects = [
            {
                "name": "Security Audit",
                "description": "Audit all services for vulnerabilities.",
                "action": self._security_audit,
                "args": {"effectiveness": effectiveness}
            },
            {
                "name": "Threat Detection",
                "description": "Scan for active threats in the current location.",
                "action": self._detect_threats,
                "args": {"effectiveness": effectiveness, "artifact": artifact}
            },
            {
                "name": "Access Review",
                "description": "Review access controls for potential issues.",
                "action": self._access_review,
                "args": {"effectiveness": effectiveness}
            }
        ]

        # Present options to player
        print("Choose a security operation:")
        for i, effect in enumerate(effects, 1):
            print(f"{i}. {effect['name']} - {effect['description']}")

        choice = get_valid_input("Select operation: ",
                                 range(1, len(effects) + 1))
        selected = effects[choice - 1]

        # Execute the selected operation
        print(f"\nExecuting {selected['name']}...")
        selected["action"](**selected["args"])

    def use_network_artifact(self, artifact):
        """Use a network type artifact."""
        print(f"\n{CLR_SECTION}[NETWORK OPERATIONS]{CLR_RESET}")

        display_loading_bar(f"Activating {artifact.name}", 2)

        # Network artifacts work with connections and traffic
        network_skill = self.player.skills.get("networking", 0)
        effectiveness = artifact.power + (network_skill // 2)

        # Choose an effect based on artifact
        effects = [
            {
                "name": "Traffic Analysis",
                "description": "Analyze network traffic for insights.",
                "action": self._traffic_analysis,
                "args": {"effectiveness": effectiveness}
            },
            {
                "name": "Route Tracing",
                "description": "Trace connections to discover new locations.",
                "action": self._route_tracing,
                "args": {"effectiveness": effectiveness}
            },
            {
                "name": "Connection Boost",
                "description": "Temporarily boost your bandwidth.",
                "action": self._connection_boost,
                "args": {"effectiveness": effectiveness}
            }
        ]

        # Present options to player
        print("Choose a network operation:")
        for i, effect in enumerate(effects, 1):
            print(f"{i}. {effect['name']} - {effect['description']}")

        choice = get_valid_input("Select operation: ",
                                 range(1, len(effects) + 1))
        selected = effects[choice - 1]

        # Execute the selected operation
        print(f"\nExecuting {selected['name']}...")
        selected["action"](**selected["args"])

    def use_recovery_artifact(self, artifact):
        """Use a recovery type artifact."""
        print(f"\n{CLR_SECTION}[RECOVERY OPERATIONS]{CLR_RESET}")

        # Recovery artifacts restore services or health
        power = artifact.power + artifact.upgrade_level

        if self.player.inventory.deployed_services:
            # Show deployable services and add a health recovery option
            print("Select a target for recovery:")

            options = []
            for i, service in enumerate(self.player.inventory.deployed_services, 1):
                status = "ONLINE" if service.is_deployed else "OFFLINE"
                health_status = f"Health: {service.health}%"
                print(
                    f"{i}. {service.name} ({service.instance_id}) - {status} - {health_status}")
                options.append(service)

            # Add player health option
            player_option = len(options) + 1
            print(
                f"{player_option}. Recover your own health ({self.player.health}/{self.player.max_health})")

            # Add cancel option
            cancel_option = player_option + 1
            print(f"{cancel_option}. Cancel")

            choice = get_valid_input(
                "Select recovery target: ", range(1, cancel_option + 1))

            if choice == cancel_option:
                return

            if choice == player_option:
                # Heal player
                heal_amount = power * 10
                actual_heal = self.player.heal(heal_amount)
                display_loading_bar(f"Administering recovery protocol", 1.5)
                display_notification(
                    f"Recovered {actual_heal} health points", "success")
            else:
                # Heal service
                service = options[choice - 1]

                if not service.is_deployed and service.health == 0:
                    # Attempt to bring service back online
                    display_loading_bar("Attempting emergency recovery", 2)

                    recovery_chance = 50 + (power * 5)
                    if random.randint(1, 100) <= recovery_chance:
                        service.is_deployed = True
                        service.health = 30  # Partial recovery
                        display_notification(
                            f"Emergency recovery successful! {service.name} is back online but needs maintenance.", "success")
                    else:
                        display_notification(
                            "Recovery attempt failed. Service remains offline.", "error")
                else:
                    # Regular health recovery
                    repair_amount = power * 15
                    display_loading_bar(f"Repairing {service.name}", 1.5)
                    actual_repair = service.repair(repair_amount)
                    display_notification(
                        f"Repaired {service.name} by {actual_repair}% health", "success")
        else:
            # No services, just heal player
            heal_amount = power * 10
            actual_heal = self.player.heal(heal_amount)
            display_loading_bar(f"Administering recovery protocol", 1.5)
            display_notification(
                f"Recovered {actual_heal} health points", "success")

    def use_database_artifact(self, artifact):
        """Use a database type artifact."""
        print(f"\n{CLR_SECTION}[DATABASE OPERATIONS]{CLR_RESET}")

        display_loading_bar(f"Activating {artifact.name}", 2)

        # Database artifacts work with data and information
        database_skill = self.player.skills.get("database", 0)
        effectiveness = artifact.power + (database_skill // 2)

        # Choose an effect based on artifact
        effects = [
            {
                "name": "Data Mining",
                "description": "Extract valuable information from databases.",
                "action": self._data_mining,
                "args": {"effectiveness": effectiveness}
            },
            {
                "name": "Query Optimization",
                "description": "Optimize database queries for better performance.",
                "action": self._query_optimization,
                "args": {"effectiveness": effectiveness}
            },
            {
                "name": "Restore Backup",
                "description": "Attempt to restore data from backups.",
                "action": self._restore_backup,
                "args": {"effectiveness": effectiveness}
            }
        ]

        # Present options to player
        print("Choose a database operation:")
        for i, effect in enumerate(effects, 1):
            print(f"{i}. {effect['name']} - {effect['description']}")

        choice = get_valid_input("Select operation: ",
                                 range(1, len(effects) + 1))
        selected = effects[choice - 1]

        # Execute the selected operation
        print(f"\nExecuting {selected['name']}...")
        selected["action"](**selected["args"])

    def vendor_menu(self, vendor):
        """Display and interact with a vendor's inventory."""
        while True:
            print(f"\n{CLR_SECTION}[{vendor['name']}]{CLR_RESET}")
            print(vendor['description'])
            print(
                f"{CLR_CREDITS}Your Credits: {self.player.cloud_credits}{CLR_RESET}")

            # Display vendor inventory
            categories = []
            if "artifacts" in vendor["inventory"]:
                categories.append("artifacts")
            if "services" in vendor["inventory"]:
                categories.append("services")
            if "consumables" in vendor["inventory"]:
                categories.append("consumables")

            if not categories:
                print("This vendor doesn't have anything for sale at the moment.")
                input("\nPress Enter to continue...")
                return

            # Let player choose category
            print("\nWhat would you like to browse?")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category.capitalize()}")

            print(f"{len(categories) + 1}. Exit Shop")

            choice = get_valid_input(
                "Select category: ", range(1, len(categories) + 2))

            if choice == len(categories) + 1:
                return

            selected_category = categories[choice - 1]

            # Show items in selected category
            if selected_category == "artifacts":
                self.browse_artifacts(vendor)
            elif selected_category == "services":
                self.browse_services(vendor)
            elif selected_category == "consumables":
                self.browse_consumables(vendor)

    # Add utility methods for the security, network, and database artifact actions

    def _security_audit(self, effectiveness):
        """Perform a security audit on all deployed services."""
        vulnerable_services = []

        for service in self.player.inventory.deployed_services:
            if service.is_deployed and service.security_level < 8:
                # Lower security services might have vulnerabilities
                chance = 60 - (service.security_level * 5)
                if random.randint(1, 100) <= chance:
                    vulnerable_services.append(service)

        if vulnerable_services:
            print(
                f"{CLR_WARNING}Security audit found vulnerabilities in {len(vulnerable_services)} services:{CLR_RESET}")

            for i, service in enumerate(vulnerable_services, 1):
                print(
                    f"{i}. {service.name} ({service.instance_id}) - Security Level: {service.security_level}/10")

            print(
                f"{len(vulnerable_services) + 1}. Fix All (Cost: {len(vulnerable_services) * 10} credits)")
            print(f"{len(vulnerable_services) + 2}. Cancel")

            choice = get_valid_input("Select an option: ", range(
                1, len(vulnerable_services) + 3))

            if choice <= len(vulnerable_services):
                # Fix single service
                service = vulnerable_services[choice - 1]
                cost = 10

                if self.player.cloud_credits >= cost:
                    self.player.cloud_credits -= cost
                    # Effectiveness determines how much security is improved
                    improvement = min(2, max(1, effectiveness // 3))
                    service.enhance_security(improvement)
                    display_notification(
                        f"Fixed vulnerability in {service.name}", "success")
                else:
                    display_notification("Not enough credits!", "error")

            elif choice == len(vulnerable_services) + 1:
                # Fix all
                total_cost = len(vulnerable_services) * 10

                if self.player.cloud_credits >= total_cost:
                    self.player.cloud_credits -= total_cost
                    for service in vulnerable_services:
                        improvement = min(2, max(1, effectiveness // 3))
                        service.enhance_security(improvement)
                    display_notification(
                        f"Fixed vulnerabilities in all services", "success")
                else:
                    display_notification("Not enough credits!", "error")
        else:
            print(
                f"{CLR_SUCCESS}Security audit complete. No significant vulnerabilities found.{CLR_RESET}")

            # Small reputation bonus with CorpSec for maintaining good security
            self.player.update_faction_reputation("CorpSec", 1)

    def _detect_threats(self, effectiveness, artifact):
        """Scan for active threats in the current location."""
        current_loc = self.player.current_location

        # Threat detection is more likely to find something in higher difficulty locations
        detection_chance = 30 + effectiveness * 5
        if current_loc.difficulty >= 5:
            detection_chance += 20

        if random.randint(1, 100) <= detection_chance:
            threat_level = random.randint(
                1, min(10, current_loc.difficulty + 2))

            print(f"{CLR_WARNING}Threat detected! Level {threat_level}/10{CLR_RESET}")

            # Random threat type
            threat_types = ["Intrusion", "Data Breach",
                            "Malware", "DoS Attack", "Unauthorized Access"]
            threat = random.choice(threat_types)

            print(f"Type: {threat}")
            print(f"Location: {current_loc.name}")

            # Player can investigate or neutralize
            print("\nOptions:")
            print("1. Investigate (gain intelligence)")
            print("2. Neutralize (prevent damage)")
            print("3. Ignore (potential consequences)")

            action = get_valid_input("Choose an action: ", range(1, 4))

            if action == 1:
                # Investigate
                investigation_success = (
                    effectiveness + self.player.skills.get("investigation", 0)) >= threat_level * 1.5

                if investigation_success:
                    print(f"{CLR_SUCCESS}Investigation successful!{CLR_RESET}")

                    # Generate a clue
                    clue_id = f"threat_clue_{random.randint(1000, 9999)}"
                    self.player.add_clue(clue_id)

                    # Gain investigation skill
                    self.player.increase_skill("investigation", 1)

                    # Small chance to implicate ShadowNetwork
                    if random.randint(1, 100) <= 40:
                        print(
                            f"{CLR_SHADOW_ADMIN}The threat appears to be connected to the Shadow Network...{CLR_RESET}")
                        self.player.update_faction_reputation(
                            "ShadowNetwork", -1)
                else:
                    print(
                        f"{CLR_ERROR}The investigation was inconclusive.{CLR_RESET}")

            elif action == 2:
                # Neutralize
                neutralize_success = (
                    effectiveness + self.player.skills.get("security", 0)) >= threat_level

                if neutralize_success:
                    print(f"{CLR_SUCCESS}Threat neutralized!{CLR_RESET}")

                    # Gain security skill
                    self.player.increase_skill("security", 1)

                    # Faction reputation with CorpSec
                    self.player.update_faction_reputation("CorpSec", 2)

                    # Reward based on threat level
                    credits = threat_level * 10
                    self.player.cloud_credits += credits
                    print(
                        f"{CLR_CREDITS}Earned {credits} credits for neutralizing the threat.{CLR_RESET}")
                else:
                    print(f"{CLR_ERROR}Failed to neutralize the threat!{CLR_RESET}")

                    # If the player has any deployed services, one might be damaged
                    if self.player.inventory.deployed_services:
                        vulnerable_service = random.choice(
                            self.player.inventory.deployed_services)
                        if vulnerable_service.is_deployed:
                            damage = threat_level * 5
                            vulnerable_service.apply_damage(damage)
                            print(
                                f"{CLR_ERROR}The threat damaged {vulnerable_service.name}!{CLR_RESET}")

            elif action == 3:
                # Ignore
                print(
                    f"{CLR_WARNING}You decide to ignore the threat for now.{CLR_RESET}")

                # Chance for consequences
                if random.randint(1, 100) <= 40 + (threat_level * 5):
                    # Random negative effect
                    effect_type = random.choice(
                        ["service", "credits", "reputation"])

                    if effect_type == "service" and self.player.inventory.deployed_services:
                        vulnerable_service = random.choice(
                            self.player.inventory.deployed_services)
                        if vulnerable_service.is_deployed:
                            damage = threat_level * 7  # More damage for ignoring
                            vulnerable_service.apply_damage(damage)
                            print(
                                f"{CLR_ERROR}A service was damaged by the ignored threat!{CLR_RESET}")

                    elif effect_type == "credits":
                        loss = threat_level * 15
                        self.player.cloud_credits = max(
                            0, self.player.cloud_credits - loss)
                        print(
                            f"{CLR_ERROR}The threat resulted in a loss of {loss} credits!{CLR_RESET}")

                    elif effect_type == "reputation":
                        self.player.update_faction_reputation(
                            "CorpSec", -threat_level)
                        print(
                            f"{CLR_ERROR}Your reputation with CorpSec has decreased for ignoring the threat.{CLR_RESET}")

        else:
            print(
                f"{CLR_SUCCESS}No active threats detected in this location.{CLR_RESET}")
            print("The scan completed successfully.")

    def _access_review(self, effectiveness):
        """Review access controls for potential issues."""
        print("Conducting access review...")

        # Chance to find access issues
        discovery_chance = 40 + (effectiveness * 3)

        if random.randint(1, 100) <= discovery_chance:
            issue_found = random.choice([
                "excessive privileges",
                "dormant accounts",
                "weak authentication",
                "missing MFA",
                "leaked credentials"
            ])

            print(
                f"{CLR_WARNING}Access review found issues: {issue_found}{CLR_RESET}")

            # Remediation options
            print("\nOptions:")
            print("1. Apply quick fix (costs 15 credits)")
            print(
                "2. Perform comprehensive remediation (costs 35 credits, more effective)")
            print("3. Ignore (potential security risk)")

            choice = get_valid_input("Choose an action: ", range(1, 4))

            if choice == 1:
                # Quick fix
                if self.player.cloud_credits >= 15:
                    self.player.cloud_credits -= 15

                    # Apply effects
                    if self.player.inventory.deployed_services:
                        # Improve security for a random service
                        service = random.choice(
                            self.player.inventory.deployed_services)
                        if service.is_deployed and service.security_level < 10:
                            service.enhance_security(1)
                            print(
                                f"{CLR_SUCCESS}Applied quick fix to {service.name}.{CLR_RESET}")
                        else:
                            print(
                                f"{CLR_SUCCESS}Applied general security improvements.{CLR_RESET}")

                    # Small skill gain
                    self.player.increase_skill("security", 1)
                else:
                    display_notification("Not enough credits!", "error")

            elif choice == 2:
                # Comprehensive fix
                if self.player.cloud_credits >= 35:
                    self.player.cloud_credits -= 35

                    display_loading_bar(
                        "Applying comprehensive remediation", 2)

                    # Apply effects to all services
                    security_improved = False
                    if self.player.inventory.deployed_services:
                        for service in self.player.inventory.deployed_services:
                            if service.is_deployed and service.security_level < 10:
                                service.enhance_security(2)
                                security_improved = True

                    if security_improved:
                        print(
                            f"{CLR_SUCCESS}Improved security for all deployed services.{CLR_RESET}")
                    else:
                        print(
                            f"{CLR_SUCCESS}Applied comprehensive security improvements.{CLR_RESET}")

                    # Larger skill gain
                    self.player.increase_skill("security", 2)

                    # Reputation gain
                    self.player.update_faction_reputation("CorpSec", 3)
                else:
                    display_notification("Not enough credits!", "error")

            elif choice == 3:
                # Ignore
                print(
                    f"{CLR_WARNING}You decide to ignore the access issues for now.{CLR_RESET}")

                # Chance for negative consequence later
                if random.randint(1, 100) <= 30:
                    # Queue a security incident for later
                    # (This could be implemented with a delayed event system)
                    print(
                        f"{CLR_WARNING}This decision may have consequences...{CLR_RESET}")

                    # Small reputation loss
                    self.player.update_faction_reputation("CorpSec", -1)

        else:
            print(
                f"{CLR_SUCCESS}Access review complete. No significant issues found.{CLR_RESET}")
            # Small skill gain for being thorough
            self.player.increase_skill("security", 1)

    # More utility methods for the network artifact actions

    def _traffic_analysis(self, effectiveness):
        """Analyze network traffic for insights."""
        print("Analyzing network traffic patterns...")
        display_loading_bar("Processing data packets", 2)

        # Insights depend on effectiveness
        insight_chance = 40 + (effectiveness * 4)

        if random.randint(1, 100) <= insight_chance:
            # Discovery types
            discoveries = [
                {"name": "Unusual Traffic Pattern",
                    "type": "security", "value": 1},
                {"name": "Optimization Opportunity",
                    "type": "performance", "value": 2},
                {"name": "Encrypted Communications", "type": "clue", "value": 1},
                {"name": "Credit Generating Algorithm",
                    "type": "credits", "value": effectiveness * 5},
                {"name": "Skill Enhancement Pathway", "type": "skill", "value": 1}
            ]

            discovery = random.choice(discoveries)

            print(
                f"{CLR_SUCCESS}Analysis complete. Found: {discovery['name']}{CLR_RESET}")

            if discovery["type"] == "security":
                for service in self.player.inventory.deployed_services:
                    if service.is_deployed and service.security_level < 10:
                        service.enhance_security(discovery["value"])
                        print(
                            f"Enhanced security for {service.name} by analyzing threat patterns.")
                        break
                else:
                    self.player.increase_skill("security", 1)
                    print("Learned about security threats from traffic analysis.")

            elif discovery["type"] == "performance":
                for service in self.player.inventory.deployed_services:
                    if service.is_deployed and service.performance < 10:
                        service.optimize_performance(discovery["value"])
                        print(
                            f"Optimized {service.name} based on traffic patterns.")
                        break
                else:
                    self.player.increase_skill("networking", 1)
                    print("Learned optimization techniques from traffic analysis.")

            elif discovery["type"] == "clue":
                clue_id = f"traffic_clue_{random.randint(1000, 9999)}"
                self.player.add_clue(clue_id)

            elif discovery["type"] == "credits":
                credits = discovery["value"]
                self.player.cloud_credits += credits
                print(
                    f"{CLR_CREDITS}Discovering inefficiencies saved {credits} credits!{CLR_RESET}")

            elif discovery["type"] == "skill":
                skill = random.choice(
                    ["networking", "investigation", "security"])
                self.player.increase_skill(skill, discovery["value"])

        else:
            print(
                f"{CLR_WARNING}Analysis complete. No significant insights found in the traffic.{CLR_RESET}")
            # Still gain a little networking experience
            self.player.increase_skill("networking", 1)

    def _route_tracing(self, effectiveness):
        """Trace connections to discover new locations."""
        print("Tracing network routes...")
        display_loading_bar("Mapping connections", 2)

        # Get current location
        current_loc = self.player.current_location

        # Find locations that aren't directly connected but could be
        potential_discoveries = []
        for loc_name, location in self.locations.items():
            # Skip current location and already connected locations
            if loc_name == current_loc.name or loc_name in current_loc.connections:
                continue

            # Check if this location is already discovered
            if loc_name in self.discovered_locations:
                # Already discovered locations are easier to connect to
                if random.randint(1, 100) <= 60 + effectiveness:
                    potential_discoveries.append(location)
            else:
                # Undiscovered locations are harder to find
                if random.randint(1, 100) <= 30 + effectiveness:
                    # Limit by difficulty - can't discover locations too far above current skills
                    max_safe_difficulty = max(self.player.skills.values()) + 3
                    if location.difficulty <= max_safe_difficulty:
                        potential_discoveries.append(location)

        if potential_discoveries:
            # Limit discoveries based on effectiveness
            max_discoveries = min(3, 1 + (effectiveness // 3))
            discoveries = random.sample(potential_discoveries, min(
                max_discoveries, len(potential_discoveries)))

            print(
                f"{CLR_SUCCESS}Route tracing complete. Discovered connections to {len(discoveries)} locations:{CLR_RESET}")

            for i, location in enumerate(discoveries, 1):
                print(f"{i}. {location.name} - {location.region}")
                # Add to discovered locations
                self.discovered_locations.add(location.name)

                # Option to add direct connection
                # First discovery always adds connection
                if i == 1 or random.randint(1, 100) <= 40:
                    current_loc.add_connection(location.name)
                    location.add_connection(current_loc.name)
                    print(
                        f"{CLR_SUCCESS}Established direct connection to {location.name}!{CLR_RESET}")

            # Skill gain
            self.player.increase_skill("networking", 1)

        else:
            print(
                f"{CLR_WARNING}Route tracing complete. No new connections discovered.{CLR_RESET}")
            # Still gain a little networking experience
            if random.randint(1, 100) <= 50:
                self.player.increase_skill("networking", 1)

    def _connection_boost(self, effectiveness):
        """Temporarily boost your bandwidth."""
        print("Optimizing network connection...")
        display_loading_bar("Enhancing bandwidth", 1.5)

        # Calculate boost amount
        boost_amount = effectiveness * 10
        duration = 3 + (effectiveness // 3)

        # Apply boost
        original_bandwidth = self.player.bandwidth
        self.player.bandwidth += boost_amount

        print(
            f"{CLR_SUCCESS}Connection optimized! Bandwidth increased by {boost_amount}.{CLR_RESET}")
        print(f"Duration: {duration} days")
        print(f"New bandwidth: {self.player.bandwidth}")

        # Add a temporary boost that will be removed later
        # This would need to be handled in the update_game_state method
        print(f"{CLR_WARNING}Note: This feature is not fully implemented in the game mechanics.{CLR_RESET}")

        # Skill gain
        self.player.increase_skill("networking", 1)

    # Database artifact utility methods

    def _data_mining(self, effectiveness):
        """Extract valuable information from databases."""
        print("Mining databases for valuable information...")
        display_loading_bar("Processing data", 2)

        # Success chance
        success_chance = 50 + (effectiveness * 3) + \
            (self.player.skills.get("database", 0) * 3)

        if random.randint(1, 100) <= success_chance:
            # Determine reward type
            reward_type = random.choices(
                ["credits", "clue", "intelligence", "skill"],
                weights=[40, 30, 20, 10],
                k=1
            )[0]

            if reward_type == "credits":
                credits = effectiveness * 10 + random.randint(20, 50)
                self.player.cloud_credits += credits
                print(
                    f"{CLR_SUCCESS}Data mining successful! Extracted valuable market data.{CLR_RESET}")
                print(
                    f"{CLR_CREDITS}Earned {credits} credits from the information.{CLR_RESET}")

            elif reward_type == "clue":
                clue_id = f"data_mining_clue_{random.randint(1000, 9999)}"
                self.player.add_clue(clue_id)
                print(
                    f"{CLR_SUCCESS}Data mining successful! Uncovered hidden connections.{CLR_RESET}")

                # Chance to find Shadow Admin connection
                if random.randint(1, 100) <= 20:
                    print(
                        f"{CLR_SHADOW_ADMIN}The data contains references to the Shadow Admin...{CLR_RESET}")
                    self.player.update_faction_reputation("ShadowNetwork", 1)

            elif reward_type == "intelligence":
                # Reveal information about a quest
                active_quests = self.player.active_quests
                if active_quests:
                    quest_id = random.choice(active_quests)
                    if quest_id in self.quests:
                        quest = self.quests[quest_id]

                        # Find an incomplete objective
                        incomplete_objectives = [
                            obj for obj in quest.objectives if not obj["completed"]]
                        if incomplete_objectives:
                            objective = random.choice(incomplete_objectives)
                            print(
                                f"{CLR_SUCCESS}Data mining successful! Found intel related to your quest:{CLR_RESET}")
                            print(f"Quest: {quest.title}")
                            print(f"Objective: {objective['description']}")
                            print(
                                f"{CLR_CLUE}The data suggests you should focus on locations with higher security.{CLR_RESET}")
                        else:
                            print(
                                f"{CLR_SUCCESS}Data mining successful! Found useful intelligence.{CLR_RESET}")
                            self.player.increase_skill("investigation", 1)
                    else:
                        print(
                            f"{CLR_SUCCESS}Data mining successful! Found useful intelligence.{CLR_RESET}")
                        self.player.increase_skill("investigation", 1)
                else:
                    print(
                        f"{CLR_SUCCESS}Data mining successful! Found useful intelligence.{CLR_RESET}")
                    self.player.increase_skill("investigation", 1)

            elif reward_type == "skill":
                skill = random.choice(
                    ["database", "investigation", "security"])
                self.player.increase_skill(skill, 1)
                print(
                    f"{CLR_SUCCESS}Data mining successful! Learned new techniques.{CLR_RESET}")

        else:
            print(
                f"{CLR_WARNING}Data mining operation completed with limited results.{CLR_RESET}")

            # Small chance to attract attention
            if random.randint(1, 100) <= 20:
                print(
                    f"{CLR_WARNING}Your data mining activities may have attracted unwanted attention...{CLR_RESET}")

                # Small reputation hit
                faction = random.choice(["CorpSec", "DataBrokers"])
                self.player.update_faction_reputation(faction, -1)

    def _query_optimization(self, effectiveness):
        """Optimize database queries for better performance."""
        print("Optimizing database queries...")
        display_loading_bar("Analyzing query patterns", 2)

        # Apply to services if available
        optimized_services = 0

        if self.player.inventory.deployed_services:
            for service in self.player.inventory.deployed_services:
                if service.is_deployed and service.service_type in ["Database"]:
                    # Database services get direct performance boost
                    performance_boost = min(3, 1 + (effectiveness // 3))
                    if service.performance < 10:
                        service.optimize_performance(performance_boost)
                        optimized_services += 1
                elif service.is_deployed:
                    # Non-database services get smaller boost
                    performance_boost = 1
                    if service.performance < 10 and random.randint(1, 100) <= 50:
                        service.optimize_performance(performance_boost)
                        optimized_services += 1

        if optimized_services > 0:
            print(f"{CLR_SUCCESS}Query optimization complete! Improved performance for {optimized_services} services.{CLR_RESET}")

            # Calculate credits saved
            credits_saved = optimized_services * 5 * effectiveness
            self.player.cloud_credits += credits_saved
            print(f"{CLR_CREDITS}Optimization will save approximately {credits_saved} credits in operational costs.{CLR_RESET}")

            # Reputation gain
            if optimized_services >= 3:
                self.player.update_faction_reputation("DataBrokers", 2)
                print(
                    f"{CLR_SUCCESS}Your optimization skills have impressed the Data Brokers.{CLR_RESET}")
        else:
            print(
                f"{CLR_WARNING}Query optimization complete, but no suitable services to optimize.{CLR_RESET}")
            print("The experience has still improved your database skills.")

        # Skill gain
        self.player.increase_skill("database", 1)

    def _restore_backup(self, effectiveness):
        """Attempt to restore data from backups."""
        print("Searching for available backups...")
        display_loading_bar("Scanning backup repositories", 2)

        # Find services that need restoration
        restorable_services = []

        if self.player.inventory.deployed_services:
            for service in self.player.inventory.deployed_services:
                if not service.is_deployed or service.health < 50:
                    restorable_services.append(service)

        if restorable_services:
            print(
                f"{CLR_SUCCESS}Found {len(restorable_services)} services that could benefit from restoration:{CLR_RESET}")

            for i, service in enumerate(restorable_services, 1):
                status = "OFFLINE" if not service.is_deployed else f"Health: {service.health}%"
                print(f"{i}. {service.name} ({service.instance_id}) - {status}")

            print(f"{len(restorable_services) + 1}. Cancel")

            choice = get_valid_input("Select a service to restore: ", range(
                1, len(restorable_services) + 2))

            if choice <= len(restorable_services):
                service = restorable_services[choice - 1]

                print(f"Attempting to restore {service.name}...")
                display_loading_bar("Retrieving backup data", 2)

                # Calculate success chance
                success_chance = 50 + (effectiveness * 5) + \
                    (self.player.skills.get("database", 0) * 3)

                if random.randint(1, 100) <= success_chance:
                    if not service.is_deployed:
                        service.is_deployed = True
                        # Partial health restoration
                        service.health = 50 + (effectiveness * 5)
                        print(
                            f"{CLR_SUCCESS}Successfully restored {service.name} from backup!{CLR_RESET}")
                        print(
                            f"Service is now online with {service.health}% health.")
                    else:
                        health_before = service.health
                        service.health = min(
                            100, service.health + 30 + (effectiveness * 3))
                        print(
                            f"{CLR_SUCCESS}Successfully restored {service.name} data from backup!{CLR_RESET}")
                        print(
                            f"Health improved from {health_before}% to {service.health}%.")

                    # Skill gain
                    self.player.increase_skill("database", 1)

                    # Reputation gain
                    if service.service_type == "Database":
                        self.player.update_faction_reputation("DataBrokers", 2)
                else:
                    print(
                        f"{CLR_ERROR}Backup restoration failed. The backup data may be corrupted.{CLR_RESET}")

                    # Still gain some skill
                    if random.randint(1, 100) <= 50:
                        self.player.increase_skill("database", 1)
                        print("You learned from the experience despite the failure.")
        else:
            print(
                f"{CLR_WARNING}No services found that require backup restoration.{CLR_RESET}")

            # Alternative benefit
            print("Instead, you optimize your backup procedures.")

            # Protect against future failures
            for service in self.player.inventory.deployed_services:
                if service.is_deployed:
                    # Add a "Backup Protection" status effect
                    service.add_status_effect({
                        "name": "Backup Protection",
                        "duration": 5,
                        "per_turn_effect": lambda s: None,  # No per-turn effect
                        "description": "Protects against critical failures"
                    })

            # Skill gain
            self.player.increase_skill("database", 1)

    # Methods for browsing vendor inventory

    def browse_artifacts(self, vendor):
        """Browse and potentially purchase artifacts from a vendor."""
        if "artifacts" not in vendor["inventory"] or not vendor["inventory"]["artifacts"]:
            print("This vendor doesn't have any artifacts for sale.")
            return

        print(f"\n{CLR_SECTION}[ARTIFACTS FOR SALE]{CLR_RESET}")

        artifacts_for_sale = []
        for artifact_name in vendor["inventory"]["artifacts"]:
            if artifact_name in self.artifacts:
                artifact_data = self.artifacts[artifact_name]
                artifacts_for_sale.append(artifact_data)

        if not artifacts_for_sale:
            print("No artifacts available at this time.")
            return

        # Display artifacts
        for i, artifact in enumerate(artifacts_for_sale, 1):
            # Purchasing price is higher than base cost
            price = artifact["cost"] * 2
            print(f"{i}. {artifact['name']} - {artifact['description']}")
            print(
                f"   Type: {artifact['artifact_type']} | Power: {artifact['power']} | Price: {price} credits")

        print(f"{len(artifacts_for_sale) + 1}. Cancel")

        choice = get_valid_input("Select an artifact to purchase: ", range(
            1, len(artifacts_for_sale) + 2))

        if choice <= len(artifacts_for_sale):
            selected = artifacts_for_sale[choice - 1]
            price = selected["cost"] * 2

            if self.player.cloud_credits >= price:
                if confirm_action(f"Purchase {selected['name']} for {price} credits?"):
                    self.player.cloud_credits -= price

                    new_artifact = CloudArtifact(
                        selected["name"],
                        selected["description"],
                        selected["artifact_type"],
                        selected["aws_service"],
                        selected["cost"],
                        selected["power"]
                    )

                    if self.player.add_artifact(new_artifact):
                        display_notification(
                            f"Purchased {selected['name']}!", "success")
                    else:
                        # Refund if inventory is full
                        self.player.cloud_credits += price
                        display_notification(
                            "Purchase failed: Inventory full", "error")
            else:
                display_notification(
                    "Not enough credits for this purchase!", "error")

    def browse_services(self, vendor):
        """Browse and potentially purchase services from a vendor."""
        if "services" not in vendor["inventory"] or not vendor["inventory"]["services"]:
            print("This vendor doesn't have any services for sale.")
            return

        print(f"\n{CLR_SECTION}[SERVICES FOR SALE]{CLR_RESET}")

        services_for_sale = []
        for service_name in vendor["inventory"]["services"]:
            if service_name in self.services:
                service_data = self.services[service_name]
                services_for_sale.append(service_data)

        if not services_for_sale:
            print("No services available at this time.")
            return

        # Display services
        for i, service in enumerate(services_for_sale, 1):
            # Purchase price is higher than deploy cost
            price = service["deploy_cost"] * 1.5
            print(f"{i}. {service['name']} - {service['description']}")
            print(
                f"   Type: {service['service_type']} | Cost/hr: {service['cost_per_hour']} | Price: {price} credits")

        print(f"{len(services_for_sale) + 1}. Cancel")

        choice = get_valid_input(
            "Select a service to purchase: ", range(1, len(services_for_sale) + 2))

        if choice <= len(services_for_sale):
            selected = services_for_sale[choice - 1]
            price = int(selected["deploy_cost"] * 1.5)

            if self.player.cloud_credits >= price:
                if confirm_action(f"Purchase {selected['name']} for {price} credits?"):
                    self.player.cloud_credits -= price

                    new_service = CloudService(
                        selected["name"],
                        selected["description"],
                        selected["service_type"],
                        selected["cost_per_hour"],
                        selected["deploy_cost"],
                        selected["region_availability"],
                        selected["dependencies"]
                    )

                    if self.player.add_service(new_service):
                        display_notification(
                            f"Purchased {selected['name']}!", "success")
                    else:
                        # Refund if inventory is full
                        self.player.cloud_credits += price
                        display_notification(
                            "Purchase failed: Service limit reached", "error")
            else:
                display_notification(
                    "Not enough credits for this purchase!", "error")

    def browse_consumables(self, vendor):
        """Browse and potentially purchase consumables from a vendor."""
        if "consumables" not in vendor["inventory"] or not vendor["inventory"]["consumables"]:
            print("This vendor doesn't have any consumables for sale.")
            return

        print(f"\n{CLR_SECTION}[CONSUMABLES FOR SALE]{CLR_RESET}")

        consumables = vendor["inventory"]["consumables"]

        # Display consumables
        items = list(consumables.items())
        for i, (item_name, item_data) in enumerate(items, 1):
            print(f"{i}. {item_name} - {item_data['description']}")
            print(f"   Price: {item_data['price']} credits")

        print(f"{len(items) + 1}. Cancel")

        choice = get_valid_input(
            "Select an item to purchase: ", range(1, len(items) + 2))

        if choice <= len(items):
            item_name, item_data = items[choice - 1]

            # Ask for quantity
            quantity = get_valid_input(
                # Max 10 at once
                "How many would you like to buy? ", range(1, 11))

            total_price = item_data['price'] * quantity

            if self.player.cloud_credits >= total_price:
                if confirm_action(f"Purchase {quantity}x {item_name} for {total_price} credits?"):
                    self.player.cloud_credits -= total_price
                    self.player.inventory.add_consumable(item_name, quantity)
                    display_notification(
                        f"Purchased {quantity}x {item_name}!", "success")
            else:
                display_notification(
                    "Not enough credits for this purchase!", "error")


def main():
    """Main function to start the game."""
    # Initialize colorama if available
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass

    # Create and start game
    game = Game()

    try:
        clear_screen()

        # Display title screen
        title_art = """
   ____  _                 _   ____                             
  / ___|| | ___  _   _  __| | |  _ \ __ _ _ __   __ _  ___ _ __ 
 | |    | |/ _ \| | | |/ _` | | |_) / _` | '_ \ / _` |/ _ \ '__|
 | |___ | | (_) | |_| | (_| | |  _ < (_| | | | | (_| |  __/ |   
  \____||_|\___/ \__,_|\__,_| |_| \_\__,_|_| |_|\__, |\___|_|   
                                                |___/           
  ____  _       _ _        _   _____                _   _           
 |  _ \(_) __ _(_) |_ __ _| | |  ___|_ __ ___  _ __| |_(_) ___ _ __ 
 | | | | |/ _` | | __/ _` | | | |_ | '__/ _ \| '__| __| |/ _ \ '__|
 | |_| | | (_| | | || (_| | | |  _|| | | (_) | |  | |_| |  __/ |   
 |____/|_|\__, |_|\__\__,_|_| |_|  |_|  \___/|_|   \__|_|\___|_|   
          |___/                                                     
        """

        display_ascii_art(title_art, CLR_TITLE)

        print(f"\n{CLR_TITLE}Welcome to Cloud Ranger: Digital Frontier!{CLR_RESET}")
        print("A text-based RPG set in a world where cloud infrastructure comes to life.")

        print("\nOptions:")
        print("1. Start New Game")
        print("2. Exit")

        choice = get_valid_input("\nSelect an option: ", range(1, 3))

        if choice == 1:
            game.start_game()
        else:
            print("\nThanks for checking out Cloud Ranger: Digital Frontier!")

    except KeyboardInterrupt:
        print("\n\nGame terminated by user.")
    except Exception as e:
        print(f"\n\nAn error occurred: {str(e)}")
        if game.debug_mode:
            import traceback
            traceback.print_exc()

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
