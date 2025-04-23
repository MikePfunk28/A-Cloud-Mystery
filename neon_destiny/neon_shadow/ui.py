"""
UI related functions for the Neon Shadow game, handling display and visual effects.
"""

import os
import sys
import time
import random
from .constants import *


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


def display_tutorial_tip(tip):
    """Display a tutorial tip."""
    print(
        f"\n{CLR_TUTORIAL}┌─ TIP ───────────────────────────────────────┐{CLR_RESET}")
    print(f"{CLR_TUTORIAL}│ {tip}{' ' * (44 - len(tip))} │{CLR_RESET}")
    print(f"{CLR_TUTORIAL}└──────────────────────────────────────────────┘{CLR_RESET}")
