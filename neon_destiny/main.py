# main.py - Entry point for the Cloud Ranger game
import os
import sys
import traceback
from neon_shadow.game import Game
from neon_shadow.utils import get_valid_input
from neon_shadow.ui import clear_screen, display_ascii_art
from neon_shadow.constants import CLR_RESET, CLR_TITLE, CLR_ERROR


# Add the project root to Python's path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


def main():
    """Main function to start the game."""
    # Initialize colorama if available
    try:
        import colorama
        colorama.init(autoreset=True)
    except ImportError:
        print("Warning: Colorama library not installed. Colors will not display correctly.")
        sys.exit(1)

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
        print(f"\n\n{CLR_ERROR}An error occurred: {str(e)}{CLR_RESET}")
        if game.debug_mode:
            traceback.print_exc()

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
