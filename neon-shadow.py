import os
import sys
import time
import json
import copy
import random
from collections import defaultdict

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
CLR_INTERACTION = CLR_LIGHTBLUE_EX
CLR_CLUE = CLR_BRIGHT + CLR_YELLOW
CLR_ERROR = CLR_BRIGHT + CLR_RED
CLR_SUCCESS = CLR_BRIGHT + CLR_LIGHTGREEN_EX
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

CLR_TITLE = CLR_BRIGHT + CLR_BLUE
# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.03, color=CLR_RESET, newline=True):
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
        print(f"\r{text} [{CLR_BRIGHT}{CLR_GREEN}{completed}{CLR_RESET}{remaining}] {percent}%", end='')
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
    operations = ['DECRYPTING', 'BYPASSING', 'ACCESSING', 'INJECTING', 'EXTRACTING']
    targets = ['FIREWALL', 'MAINFRAME', 'DATABASE', 'NETWORK', 'SECURITY']
    
    start_time = time.time()
    i = 0
    while time.time() - start_time < duration:
        operation = random.choice(operations)
        target = random.choice(targets)
        print(f"\r{CLR_BRIGHT}{CLR_GREEN}{characters[i % len(characters)]} {operation} {target}... {CLR_RESET}", end='')
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
        
    print(f"\n{color}╔═══════════════════════════════════════╗{CLR_RESET}")
    print(f"{color}║ {prefix}: {message}{' ' * (33 - len(prefix) - len(message))} ║{CLR_RESET}")
    print(f"{color}╚═══════════════════════════════════════╝{CLR_RESET}")

