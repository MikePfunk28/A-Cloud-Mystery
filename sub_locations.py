def display_sub_location(sub_loc_data, player):
    clear_screen()
    print(f"{Style.BRIGHT + Fore.CYAN}--- {sub_loc_data['name']} ---{Style.RESET_ALL}")

    # ASCII Art for the Market (Example)
    print(f"{Fore.YELLOW}  _________________________")
    print(f" | {Fore.MAGENTA}[][]{Style.BRIGHT + Fore.WHITE} SERVER PARTS {Fore.MAGENTA}[][]{Style.RESET_ALL}{Fore.YELLOW} | ")
    print(f" | {Fore.CYAN}//==\\\\ VIRTUAL RAM //==\\\\{Style.RESET_ALL}{Fore.YELLOW} | ")
    print(f" | {Fore.GREEN} (( $$ )) {Fore.RED} HOT NOODLES {Fore.GREEN}(( $$ )){Style.RESET_ALL}{Fore.YELLOW} | ")
    print(f" | {Fore.WHITE}  \\\\==// {Style.DIM} Data Streams {Fore.WHITE} \\\\==//{Style.RESET_ALL}{Fore.YELLOW} | ")
    print(f" |_________[ {Fore.BLUE} Booth #7 {Style.RESET_ALL}{Fore.YELLOW}]_________| ")
    print(f"   \\_______________________/")
    print(f"    {Fore.GREEN}人{Style.RESET_ALL}   {Fore.MAGENTA}人{Style.RESET_ALL}       {Fore.CYAN}人{Style.RESET_ALL}    {Fore.WHITE}人{Style.RESET_ALL}") # People icons
    print(f"{Style.DIM}A cacophony of digital hawkers and flickering signs.{Style.RESET_ALL}\n")

    available_actions = sub_loc_data['interactions']
    print(f"{Style.BRIGHT + Fore.WHITE}Available Actions:{Style.RESET_ALL}")
    action_map = {}
    for i, action_id in enumerate(available_actions):
        action_desc = get_action_description(action_id, player) # Function to get user-friendly text
        print(f" {i+1}. {Fore.GREEN}{action_desc}{Style.RESET_ALL}")
        action_map[str(i+1)] = action_id

    print(f"\n[B]ack to {current_location_name} Hub")
    return action_map # Return map of number to action_id for processing input

def get_action_description(action_id, player):
    # This function translates action IDs to user text, potentially checking player skills/items
    if action_id == 'talk_merchant':
        return "Talk to the eccentric merchant at Booth #7"
    elif action_id == 'scan_network':
        # Check if player has a relevant artifact/skill
        if player_has_artifact(player, "Network Scanner"):
             return "Use Network Scanner on market Wi-Fi"
        else:
             return f"{Style.DIM}Scan market Wi-Fi (Requires Network Scanner Artifact){Style.RESET_ALL}"
    elif action_id == 'examine_server':
        return "Examine the ancient server rack"
    elif action_id == 'talk_monk':
        return "Speak with the cyber-monk"
    # Add descriptions for all other action_ids...
    else:
        return action_id # Fallback

def player_has_artifact(player, artifact_name):
     # Simple check
     return any(a.name == artifact_name for a in player.inventory + player.architecture)