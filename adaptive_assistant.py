import os
import time
import random
import sys

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
    CLR_BACK_RED = ""
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

# --- Helper Functions ---


def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_slow(text, delay=0.03, color=CLR_RESET):
    """Prints text character by character with optional color."""
    for char in text:
        sys.stdout.write(color + char + CLR_RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Newline at the end


def display_ascii_art(art, color=CLR_WHITE):
    """Prints multi-line ASCII art string with specified color."""
    print(color)
    print(art)
    print(CLR_RESET)

# --- Core Classes ---


class CloudArtifact:
    """Represents an AWS service or tool the player can use."""

    def __init__(self, name, description, artifact_type, cost=0):
        self.name = name
        self.description = description
        # e.g., 'Scanner', 'Firewall', 'Database', 'Compute'
        self.artifact_type = artifact_type
        self.cost = cost  # Optional Cloud Credit cost to use

    def __str__(self):
        return f"{CLR_ARTIFACT}{self.name}{CLR_RESET} ({self.artifact_type})"


class Player:
    """Holds player state."""

    def __init__(self, name="Ranger"):
        self.name = name
        self.cloud_credits = 500  # Starting currency
        self.bandwidth = 100      # Starting bandwidth
        self.time_left = 365      # Days remaining
        self.inventory = []       # List of CloudArtifact objects
        self.clues = set()        # Set of discovered clue IDs

    def add_artifact(self, artifact):
        if artifact not in self.inventory:
            self.inventory.append(artifact)
            print(f"{CLR_SUCCESS}Acquired artifact: {artifact}{CLR_RESET}")
            time.sleep(1)

    def has_artifact(self, artifact_name):
        return any(a.name == artifact_name for a in self.inventory)

    def add_clue(self, clue_id):
        if clue_id not in self.clues:
            self.clues.add(clue_id)
            print(f"{CLR_CLUE}New Clue Added! ({clue_id}){CLR_RESET}")
            time.sleep(1.5)

    def display_status(self):
        print("\n--- Status ---")
        print(f" Credits: {CLR_YELLOW}{self.cloud_credits}{CLR_RESET}")
        print(f" Bandwidth: {CLR_BLUE}{self.bandwidth}{CLR_RESET}")
        print(f" Time Left: {CLR_CYAN}{self.time_left} days{CLR_RESET}")
        inv = ', '.join(str(a)
                        for a in self.inventory) if self.inventory else 'Empty'
        print(f" Inventory: {inv}")
        print(f" Clues: {len(self.clues)} collected")
        print("--------------")
        input(f"{CLR_PROMPT}Press Enter to continue...{CLR_RESET}")


class LocationNode:
    """Represents an interactable location within the game world."""

    def __init__(self, node_id, name, description, ascii_art="", connections=None, interactions=None):
        self.node_id = node_id  # Unique ID
        self.name = name
        self.description = description
        self.ascii_art = ascii_art
        # e.g., {'north': 'target_node_id'}
        self.connections = connections if connections else {}
        # Interactions: list of dicts with 'id', 'name', 'action', 'completed', and optional 'requires_artifact'
        self.interactions = interactions if interactions else []

    def display(self):
        clear_screen()
        if self.ascii_art:
            display_ascii_art(self.ascii_art, CLR_LOCATION_DESC)
        print(f"{CLR_LOCATION_NAME}--- {self.name} ---{CLR_RESET}")
        print(CLR_LOCATION_DESC + self.description + CLR_RESET)
        print("-" * (len(self.name) + 8))
        print("\nNearby Locations:")
        if self.connections:
            for direction, target in self.connections.items():
                print(
                    f" [{direction[0].upper()}] {direction.capitalize()} -> {target.replace('_', ' ').title()}")
        else:
            print(" None")
        print("\nInteractions:")
        available = [i for i in self.interactions if not i.get(
            'completed', False)]
        if available:
            for idx, inter in enumerate(available):
                req = f" (Requires: {CLR_ARTIFACT}{inter['requires_artifact']}{CLR_INTERACTION})" if inter.get(
                    'requires_artifact') else ""
                print(
                    f" [{idx+1}] {CLR_INTERACTION}{inter['name']}{req}{CLR_RESET}")
        else:
            print(" Nothing interactive here.")
        print("\nOther Actions:")
        print(" [S] Status")
        print(" [Q] Quit Game")


# --- Game Data ---
# Define starting artifacts
ARTIFACT_SCANNER = CloudArtifact(
    "Basic Network Scanner", "Scans local networks for open ports and device info.", "Scanner")
ARTIFACT_LOG_VIEWER = CloudArtifact(
    "CloudWatch Logs Viewer", "Interface to view system or application logs.", "Utility")
ARTIFACT_WAF_CONFIG = CloudArtifact(
    "WAF Rule Analyzer", "Analyzes and suggests Web Application Firewall rules.", "Security")

# Define Neo-Kyoto Location Nodes with ASCII art
NEO_KYOTO_LANDING_ART = r"""
   .-'''-.        ____                       .-'''-.
 .'   _   \     .'    '.   _              .'   _   \
/   /` '.   \  . H  .--./ .' ) ____      /   /` '.   \
.   | /  .`|  | | /||_|()|(   )_ \     .   | /  .`|  |
|   ' E = / |  | |// / | | '.'.'.') .-'|   ' E = / |  |
\    .-'  /   | | / /| | |( | | | / / \    .-'  /   |
 \ .-'  .'    | `-' / | |//| | \ `'.   \ .-'  .'    |
  '-'    /     `.`'.'/| | |)_ \ | |) /    '-'    /     |
       .'        `'-' \_\| / |/.' /'.     |'.'.' .---'|
      /                 '. \_/ .' .'      |'-' /    /
     /                   '. .. .' /       \ .'.'   .'
    /                      '''   /         '-'/    /
   /----------------------------/           \ '-' .'
  /============================/             `---`
 /________NEO-KYOTO_AIRPORT___/
"""

GIGACORP_PLAZA_ART = r"""
        _.--""--._
      .'          `.
     /   O      O   \
    |    \  ^^  /    |
    \     `----'     /
   /`-.          .-'\  
  /    `--.__.--'    \
 /                     \
|_______GIGACORP________|
 \ ][ ][ ][ ][ ][ ][ ] /--,
__||___________________|| L_)
(__|___________________|__)
"""

DATA_HAVEN_ART = r"""
       옥       옥       옥
    +-------+-------+-------+
    | [:::] | [:::] | [:::] |
    |       |       |       |
    |_______|_______|_______|
    |[ सर्वर]| [ सर्वर]| [ सर्वर]|
    +-------+-------+-------+
    | ##### | ##### | ##### |
   /________\________\________\
  //_______ DATA HAVEN _______\\
"""

WHISPERING_ALLEY_ART = r"""
  ||        || | || \   / ||
 /||\      /|| | ||\ \ / /||
| || | __ | || | || \ V / || |
 \|`-' / `\|| | || | > <| || |__
 /    ||   `' | || |/ / \ || '--'
|     ||      | || | / \ || |
\_____/|______\ /|_/_/ \_\_/ |______
      ||      || ||          ||
      ||______||_||__________||
 Neon Noodles || Lucky Cat Pawn
"""

# Define Interaction Functions


def investigate_landing_traffic(player, node):
    print_slow("\nAccessing the orbital port's network monitor...",
               delay=0.05, color=CLR_SYSTEM)
    if player.has_artifact("Basic Network Scanner"):
        print_slow(f"Using your {ARTIFACT_SCANNER.name}, you filter the noise...",
                   delay=0.05, color=CLR_INTERACTION)
        time.sleep(1.5)
        print_slow("Odd outbound packets detected... routing to GigaCorp district.",
                   delay=0.05, color=CLR_CLUE)
        player.add_clue("NK_Traffic_Anomaly")
        for inter in node.interactions:
            if inter['id'] == 'scan_traffic':
                inter['completed'] = True
    else:
        print_slow("The data stream is overwhelming. You need a Network Scanner.",
                   delay=0.05, color=CLR_YELLOW)
    input(f"{CLR_PROMPT}Press Enter...{CLR_RESET}")


def check_gigacorp_security_feed(player, node):
    print_slow("\nTapping into GigaCorp's public security feed...",
               delay=0.05, color=CLR_SYSTEM)
    time.sleep(1)
    print_slow("Scanning for anomalies...", delay=0.05, color=CLR_INTERACTION)
    time.sleep(1.5)
    print_slow("Flickering timestamp anomaly detected. Feed tampered around 03:00 JST.",
               delay=0.05, color=CLR_CLUE)
    player.add_clue("NK_Feed_Tamper")
    for inter in node.interactions:
        if inter['id'] == 'check_feed':
            inter['completed'] = True
    input(f"{CLR_PROMPT}Press Enter...{CLR_RESET}")


def examine_data_haven_logs(player, node):
    print_slow("\nAccessing terminal at Data Haven...",
               delay=0.05, color=CLR_SYSTEM)
    if player.has_artifact("CloudWatch Logs Viewer"):
        print_slow(f"Using {ARTIFACT_LOG_VIEWER.name} to filter logs...",
                   delay=0.05, color=CLR_INTERACTION)
        time.sleep(2)
        print_slow("Found unauthorized root access from IP: Whispering Alley?",
                   delay=0.05, color=CLR_CLUE)
        player.add_clue("NK_Root_Access_Alley")
        for inter in node.interactions:
            if inter['id'] == 'check_logs':
                inter['completed'] = True
    else:
        print_slow("Log format encrypted. You need a Logs Viewer artifact.",
                   delay=0.05, color=CLR_YELLOW)
    input(f"{CLR_PROMPT}Press Enter...{CLR_RESET}")


def analyze_waf_bypass(player, node):
    print_slow("\nInvestigating the noodle shop's ordering system compromise...",
               delay=0.05, color=CLR_SYSTEM)
    if player.has_artifact("WAF Rule Analyzer"):
        print_slow(
            f"Analyzing logs with {ARTIFACT_WAF_CONFIG.name}...", delay=0.05, color=CLR_INTERACTION)
        time.sleep(2)
        print_slow("SQL Injection bypassed weak WAF rules detected.",
                   delay=0.05, color=CLR_INTERACTION)
        print_slow("Suspicious payload attempted data extraction.",
                   delay=0.05, color=CLR_CLUE)
        player.add_clue("NK_SQLi_Attempt")
        for inter in node.interactions:
            if inter['id'] == 'analyze_waf':
                inter['completed'] = True
    else:
        print_slow("Firewall logs too complex. You need a WAF Rule Analyzer artifact.",
                   delay=0.05, color=CLR_YELLOW)
    input(f"{CLR_PROMPT}Press Enter...{CLR_RESET}")


# --- Create Location Nodes ---
NODES = {
    'neo_kyoto_landing': LocationNode(
        'neo_kyoto_landing',
        "Neo-Kyoto Orbital Port - Landing Zone",
        "The orbital port is abuzz with anti-grav traffic. Towering chrome structures and neon reflections set the stage.",
        NEO_KYOTO_LANDING_ART,
        connections={'north': 'gigacorp_plaza'},
        interactions=[{'id': 'scan_traffic', 'name': "Scan Network Traffic",
                       'action': investigate_landing_traffic, 'requires_artifact': "Basic Network Scanner"}]
    ),
    'gigacorp_plaza': LocationNode(
        'gigacorp_plaza',
        "GigaCorp Plaza",
        "A vast plaza dominated by a monolithic tower. Holographic ads flicker on synth-stone surfaces.",
        GIGACORP_PLAZA_ART,
        connections={'south': 'neo_kyoto_landing',
                     'east': 'data_haven_rooftops', 'west': 'whispering_alley'},
        interactions=[{'id': 'check_feed', 'name': "Check Security Feed",
                       'action': check_gigacorp_security_feed}]
    ),
    'data_haven_rooftops': LocationNode(
        'data_haven_rooftops',
        "Data Haven Rooftops",
        "A chaotic array of satellite dishes and server racks atop aging structures. Data flows like electricity.",
        DATA_HAVEN_ART,
        connections={'west': 'gigacorp_plaza'},
        interactions=[{'id': 'check_logs', 'name': "Examine Access Logs",
                       'action': examine_data_haven_logs, 'requires_artifact': "CloudWatch Logs Viewer"}]
    ),
    'whispering_alley': LocationNode(
        'whispering_alley',
        "Whispering Alley",
        "A narrow, rain-soaked alley filled with neon signs, noodle stalls, and clandestine whispers.",
        WHISPERING_ALLEY_ART,
        connections={'east': 'gigacorp_plaza'},
        interactions=[{'id': 'analyze_waf', 'name': "Analyze Noodle Shop WAF Logs",
                       'action': analyze_waf_bypass, 'requires_artifact': "WAF Rule Analyzer"}]
    ),
}

# --- Game Class ---


class Game:
    """Manages game state and loop."""

    def __init__(self):
        self.player = None
        self.current_node_id = None  # Start node ID will be set in intro
        self.nodes = NODES  # Loaded nodes
        self.is_running = False

    def display_intro(self):
        clear_screen()
        intro_art = r"""
        _________ _____ _________.___     ________      ________ __          __
        \_   ___ \\__  \\______   \   |   /  _____/     /  _____/|  | _____ _/  |_  ____  
        /    \  \/ /   | |    |  _/   |  /   \  ___    /   \  ___|  | \__  \\   __\/ __ \ 
        \     \___/   | |    |   \   |  \    \_\  \   \    \_\  \  |__/ __ \|  | \  ___/
         \______  /_______\______  /___|   \______  / /\ \______  /____(____  /__|  \___  >
                \/     /_____/  \/ \_________/     \/  /_____/ \/           \/          \/
        -- C L O U D   Q U E S T :   T H E   N E O N   S H A D O W --
        """
        display_ascii_art(intro_art, CLR_BRIGHT + CLR_CYAN)
        time.sleep(2)
        print_slow("Connecting secure channel...",
                   delay=0.05, color=CLR_SYSTEM)
        time.sleep(1)
        print_slow("> System Check... OK", delay=0.05, color=CLR_GREEN)
        print_slow("> Secure Channel... ESTABLISHED",
                   delay=0.05, color=CLR_GREEN)
        print_slow("> Location... Unknown Datastream",
                   delay=0.05, color=CLR_YELLOW)
        time.sleep(1)
        print_slow("\nVOICE (Dr. Aurora Server):",
                   color=CLR_BRIGHT + CLR_NARRATOR)
        print_slow(
            "Ranger... can you hear me? The network is unstable. Interference is strong.", color=CLR_NARRATOR)
        time.sleep(0.5)
        print_slow(
            "Something big just happened. Project Chimera... it's gone dark.", color=CLR_NARRATOR)
        time.sleep(0.5)
        print_slow(
            "The fragments are scattered... artifacts now. The Shadow Admin is hunting them too.", color=CLR_NARRATOR)
        time.sleep(1.5)
        display_ascii_art(r"""
           \ \ / /        (_) |
            \ V / ___ _ __ _| |_ ___ _ __
            /   \/ _ \ '__| | __/ _ \ '__|
           / /^\ \  __/ |  | | ||  __/ |
           \/   \/\___|_|  |_|\__\___|_|
        """, CLR_SHADOW_ADMIN)
        time.sleep(1.5)
        print_slow(
            "Your mission: Find the artifacts. Build countermeasures. Track the Shadow Admin.", color=CLR_NARRATOR)
        print_slow(
            "The trail starts in Neo-Kyoto... where the first fragment vanished.", color=CLR_NARRATOR)
        time.sleep(1.5)
        player_name = input(
            f"{CLR_PROMPT}Enter Your Ranger Handle: {CLR_PLAYER_INPUT}")
        self.player = Player(player_name if player_name else "Ranger")
        print_slow(
            f"\nVOICE (Dr. Aurora Server): Good luck, {self.player.name}. He remembers you.", color=CLR_NARRATOR)
        time.sleep(2)
        # Give starting artifacts
        self.player.add_artifact(ARTIFACT_SCANNER)
        self.player.add_artifact(ARTIFACT_LOG_VIEWER)
        self.current_node_id = 'neo_kyoto_landing'

    def start_game(self):
        self.display_intro()
        self.is_running = True
        self.main_loop()

    def get_current_node(self):
        return self.nodes.get(self.current_node_id)

    def main_loop(self):
        while self.is_running:
            current_node = self.get_current_node()
            if not current_node:
                print(
                    f"{CLR_ERROR}Error: Node '{self.current_node_id}' not found!{CLR_RESET}")
                self.is_running = False
                break

            current_node.display()
            prompt = f"\n{CLR_PROMPT}Action ([M]ove, [I]nteract #, [S]tatus, [Q]uit): {CLR_PLAYER_INPUT}"
            choice = input(prompt).upper().strip()
            print(CLR_RESET, end='')

            if choice == 'Q':
                print_slow("Exiting CloudQuest...", color=CLR_YELLOW)
                self.is_running = False
            elif choice == 'S':
                self.player.display_status()
            elif choice == 'M':
                move_choice = input(
                    f"{CLR_PROMPT}Move direction (N, S, E, W): {CLR_PLAYER_INPUT}").upper().strip()
                if not move_choice:
                    continue
                target_direction = ""
                if move_choice == 'N':
                    target_direction = 'north'
                elif move_choice == 'S':
                    target_direction = 'south'
                elif move_choice == 'E':
                    target_direction = 'east'
                elif move_choice == 'W':
                    target_direction = 'west'
                if target_direction in current_node.connections:
                    self.current_node_id = current_node.connections[target_direction]
                    print_slow(
                        f"Moving {target_direction}...", color=CLR_SYSTEM)
                    time.sleep(1)
                else:
                    print(f"{CLR_ERROR}Cannot move in that direction.{CLR_RESET}")
                    time.sleep(1)
            elif choice.startswith('I'):
                try:
                    interact_num_str = choice.replace('I', '').strip()
                    if not interact_num_str:
                        print(
                            f"{CLR_ERROR}Specify interaction number (e.g., I1).{CLR_RESET}")
                        time.sleep(1.5)
                        continue
                    interact_idx = int(interact_num_str) - 1
                    available = [i for i in current_node.interactions if not i.get(
                        'completed', False)]
                    if 0 <= interact_idx < len(available):
                        interaction = available[interact_idx]
                        required = interaction.get('requires_artifact')
                        if required and not self.player.has_artifact(required):
                            print(
                                f"{CLR_YELLOW}You need the {CLR_ARTIFACT}{required}{CLR_YELLOW} artifact to do that.{CLR_RESET}")
                            time.sleep(2)
                            continue
                        action_func = interaction.get('action')
                        if action_func:
                            action_func(self.player, current_node)
                        else:
                            print(
                                f"{CLR_YELLOW}Interaction '{interaction['name']}' not implemented yet.{CLR_RESET}")
                            time.sleep(1.5)
                    else:
                        print(
                            f"{CLR_ERROR}Invalid interaction number.{CLR_RESET}")
                        time.sleep(1)
                except ValueError:
                    print(
                        f"{CLR_ERROR}Invalid input for interaction number.{CLR_RESET}")
                    time.sleep(1)
                except Exception as e:
                    print(f"{CLR_ERROR}Error during interaction: {e}{CLR_RESET}")
                    time.sleep(2)
            else:
                print(f"{CLR_ERROR}Unknown command.{CLR_RESET}")
                time.sleep(1)


# --- Main Execution ---
if __name__ == "__main__":
    game = Game()
    try:
        game.start_game()
    except KeyboardInterrupt:
        print_slow("\n\nCtrl+C detected. Exiting game.", color=CLR_YELLOW)
    except Exception as e:
        clear_screen()
        print(f"{CLR_BRIGHT}{CLR_BACK_RED}--- FATAL ERROR ---{CLR_RESET}")
        print(f"{CLR_ERROR}An unexpected error occurred:")
        print(str(e))
        import traceback
        traceback.print_exc()
        print(f"{CLR_BRIGHT}{CLR_BACK_RED}-------------------{CLR_RESET}")
        print("\nPlease report this error.")
    finally:
        if 'colorama' in sys.modules:
            colorama.deinit()
        print("\nGame session ended.")
