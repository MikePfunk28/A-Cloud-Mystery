# Assume colorama is initialized: colorama.init(autoreset=True)
import os
from colorama import Fore, Back, Style

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_location_hub(location_name, description, available_sub_locations):
    clear_screen()
    print(f"{Style.BRIGHT + Fore.MAGENTA}=== {location_name} ===")
    print(f"{Fore.YELLOW}{description}{Style.RESET_ALL}\n")

    # ASCII Art for Neo-Kyoto (Example)
    print(f"{Fore.CYAN}  /\\                                                  /\\")
    print(f"{Fore.CYAN} /  \\{Fore.WHITE}  .--.     {Fore.MAGENTA} ____                       {Fore.WHITE}.--.     {Fore.CYAN}/  \\")
    print(f"{Fore.CYAN}/____\\ {Fore.WHITE} |  | {Fore.YELLOW} ___ {Fore.MAGENTA}|    \\ {Fore.WHITE} ___ {Fore.CYAN} ___  {Fore.WHITE} ___ |  |    {Fore.CYAN}/____\\")
    print(f"{Fore.CYAN}|    | {Fore.WHITE} | {Style.BRIGHT + Fore.RED}O{Style.RESET_ALL + Fore.WHITE} |{Fore.YELLOW}|   |{Fore.MAGENTA}|     \\{Fore.WHITE}| - |{Fore.CYAN}|   ||{Fore.WHITE}| - |{Style.BRIGHT + Fore.RED}O{Style.RESET_ALL + Fore.WHITE} |   {Fore.CYAN}|    |")
    print(f"{Fore.CYAN}|    | {Fore.WHITE} |  | {Fore.YELLOW}|___|{Fore.MAGENTA}|__|\\__\\{Fore.WHITE}|___|{Fore.CYAN}|__/|{Fore.WHITE}|___||  |   {Fore.CYAN}|    |")
    print(f"{Fore.CYAN}|____| {Fore.WHITE} '==' {Fore.YELLOW}     {Fore.MAGENTA}      {Fore.WHITE}     {Fore.CYAN}    {Fore.WHITE}    '=='   {Fore.CYAN}|____|")
    print(f"{Fore.GREEN}~~~~~~~~~~~~~~~~~~ {Fore.BLUE}Digital River District{Fore.GREEN} ~~~~~~~~~~~~~~~~~~{Style.RESET_ALL}\n")


    print(f"{Style.BRIGHT + Fore.WHITE}Places of Interest:{Style.RESET_ALL}")
    for i, sub_loc in enumerate(available_sub_locations):
        status = f"[{Fore.GREEN}Visited{Style.RESET_ALL}]" if sub_loc['visited'] else ""
        print(f" {i+1}. {Fore.CYAN}{sub_loc['name']}{Style.RESET_ALL} - {sub_loc['short_desc']} {status}")

    print(f"\nActions: [1-{len(available_sub_locations)}] Investigate, [T]ravel Hub, [H]Q Access, [S]tatus")

# --- Game Data for Neo-Kyoto ---
neo_kyoto_desc = "Neon signs reflect off rain-slicked streets. Data streams pulse visibly in the augmented reality overlay. Home to cutting-edge tech and ancient traditions."

neo_kyoto_sub_locations = [
    {'id': 'nk_market', 'name': "Akihabara Datastream Market", 'short_desc': "Bustling digital marketplace.", 'visited': False, 'clues': [], 'interactions': ['talk_merchant', 'scan_network']},
    {'id': 'nk_shrine', 'name': "Serenity Cache Shrine", 'short_desc': "An old shrine with surprising network access.", 'visited': False, 'clues': [], 'interactions': ['examine_server', 'talk_monk']},
    {'id': 'nk_corp', 'name': "YamaTech Tower Lobby", 'short_desc': "Gleaming corporate headquarters.", 'visited': False, 'clues': [], 'interactions': ['talk_receptionist', 'check_visitor_log']},
    {'id': 'nk_noodles', 'name': "Ramen Runner Noodle Shop", 'short_desc': "A local favorite, good for info.", 'visited': False, 'clues': [], 'interactions': ['talk_owner', 'check_public_terminal']}
]

# --- Player State Addition ---
# player.known_clues = {} # Dictionary to store clues found, maybe {'location_id': ['clue text 1', 'clue text 2']}
# player.visited_sub_locations = set() # Store IDs like 'nk_market'