def display_mini_map(current_location, locations):
    """Display a mini map of nearby locations."""
    print(f"\n{CLR_BRIGHT}{CLR_CYAN}╔══ MINI MAP ══╗{CLR_RESET}")
    for location in locations:
        if location == current_location:
            print(f"{CLR_BRIGHT}{CLR_CYAN}║ {CLR_BRIGHT}{CLR_YELLOW}[*] {location}{CLR_RESET}{' ' * (12 - len(location))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        else:
            print(f"{CLR_BRIGHT}{CLR_CYAN}║ {CLR_RESET}[ ] {location}{' ' * (12 - len(location))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
    print(f"{CLR_BRIGHT}{CLR_CYAN}╚═══════════════╝{CLR_RESET}")

def confirm_action(prompt):
    """Ask for confirmation before proceeding."""
    response = input(f"{CLR_PROMPT}{prompt} (y/n): {CLR_RESET}").lower()
    return response == 'y' or response == 'yes'

def display_tutorial_tip(tip):
    """Display a tutorial tip."""
    print(f"\n{CLR_TUTORIAL}┌─ TIP ───────────────────────────────────────┐{CLR_RESET}")
    print(f"{CLR_TUTORIAL}│ {tip}{' ' * (44 - len(tip))} │{CLR_RESET}")
    print(f"{CLR_TUTORIAL}└──────────────────────────────────────────────┘{CLR_RESET}")

# --- Core Classes ---
class CloudArtifact:
    """Represents an AWS service or tool the player can use."""
    
    def __init__(self, name, description, artifact_type, aws_service=None, cost=0, power=1):
        self.name = name
        self.description = description
        # e.g., 'Scanner', 'Firewall', 'Database', 'Compute'
        self.artifact_type = artifact_type
        self.aws_service = aws_service  # The AWS service this artifact is associated with
        self.cost = cost  # Optional Cloud Credit cost to use
        self.power = power  # How powerful this artifact is (1-10)
        self.upgrade_level = 0  # Current upgrade level
        self.max_upgrade = 3  # Maximum upgrade level
        
    def __str__(self):
        upgrade_stars = '★' * self.upgrade_level + '☆' * (self.max_upgrade - self.upgrade_level)
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
        print(f"Using {self.name}...")
        # Implement artifact-specific logic here
        return True

class CloudService:
    """Represents an AWS service that can be deployed by the player."""
    
    def __init__(self, name, description, service_type, cost_per_hour, 
                 deploy_cost, region_availability, dependencies=None):
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
        
    def __str__(self):
        status = "DEPLOYED" if self.is_deployed else "NOT DEPLOYED"
        return f"{CLR_CLOUD_SERVICE}{self.name}{CLR_RESET} ({self.service_type}) - {status}"
        
    def deploy(self, region):
        """Deploy the service to a region."""
        if region in self.region_availability:
            self.is_deployed = True
            self.deployment_region = region
            display_notification(f"Deployed {self.name} to {region}", "success")
            return True
        else:
            display_notification(f"{self.name} not available in {region}", "error")
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
        
        return revenue * performance_multiplier * security_multiplier * health_penalty
        
    def apply_damage(self, amount):
        """Apply damage to the service."""
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.is_deployed = False
            display_notification(f"{self.name} has failed and is now offline!", "error")
            
    def repair(self, amount):
        """Repair the service."""
        self.health = min(100, self.health + amount)
        
    def enhance_security(self, amount):
        """Enhance the security of the service."""
        self.security_level = min(10, self.security_level + amount)
        
    def optimize_performance(self, amount):
        """Optimize the performance of the service."""
        self.performance = min(10, self.performance + amount)

class Inventory:
    """Handles the player's inventory of artifacts and cloud services."""
    
    def __init__(self):
        self.artifacts = []
        self.services = []
        self.cloud_credits = 500
        self.max_artifacts = 10
        self.max_services = 5
        
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
        
        print(f"\n{CLR_ARTIFACT}Artifacts ({len(self.artifacts)}/{self.max_artifacts}):{CLR_RESET}")
        if self.artifacts:
            for idx, artifact in enumerate(self.artifacts, 1):
                print(f"{idx}. {artifact} - {artifact.description}")
        else:
            print("No artifacts in inventory.")
        
        print(f"\n{CLR_CLOUD_SERVICE}Cloud Services ({len(self.services)}/{self.max_services}):{CLR_RESET}")
        if self.services:
            for idx, service in enumerate(self.services, 1):
                status = f"{CLR_GREEN}ONLINE{CLR_RESET}" if service.is_deployed else f"{CLR_RED}OFFLINE{CLR_RESET}"
                print(f"{idx}. {service.name} - {status}")
                if service.is_deployed:
                    print(f"   Region: {service.deployment_region}")
                    print(f"   Health: {service.health}% | Security: {service.security_level}/10 | Performance: {service.performance}/10")
                    print(f"   Revenue: {service.calculate_revenue()} credits/hour")
        else:
            print("No cloud services in inventory.")

class CloudRanger:
    """Represents a Cloud Ranger player character."""
    
    def __init__(self, name, specialty, initial_skills=None):
        self.name = name
        self.specialty = specialty
        self.inventory = Inventory()
        self.bandwidth = 100      # Starting bandwidth
        self.time_left = 365      # Days remaining
        self.clues = set()        # Set of discovered clue IDs
        self.current_location = None
        self.reputation = 50      # Reputation with various factions (0-100)
        self.skill_levels = initial_skills if initial_skills else {
            "cloud": 1,
            "security": 1,
            "database": 1,
            "investigation": 1,
            "networking": 1,
            "serverless": 1
        }
        self.completed_quests = []  # List of completed quest IDs
        self.active_quests = []     # List of active quest IDs
        self.deployed_services = []  # List of deployed services 
        self.temp_skill_boosts = [] # List of temporary skill boosts
        self.artifacts = []         # List of artifacts owned
        self.services = []          # List of available services
        self.logs = []              # Game event logs
        self.achievements = set()   # Set of achievement IDs
        
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
            display_notification(f"Acquired artifact: {artifact.name}", "success")
            return True
        else:
            display_notification("Inventory full! Cannot acquire artifact.", "error")
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
            display_notification(f"Acquired service: {service.name}", "success")
            return True
        else:
            display_notification("Service limit reached! Cannot acquire service.", "error")
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
            display_notification(f"Quest Completed! ({quest_id}) +50 credits", "success")
            return True
        return False
        
    def increase_skill(self, skill, amount=1):
        """Increase a skill level."""
        if skill in self.skill_levels:
            self.skill_levels[skill] = min(10, self.skill_levels[skill] + amount)
            display_notification(f"Skill Increased: {skill} is now level {self.skill_levels[skill]}", "success")
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
        print(f"\n{CLR_BRIGHT}{CLR_CYAN}╔════════ PLAYER STATUS ════════╗{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Name: {self.name}{' ' * (27 - len(self.name))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Location: {self.current_location.name if self.current_location else 'Unknown'}{' ' * (20 - len(self.current_location.name) if self.current_location else 13)}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Reputation: {self.reputation}/100{' ' * 15}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Cloud Credits: {self.cloud_credits}{' ' * (16 - len(str(self.cloud_credits)))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Bandwidth: {self.bandwidth}{' ' * (20 - len(str(self.bandwidth)))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Time Left: {self.time_left} days{' ' * (16 - len(str(self.time_left)))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} Clues: {len(self.clues)} collected{' ' * (15 - len(str(len(self.clues))))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_CYAN}╠════════ SKILL LEVELS ══════════╣{CLR_RESET}")
        
        for skill, level in self.skill_levels.items():
            stars = '★' * level + '☆' * (10 - level)
            print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} {skill.capitalize()}: {stars}{' ' * (10 - len(skill))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        
        print(f"{CLR_BRIGHT}{CLR_CYAN}╠════════ ACTIVE QUESTS ═════════╣{CLR_RESET}")
        if self.active_quests:
            for quest in self.active_quests[:3]:  # Show max 3 quests
                print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} • {quest}{' ' * (28 - len(quest))}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
            if len(self.active_quests) > 3:
                print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} ... and {len(self.active_quests) - 3} more{' ' * 17}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        else:
            print(f"{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET} No active quests{' ' * 15}{CLR_BRIGHT}{CLR_CYAN}║{CLR_RESET}")
        
        print(f"{CLR_BRIGHT}{CLR_CYAN}╚══════════════════════════════════╝{CLR_RESET}")
        
        # Show full inventory
        self.inventory.display()
        
        input(f"{CLR_PROMPT}Press Enter to continue...{CLR_RESET}")

