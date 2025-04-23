"""
neon_shadow_game/                # Project root
├── neon_shadow/                 # Core package
│   ├── __init__.py              # Package initializer
# All global constants (CLR_*, GAME_CONSTANTS, etc.)
│   ├── constants.py
# Terminal/UI functions (clear_screen, print_slow, loading bars, animations)
│   ├── ui.py
# Generic helpers (confirmation, choice parsing, formatting)
│   ├── utils.py
│   ├── player.py                # Player and CloudRanger classes
│   ├── inventory.py             # Inventory class
│   ├── artifact.py              # CloudArtifact class
│   ├── service.py               # CloudService class
│   ├── event.py                 # CloudEvent class
│   ├── quest.py                 # Quest class
│   ├── location.py              # Location class
│   ├── content/                 # Static content definitions
│   │   ├── artifacts.py         # Template data for artifacts
│   │   ├── services.py          # Template data for services
│   │   ├── quests.py            # Template data for quests
│   │   ├── events.py            # Template data for events
│   │   ├── locations.py         # Template data for locations and hazards
│   │   ├── weather.py           # Weather condition definitions
│   │   └── vendors.py           # Vendor inventories
│   └── game.py                  # Game engine, world builder, main loop
├── main.py                      # Entry point: config, instantiate Game, start gameplay
├── tests/                       # Unit tests for each module
│   ├── test_player.py
│   ├── test_inventory.py
│   ├── test_artifact.py
|   ├── test_service.py
|   ├── test_event.py
|   ├── test_quest.py
|   ├── test_location.py
|   ├── test_content.py
|   ├── test_game.py
|   ├── test_ui.py
|   ├── test_utils.py
|   └── test_constants.py
|   └── test_vendors.py
|   └── test_weather.py
│   └── ...
└── requirements.txt             # External dependencies (e.g., colorama)


#--- constants.py - --

Global constants used throughout the Neon Shadow game.
"""


# Game constants
GAME_CONSTANTS = {
    'MAX_REPUTATION': 100,
    'MIN_REPUTATION': 0,
    'DEFAULT_SKILL_LEVEL': 1
}

# Type definitions
LocationType = dict  # Dict[str, Union[str, List[str], int]]
ReputationType = dict  # Dict[str, int]

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