class Quest:
    """Represents a quest or mission that the player can undertake."""
    
    def __init__(self, id, title, description, objectives, reward, prereq_quests=None, 
                min_skill_level=None, location=None):
        self.id = id
        self.title = title
        self.description = description
        self.objectives = objectives  # List of objective dicts with 'id', 'description', 'completed'
        self.reward = reward  # Dict with 'credits', 'artifacts', 'reputation', etc.
        self.prereq_quests = prereq_quests if prereq_quests else []  # List of quest IDs
        self.min_skill_level = min_skill_level if min_skill_level else {}  # Dict of skill: level
        self.location = location  # Location where quest is available
        
    def is_available(self, player):
        """Check if the quest is available to the player."""
        # Check prerequisites
        for quest_id in self.prereq_quests:
            if quest_id not in player.quests_completed:
                return False
                
        # Check skill requirements
        for skill, level in self.min_skill_level.items():
            if player.skill_levels.get(skill, 0) < level:
                return False
                
        return True
        
    def start(self, player):
        """Start the quest."""
        if self.is_available(player):
            player.add_quest(self.id)
            return True
        return False
        
    def complete_objective(self, objective_id):
        """Mark an objective as completed."""
        for obj in self.objectives:
            if obj['id'] == objective_id:
                obj['completed'] = True
                return True
        return False

    def check_completion(self):
        """Check if all objectives are completed."""
        return all(obj['completed'] for obj in self.objectives)

    def display(self):
        """Display quest details."""
        print(
            f"\n{CLR_BRIGHT}{CLR_YELLOW}╔══════ QUEST: {self.title} ══════╗{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} {self.description}{CLR_RESET}")
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
        if 'reputation' in self.reward:
            print(
                f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • Reputation: +{self.reward['reputation']}")
        if 'skill' in self.reward:
            for skill, amount in self.reward['skill'].items():
                print(f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • Skill: {skill.capitalize()} +{amount}")

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

        print(f"\n{CLR_INTERACTION}Connections:{CLR_RESET}")
        for connection in self.connections:
            print(f"• {connection}")

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


class CloudEvent:
    """Represents an event that can occur at a location."""

    def __init__(self, id, name, description, event_type,
                 effects=None, requirements=None, chance=100, repeatable=False):
        self.id = id
        self.name = name
        self.description = description
        # 'encounter', 'discovery', 'disaster', 'reward', etc.
        self.event_type = event_type
        # Effects on player (health, credits, etc.)
        self.effects = effects if effects else {}
        self.requirements = requirements if requirements else {}  # Requirements to trigger
        self.chance = chance  # Chance of occurring (percentage)
        self.repeatable = repeatable  # Can this event occur multiple times?
        self.has_occurred = False

    def can_trigger(self, player):
        """Check if the event can be triggered."""
        if not self.repeatable and self.has_occurred:
            return False

        # Check player requirements
        if 'min_skill' in self.requirements:
            for skill, level in self.requirements['min_skill'].items():
                if player.skill_levels.get(skill, 0) < level:
                    return False

        if 'artifacts' in self.requirements:
            for artifact in self.requirements['artifacts']:
                if not player.has_artifact(artifact):
                    return False

        if 'clues' in self.requirements:
            for clue in self.requirements['clues']:
                if clue not in player.clues:
                    return False

        if 'reputation' in self.requirements:
            if player.reputation < self.requirements['reputation']:
                return False

        # Random chance
        if random.randint(1, 100) > self.chance:
            return False

        return True

    def trigger(self, player):
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

        if 'reputation' in self.effects:
            player.reputation = max(
                0, min(100, player.reputation + self.effects['reputation']))
            if self.effects['reputation'] > 0:
                print(
                    f"{CLR_SUCCESS}Reputation increased by {self.effects['reputation']}{CLR_RESET}")
            else:
                print(
                    f"{CLR_ERROR}Reputation decreased by {-self.effects['reputation']}{CLR_RESET}")

        if 'artifact' in self.effects:
            artifact = CloudArtifact(
                self.effects['artifact']['name'],
                self.effects['artifact']['description'],
                self.effects['artifact']['type'],
                self.effects['artifact'].get('aws_service'),
                self.effects['artifact'].get('cost', 0),
                self.effects['artifact'].get('power', 1)
            )
            player.add_artifact(artifact)

        if 'clue' in self.effects:
            player.add_clue(self.effects['clue'])

        if 'service' in self.effects:
            service = CloudService(
                self.effects['service']['name'],
                self.effects['service']['description'],
                self.effects['service']['type'],
                self.effects['service'].get('cost_per_hour', 1),
                self.effects['service'].get('deploy_cost', 10),
                self.effects['service'].get(
                    'region_availability', ['us-east-1']),
                self.effects['service'].get('dependencies', [])
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

        self.has_occurred = True
        return True


class Game:
    """Main game class that manages the game state and flow."""

    def __init__(self):
        # Create initial location
        self.locations = {}
        self._create_locations()  # Create locations first
        
        # Initialize with starting location
        starting_location = self.locations.get("Cloud City", Location("Unknown", "Starting area"))
        
        # Create player with starting location
        self.player = CloudRanger("", "", {})
        self.player.current_location = starting_location
        
        # Initialize other game components
        self.quests = {}  # Dict of quest ID -> Quest
        self.events = {}  # Dict of event ID -> CloudEvent
        self.artifacts = {}  # Dict of artifact templates
        self.services = {}  # Dict of service templates
        self.current_day = 1
        self.game_over = False
        self.game_won = False
        self.difficulty = "normal"  # easy, normal, hard
        
        # Create game content
        self._create_artifacts()
        self._create_services()
        self._create_quests()
        self._create_events()

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
            "service_type": ["us-east-1", "us-west-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
            "dependencies": ["VPC"]
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
                "skill": {"cloud": 1}
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
                "reputation": 5
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
                "reputation": 20
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
                "reputation": 8
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
                "reputation": 10
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
                "reputation": 12
            }
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
                "clue": "The Cloud Rangers protect the digital infrastructure from threats."
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
                "clue": "The intruder used a sophisticated SQL injection technique."
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
                "skill": {"serverless": 1, "cloud": 1}
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
                "reputation": 5
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
                "clue": "The Shadow Admin leaves cryptic messages on compromised systems."
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
                "clue": "The Shadow Admin uses custom tools to move through the cloud undetected."
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
                "time": 1
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
            initial_skills = {"network": 2, "cloud": 1}
            specialty = "Network Engineer"
        elif choice == 3:
            initial_skills = {"database": 2, "serverless": 1}
            specialty = "Database Administrator"
        else:
            initial_skills = {"cloud": 2, "security": 1}
            specialty = "DevOps Engineer"

        # Create the player
        self.player = CloudRanger(name, specialty, initial_skills)

        # Set initial location to Cloud City
        self.player.current_location = self.locations["Cloud City"]

        # Give tutorial quest
        self.player.active_quests.append(self.quests["tutorial"])

        # Set game parameters based on difficulty
        if self.difficulty == "easy":
            self.player.cloud_credits = 200
            self.player.time_left = 30
        elif self.difficulty == "normal":
            self.player.cloud_credits = 100
            self.player.time_left = 25
        else:  # hard
            self.player.cloud_credits = 50
            self.player.time_left = 20

        print(f"\n{CLR_SUCCESS}Character created! Welcome, {self.player.name} the {self.player.specialty}!{CLR_RESET}")
        input("\nPress Enter to begin your adventure...")

        # Start the game loop
        self.game_loop() if self.player else None

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
        # Check quest progress
        for quest in self.player.active_quests:
            # Check quest objectives
            current_loc_name = self.player.current_location.name

            # Tutorial quest objectives
            if quest.id == "tutorial":
                if current_loc_name == "Cloud City":
                    quest.complete_objective("tutorial_1")
                if len(self.player.artifacts) > 0:
                    quest.complete_objective("tutorial_2")
                if len(self.player.deployed_services) > 0:
                    quest.complete_objective("tutorial_3")

            # Mysterious outage quest objectives
            if quest.id == "mysterious_outage":
                if current_loc_name == "Database District":
                    quest.complete_objective("outage_1")
                if "outage_2" in self.player.clues:
                    quest.complete_objective("outage_2")
                if "outage_3" in self.player.clues:
                    quest.complete_objective("outage_3")
                if current_loc_name == "Security Perimeter" and "outage_3" in self.player.clues:
                    quest.complete_objective("outage_4")

            # Check if quest is completed
            if quest.check_completion():
                # Apply rewards
                self.apply_quest_reward(quest)
                # Remove from active quests
                self.player.completed_quests.append(quest.id)
                self.player.active_quests.remove(quest)

                print(f"\n{CLR_SUCCESS}Quest Completed: {quest.title}{CLR_RESET}")
                quest.display()
                input(PRESS_ENTER)

    def apply_quest_reward(self, quest):
        """Apply quest rewards to the player."""
        if 'credits' in quest.reward:
            self.player.cloud_credits += quest.reward['credits']

        if 'skill' in quest.reward:
            for skill, amount in quest.reward['skill'].items():
                self.player.increase_skill(skill, amount)

        if 'reputation' in quest.reward:
            self.player.reputation += quest.reward['reputation']

        if 'artifacts' in quest.reward:
            for artifact_name in quest.reward['artifacts']:
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

        if 'time' in quest.reward:
            self.player.time_left += quest.reward['time']

    def check_events(self):
        """Check and trigger random events at the current location."""
        current_location = self.player.current_location

        for event_id in current_location.events:
            if event_id in self.events:
                event = self.events[event_id]
                if event.can_trigger(self.player):
                    event.trigger(self.player)
                    input("\nPress Enter to continue...")

    def display_status(self):
        """Display player status and game information."""
        clear_screen()
        print(f"\n{CLR_TITLE}╔══════ CLOUD RANGER STATUS ══════╗{CLR_RESET}")
        print(f"{CLR_TITLE}║{CLR_RESET} {self.player.name} - {self.player.specialty}")
        print(f"{CLR_TITLE}║{CLR_RESET} Cloud Credits: {self.player.cloud_credits}")
        print(f"{CLR_TITLE}║{CLR_RESET} Reputation: {self.player.reputation}")
        print(
            f"{CLR_TITLE}║{CLR_RESET} Day: {self.current_day}/{self.player.time_left}")

        # Display skills
        print(f"{CLR_TITLE}╠══════ SKILLS ══════╣{CLR_RESET}")
        for skill, level in self.player.skill_levels.items():
            print(f"{CLR_TITLE}║{CLR_RESET} {skill.capitalize()}: {level}")

        print(f"{CLR_TITLE}╚═════════════════════════╝{CLR_RESET}")

    def display_actions(self):
        """Display available actions to the player."""
        print(f"\n{CLR_INTERACTION}Available Actions:{CLR_RESET}")
        print("1. Explore Location")
        print("2. Travel")
        print("3. View Quests")
        print("4. View Inventory")
        print("5. Deploy Service")
        print("6. Use Artifact")
        print("7. Rest (skip day)")
        print("8. Save Game")
        print("9. Quit Game")

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
            self.view_inventory()
        elif choice == 5:
            self.deploy_service()
        elif choice == 6:
            self.use_artifact()
        elif choice == 7:
            self.rest()
        elif choice == 8:
            self.save_game()
        elif choice == 9:
            self.confirm_quit()

    def explore_location(self):
        """Explore the current location for discoveries."""
        print_slow(f"\nExploring {self.player.current_location.name}...")

        # Check for special discoveries based on skills
        discovery_chance = 30 + \
            (self.player.skill_levels.get("investigation", 0) * 5)
        if random.randint(1, 100) <= discovery_chance:
            # Generate a discovery
            discovery_type = random.choice(
                ["artifact", "clue", "credits", "service"])

            if discovery_type == "artifact" and random.randint(1, 100) <= 30:
                # Find a random artifact
                artifact_name = random.choice(list(self.artifacts.keys()))
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

            elif discovery_type == "clue":
                clue_id = f"clue_{random.randint(1000, 9999)}"
                clue_text = f"You found evidence of unusual activity in {self.player.current_location.name}."

                self.player.add_clue(clue_id)
                print(f"\n{CLR_SUCCESS}You discovered a clue!{CLR_RESET}")
                print(f"{clue_text}")

            elif discovery_type == "credits":
                credits_found = random.randint(10, 50)
                self.player.cloud_credits += credits_found
                print(
                    f"\n{CLR_SUCCESS}You found {credits_found} Cloud Credits!{CLR_RESET}")

            elif discovery_type == "service":
                # Find a random service
                service_name = random.choice(list(self.services.keys()))
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
        else:
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
            print(f"{i}. {destination}")
        print(f"{len(current_location.connections) + 1}. Cancel")

        choice = get_valid_input("\nEnter your choice: ", range(
            1, len(current_location.connections) + 2))

        if choice == len(current_location.connections) + 1:
            print("Travel canceled.")
            return

        destination_name = current_location.connections[choice - 1]
        destination = self.locations[destination_name]

        # Check if player can travel to this location
        if destination.difficulty > max(self.player.skill_levels.values()) + 2:
            print(
                f"\n{CLR_ERROR}This location is too dangerous for your current skill level!{CLR_RESET}")
            print(
                f"You need more experience before traveling to {destination_name}.")
            input("\nPress Enter to continue...")
            return

        # Travel successful
        self.player.current_location = destination

        # Travel takes time
        self.current_day += 1
        print(f"\n{CLR_SUCCESS}You have arrived at {destination_name}.{CLR_RESET}")
        input("\nPress Enter to continue...")

    def view_quests(self):
        """View active and available quests."""
        print(f"\n{CLR_SECTION}[ACTIVE QUESTS]{CLR_RESET}")

        if not self.player.active_quests:
            print("You have no active quests.")
        else:
            for i, quest in enumerate(self.player.active_quests, 1):
                print(f"{i}. {quest.title}")

            print("\nSelect a quest to view details (0 to return):")
            choice = get_valid_input("Enter quest number: ", range(
                0, len(self.player.active_quests) + 1))

            if choice > 0:
                self.player.active_quests[choice - 1].display()

        # Check for available quests at this location
        current_loc = self.player.current_location.name
        available_quests = []

        # Logic to determine available quests based on location and player progress
        if current_loc == "Database District" and "mysterious_outage" not in self.player.active_quests and "mysterious_outage" not in self.player.completed_quests:
            available_quests.append(self.quests["mysterious_outage"])

        if current_loc == "Cache Cove" and "data_recovery" not in self.player.active_quests and "data_recovery" not in self.player.completed_quests:
            available_quests.append(self.quests["data_recovery"])

        if current_loc == "Serverless Valley" and "serverless_pioneer" not in self.player.active_quests and "serverless_pioneer" not in self.player.completed_quests:
            available_quests.append(self.quests["serverless_pioneer"])

        if current_loc == "Security Perimeter" and "secure_the_perimeter" not in self.player.active_quests and "secure_the_perimeter" not in self.player.completed_quests:
            available_quests.append(self.quests["secure_the_perimeter"])

        # Display available quests
        if available_quests:
            print(f"\n{CLR_SECTION}[AVAILABLE QUESTS]{CLR_RESET}")
            for i, quest in enumerate(available_quests, 1):
                print(f"{i}. {quest.title}")

            print("\nAccept a quest (0 to return):")
            choice = get_valid_input(
                "Enter quest number: ", range(0, len(available_quests) + 1))

            if choice > 0:
                selected_quest = available_quests[choice - 1]
                self.player.active_quests.append(selected_quest)
                print(
                    f"\n{CLR_SUCCESS}Quest accepted: {selected_quest.title}{CLR_RESET}")
                selected_quest.display()

        input("\nPress Enter to continue...")

    def view_inventory(self):
        """View artifacts and services in inventory."""
        print(f"\n{CLR_SECTION}[INVENTORY]{CLR_RESET}")

        # Artifacts
        print(
            f"\n{CLR_INTERACTION}Artifacts ({len(self.player.artifacts)}):{CLR_RESET}")
        if not self.player.artifacts:
            print("No artifacts in inventory.")
        else:
            for i, artifact in enumerate(self.player.artifacts, 1):
                print(
                    f"{i}. {artifact.name} (Type: {artifact.artifact_type}, Power: {artifact.power})")

        # Services
        print(
            f"\n{CLR_INTERACTION}Available Services ({len(self.player.services)}):{CLR_RESET}")
        if not self.player.services:
            print("No services available.")
        else:
            for i, service in enumerate(self.player.services, 1):
                print(
                    f"{i}. {service.name} (Type: {service.service_type}, Cost: {service.deploy_cost} credits)")

        # Deployed Services
        print(
            f"\n{CLR_INTERACTION}Deployed Services ({len(self.player.deployed_services)}):{CLR_RESET}")
        if not self.player.deployed_services:
            print("No services deployed.")
        else:
            for i, service in enumerate(self.player.deployed_services, 1):
                print(
                    f"{i}. {service.name} (Type: {service.service_type}, Region: {service.region})")

        # Clues
        print(f"\n{CLR_INTERACTION}Clues ({len(self.player.clues)}):{CLR_RESET}")
        if not self.player.clues:
            print("No clues collected.")
        else:
            for i, clue_id in enumerate(self.player.clues, 1):
                # In a full implementation, you'd have a clue database with descriptions
                print(f"{i}. Clue #{clue_id}")

        input("\nPress Enter to continue...")

    def deploy_service(self):
        """Deploy a service to the cloud."""
        print(f"\n{CLR_SECTION}[DEPLOY SERVICE]{CLR_RESET}")

        if not self.player.services:
            print("You don't have any services to deploy.")
            input("\nPress Enter to continue...")
            return

        print("Choose a service to deploy:")
        for i, service in enumerate(self.player.services, 1):
            print(f"{i}. {service.name} (Cost: {service.deploy_cost} credits)")
        print(f"{len(self.player.services) + 1}. Cancel")

        choice = get_valid_input("\nEnter your choice: ", range(
            1, len(self.player.services) + 2))

        if choice == len(self.player.services) + 1:
            print("Deployment canceled.")
            return

        selected_service = self.player.services[choice - 1]

        # Check if player has enough credits
        if self.player.cloud_credits < selected_service.deploy_cost:
            print(
                f"\n{CLR_ERROR}You don't have enough Cloud Credits to deploy this service.{CLR_RESET}")
            input("\nPress Enter to continue...")
            return

        # Check dependencies
        for dependency in selected_service.dependencies:
            has_dependency = False
            for deployed in self.player.deployed_services:
                if deployed.name == dependency:
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
        deployed_service.region = current_region
        self.player.deployed_services.append(deployed_service)
        self.player.services.remove(selected_service)

        print(
            f"\n{CLR_SUCCESS}Successfully deployed {deployed_service.name} in {current_region}!{CLR_RESET}")

        # Deployment takes time
        self.current_day += 1
        input("\nPress Enter to continue...")

    def use_artifact(self):
        """Use an artifact."""
        print(f"\n{CLR_SECTION}[USE ARTIFACT]{CLR_RESET}")

        if not self.player.artifacts:
            print("You don't have any artifacts to use.")
            input("\nPress Enter to continue...")
            return

        print("Choose an artifact to use:")
        for i, artifact in enumerate(self.player.artifacts, 1):
            print(
                f"{i}. {artifact.name} (Type: {artifact.artifact_type}, Power: {artifact.power})")
        print(f"{len(self.player.artifacts) + 1}. Cancel")

        choice = get_valid_input("\nEnter your choice: ", range(
            1, len(self.player.artifacts) + 2))

        if choice == len(self.player.artifacts) + 1:
            print("Artifact use canceled.")
            return

        selected_artifact = self.player.artifacts[choice - 1]

        # Simulate artifact use based on type
        print_slow(f"\nUsing {selected_artifact.name}...")

        if selected_artifact.artifact_type == "Scanner":
            # Scanner discovers clues and hidden services
            print(
                f"\nScanning {self.player.current_location.name} for hidden information...")

            # Higher chance based on artifact power
            discovery_chance = 30 + (selected_artifact.power * 10)

            if random.randint(1, 100) <= discovery_chance:
                discovery_type = random.choice(["clue", "service", "credits"])

                if discovery_type == "clue":
                    # Discovery may be related to quests
                    if self.player.current_location.name == "Database District" and any(q.id == "mysterious_outage" for q in self.player.active_quests):
                        clue_id = "outage_2"
                        clue_text = "Scanner found evidence of deliberate database corruption."
                    elif self.player.current_location.name == "Security Perimeter" and any(q.id == "mysterious_outage" for q in self.player.active_quests):
                        clue_id = "outage_3"
                        clue_text = "Scanner found unauthorized access logs to critical systems."
                    else:
                        clue_id = f"scanner_clue_{random.randint(1000, 9999)}"
                        clue_text = f"Scanner detected unusual activities in {self.player.current_location.name}."

                    self.player.add_clue(clue_id)
                    print(
                        f"\n{CLR_SUCCESS}Scanner discovered a clue!{CLR_RESET}")
                    print(clue_text)

                elif discovery_type == "service":
                    # Find a random service
                    available_services = [s for s in self.services.keys(
                    ) if s not in [x.name for x in self.player.services]]
                    if available_services:
                        service_name = random.choice(available_services)
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
                            f"\n{CLR_SUCCESS}Scanner discovered {new_service.name} service!{CLR_RESET}")
                        print(f"{new_service.description}")

                        self.player.add_service(new_service)
                    else:
                        print("\nScanner found nothing of interest.")

                elif discovery_type == "credits":
                    credits_found = random.randint(
                        20, 50) * selected_artifact.power
                    self.player.cloud_credits += credits_found
                    print(
                        f"\n{CLR_SUCCESS}Scanner found {credits_found} Cloud Credits!{CLR_RESET}")
            else:
                print("\nScanner found nothing of interest.")

        elif selected_artifact.artifact_type == "Analyzer":
            # Analyzers improve skills temporarily
            skill_boost = selected_artifact.power
            boost_duration = 3  # days

            # Choose a random skill to boost
            available_skills = list(self.player.skill_levels.keys())
            boosted_skill = random.choice(available_skills)

            print(f"\n{CLR_SUCCESS}The {selected_artifact.name} boosts your {boosted_skill} skill by {skill_boost} for {boost_duration} days!{CLR_RESET}")

            # In a full implementation, you would track temporary skill boosts
            self.player.temp_skill_boosts.append({
                "skill": boosted_skill,
                "amount": skill_boost,
                "remaining_days": boost_duration
            })

        elif selected_artifact.artifact_type == "Tool":
            # Tools help with specific tasks
            print(
                f"\n{CLR_SUCCESS}You use the {selected_artifact.name} to optimize your current tasks.{CLR_RESET}")

            # Random benefit
            benefit = random.choice(["credits", "time", "reputation"])

            if benefit == "credits":
                credits_saved = selected_artifact.power * 15
                self.player.cloud_credits += credits_saved
                print(
                    f"You saved {credits_saved} Cloud Credits through optimization!")

            elif benefit == "time":
                time_saved = 1  # day
                print(f"You saved {time_saved} day through efficient work!")
                self.current_day -= time_saved
                if self.current_day < 1:
                    self.current_day = 1

            elif benefit == "reputation":
                rep_gained = selected_artifact.power * 2
                self.player.reputation += rep_gained
                print(
                    f"Your efficient work earned you {rep_gained} additional reputation!")

        elif selected_artifact.artifact_type == "Archive":
            # Archives contain knowledge that improves skills permanently
            print(
                f"\n{CLR_SUCCESS}You study the {selected_artifact.name} and gain valuable knowledge.{CLR_RESET}")

            # Choose a skill to improve based on the archive
            if selected_artifact.name == "CloudFormation Architect":
                skill_to_improve = "cloud"
            elif selected_artifact.name == "IAM Auditor":
                skill_to_improve = "security"
            elif selected_artifact.name == "Aurora Analyzer":
                skill_to_improve = "database"
            elif selected_artifact.name == "Lambda Invoker":
                skill_to_improve = "serverless"
            else:
                # Random skill improvement
                skill_to_improve = random.choice(
                    list(self.player.skill_levels.keys()))

            improvement = selected_artifact.power
            self.player.increase_skill(skill_to_improve, improvement)
            print(
                f"Your {skill_to_improve} skill has permanently increased by {improvement}!")

            # Archives are consumed on use
            self.player.artifacts.remove(selected_artifact)
            print("The archive has been consumed.")

        else:
            print(
                f"You use the {selected_artifact.name} but nothing interesting happens.")

        # Using artifacts takes time
        self.current_day += 1
        input("\nPress Enter to continue...")

    def rest(self):
        """Rest for a day to recover resources."""
        print_slow("\nYou take some time to rest and recharge...")

        # Recover resources or special effects
        recovery_amount = 10 + (self.player.skill_levels.get("cloud", 0) * 2)
        self.player.cloud_credits += recovery_amount

        print(
            f"\n{CLR_SUCCESS}You recovered {recovery_amount} Cloud Credits.{CLR_RESET}")

        # Check for special recovery events
        if random.randint(1, 100) <= 20:
            # Special recovery - skill improvement
            skill = random.choice(list(self.player.skill_levels.keys()))
            self.player.increase_skill(skill, 1)
            print(
                f"\n{CLR_SUCCESS}While resting, you had an insight about {skill}. Your skill increased by 1!{CLR_RESET}")

        # Resting takes time
        self.current_day += 1
        input("\nPress Enter to continue...")

    def save_game(self):
        """Save the current game state."""
        print_slow("\nSaving game...")

        # In a full implementation, you would serialize the game state to a file
        # For this demo, we'll simulate saving
        print(f"\n{CLR_SUCCESS}Game saved successfully!{CLR_RESET}")
        input("\nPress Enter to continue...")

    def confirm_quit(self):
        """Confirm if the player wants to quit."""
        print("\nAre you sure you want to quit the game? Unsaved progress will be lost.")
        print("1. Yes, quit game")
        print("2. No, continue playing")

        choice = get_valid_input("\nEnter your choice (1-2): ", range(1, 3))

        if choice == 1:
            self.game_over = True
        else:
            print("\nReturning to game...")

    def check_game_over(self):
        """Check win/lose conditions."""
        # Win condition: Complete Shadow Admin quest
        if "shadow_admin" in self.player.completed_quests:
            self.win_reason = "You have unmasked the Shadow Admin and saved Cloud City!"
            return True

        # Lose condition: Out of time
        if self.current_day > self.player.time_left:
            self.win_reason = "You have run out of time! The Shadow Admin's plans have succeeded."
            return True

        return False

    def end_game(self):
        """End the game and display final stats."""
        clear_screen()

        if "shadow_admin" in self.player.completed_quests:
            print(
                f"\n{CLR_TITLE}╔══════════════════════════════════════════════════════════╗{CLR_RESET}")
            print(
                f"{CLR_TITLE}║                       VICTORY!                           ║{CLR_RESET}")
            print(
                f"{CLR_TITLE}╚══════════════════════════════════════════════════════════╝{CLR_RESET}")
        else:
            print(
                f"\n{CLR_TITLE}╔══════════════════════════════════════════════════════════╗{CLR_RESET}")
            print(
                f"{CLR_TITLE}║                      GAME OVER                           ║{CLR_RESET}")
            print(
                f"{CLR_TITLE}╚══════════════════════════════════════════════════════════╝{CLR_RESET}")

        print(f"\n{self.win_reason}")

        # Display final stats
        print(f"\n{CLR_SECTION}[FINAL STATS]{CLR_RESET}") if self.player else None
        print(f"Days played: {self.current_day}")
        print(f"Cloud Credits: {self.player.cloud_credits}")
        print(f"Reputation: {self.player.reputation}")
        print(f"Completed Quests: {len(self.player.completed_quests)}")

        # Display skill levels
        print(f"\n{CLR_SECTION}[FINAL SKILLS]{CLR_RESET}")
        for skill, level in self.player.skill_levels.items() if self.player else []:
            print(f"{skill.capitalize()}: {level}")

        print("\nThank you for playing Cloud Ranger: Digital Frontier!")
        input("\nPress Enter to exit...")


# Common message constants
PRESS_ENTER = "\nPress Enter to continue..."

# Color constants
CLR_SUCCESS = "\033[1;32m"  # Bright Green for success messages
CLR_ERROR = "\033[1;31m"  # Bright Red for error messages
CLR_INTERACTION = "\033[1;33m"  # Bright Yellow for interactive elements

# Helper functions




def get_valid_input(prompt, valid_range):
    """Get valid input from the user within a specified range."""
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_range:
                return choice
            else:
                print(
                    f"Please enter a number between {min(valid_range)} and {max(valid_range)}.")
        except ValueError:
            print("Please enter a valid number.")


# Main function to start the game
def main():
    clear_screen()
    print(f"{CLR_TITLE}╔══════════════════════════════════════════════════════════╗{CLR_RESET}")
    print(f"{CLR_TITLE}║            CLOUD RANGER: DIGITAL FRONTIER                ║{CLR_RESET}")
    print(f"{CLR_TITLE}║                  THE NEON SHADOW                         ║{CLR_RESET}")
    print(f"{CLR_TITLE}╚══════════════════════════════════════════════════════════╝{CLR_RESET}")

    print_slow("\nWelcome to Cloud Ranger: Digital Frontier!")
    print_slow(
        "In this cyberpunk cloud computing adventure, you'll protect the digital world.")

    # Select difficulty
    print("\nSelect difficulty:")
    print("1. Easy (More credits, more time)")
    print("2. Normal")
    print("3. Hard (Fewer credits, less time)")

    difficulty_choice = get_valid_input(
        "Enter your choice (1-3): ", range(1, 4))

    if difficulty_choice == 1:
        difficulty = "easy"
    elif difficulty_choice == 2:
        difficulty = "normal"
    else:
        difficulty = "hard"

    # Create and start the game
    game = Game()
    game._create_locations()
    game.start_game()


# Run the game if executed directly
if __name__ == "__main__":
    main()
