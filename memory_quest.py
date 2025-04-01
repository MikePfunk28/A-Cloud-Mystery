import time
import random
import os
import sys
from datetime import datetime

# ASCII Art
LIBRARY_ART = r"""
    _______
   /      /|
  /______/ |
  |      | |
  |  ?   | /
  |______|/
"""

MONSTER_ART = r"""
     .-.
    (o.o)
     |=|
    __|__
   //.=|=\\
  // .=|=\\
  \\ .=|=\\//
   \\(_=_)//
    (:| |:)
     || ||
     () ()
     || ||
     || ||
    ==' '==
"""

GEM_ART = r"""
   /\
  /  \
 /    \
/      \
\      /
 \    /
  \  /
   \/
"""

BOOKSHELF_ART = r"""
  _________________________
 |[]                     []|
 |[]                     []|
 |[]                     []|
 |[]                     []|
 |[]_____________________[]|
"""

# Sound effects (for Windows)


def play_sound(effect):
    if sys.platform == 'win32':
        import winsound
        if effect == "correct":
            winsound.Beep(1000, 300)
        elif effect == "wrong":
            winsound.Beep(200, 500)
        elif effect == "win":
            for i in range(500, 1500, 100):
                winsound.Beep(i, 100)

# Leaderboard system


def save_score(name, score, topic):
    with open("leaderboard.txt", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d')},{name},{score},{topic}\n")


def show_leaderboard():
    try:
        with open("leaderboard.txt", "r") as f:
            scores = [line.strip().split(',') for line in f.readlines()]
            if not scores:
                print("No scores yet!")
                return

            print("\n=== TOP SCORES ===")
            # Sort by score (descending)
            scores.sort(key=lambda x: int(x[2]), reverse=True)
            for i, (date, name, score, topic) in enumerate(scores[:5], 1):
                print(f"{i}. {name}: {score} ({topic}, {date})")
    except FileNotFoundError:
        print("No scores yet!")


# Expanded question database
questions = {
    "history": [
        {"question": "Who was the first U.S. president?", "answer": "george washington",
         "hint": "Father of his country", "difficulty": "easy"},
        {"question": "Year the Titanic sank:", "answer": "1912",
            "hint": "Early 20th century", "difficulty": "easy"},
        {"question": "Ancient civilization that built the pyramids:", "answer": "egyptians",
         "hint": "Nile River civilization", "difficulty": "medium"},
        {"question": "Decode this cipher to reveal the philosopher's name: XIBBZ QLXV",
         "answer": "plato", "hint": "Caesar cipher shift +1", "difficulty": "hard"}
    ],
    "science": [
        {"question": "Chemical symbol for gold:", "answer": "au",
            "hint": "From Latin 'aurum'", "difficulty": "easy"},
        {"question": "Planet closest to the Sun:", "answer": "mercury",
            "hint": "Also a Roman god", "difficulty": "easy"},
        {"question": "What does DNA stand for?", "answer": "deoxyribonucleic acid",
         "hint": "Starts with 'deoxy'", "difficulty": "medium"},
        {"question": "This scientist developed the theory of relativity: [E=mc²]",
         "answer": "albert einstein", "hint": "Famous for his hair", "difficulty": "hard"}
    ],
    "pop_culture": [
        {"question": "Who sang 'Bohemian Rhapsody'?", "answer": "queen",
            "hint": "British rock band", "difficulty": "easy"},
        {"question": "First movie to win Best Picture Oscar:", "answer": "wings",
         "hint": "1927 silent film", "difficulty": "medium"},
        {"question": "This actor played both Neo and John Wick:", "answer": "keanu reeves",
         "hint": "Known for being wholesome", "difficulty": "medium"},
        {"question": "Decode this movie title: 8-15-13-5-1-12-15-15-13",
         "answer": "the lion king", "hint": "A=1, B=2,...", "difficulty": "hard"}
    ]
}

# Story elements for each room
room_stories = {
    1: "You enter the Hall of Beginnings. Dusty tomes line the walls...",
    2: "The Chamber of Riddles awaits. The air hums with forgotten knowledge...",
    3: "Before you stands the Vault of Final Reckoning. A massive door creaks open...",
    4: "The Forbidden Archive. Books float in midair here...",
    5: "The Observatory of Lost Time. Star charts glow on the ceiling..."
}

# Game setup


def display_intro():
    print(LIBRARY_ART)
    print("""
    MEMORY QUEST: THE LIBRARY OF MNEMOSYNE
    --------------------------------------
    An ancient library crumbles as knowledge fades from the world.
    Only you can restore it by answering questions correctly!
    
    Each correct answer repairs part of the library.
    Wrong answers summon Forgetting Monsters!
    
    Power-ups:
    - Hint Tokens: Reveal clues (limited uses)
    - Time Warp: Get extra time on timed questions
    """)


def main():
    display_intro()

    # Player setup
    player_name = input("Enter your scholar's name: ")
    topic = input("Choose your topic (history/science/pop_culture): ").lower()
    while topic not in questions:
        topic = input(
            "Invalid topic. Choose history/science/pop_culture: ").lower()

    difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
    while difficulty not in ["easy", "medium", "hard"]:
        difficulty = input(
            "Invalid difficulty. Choose easy/medium/hard: ").lower()

    score = 0
    lives = 3
    hint_tokens = 2
    time_warps = 1
    rooms_completed = 0

    print(f"\nWelcome, {player_name}, to the {topic.capitalize()} wing!")
    time.sleep(1)

    # Filter questions by difficulty
    topic_questions = [q for q in questions[topic]
                       if q.get("difficulty", "easy") == difficulty]
    random.shuffle(topic_questions)

    for room in range(1, 6):
        if room > len(topic_questions):
            break

        print("\n" + "="*50)
        print(room_stories.get(room, "A mysterious new chamber appears..."))
        print(BOOKSHELF_ART)

        current_q = topic_questions[room-1]
        time_limit = 15 if difficulty == "easy" else 10 if difficulty == "medium" else 7

        # Timed question
        start_time = time.time()
        print(f"\n⌛ You have {time_limit} seconds!")
        print(f"\nQuestion {room}: {current_q['question']}")

        # Time warp power-up check
        if time_warps > 0:
            use_warp = input(
                f"Use Time Warp? (+5 sec) You have {time_warps} left. (Y/N): ").lower()
            if use_warp == 'y':
                time_limit += 5
                time_warps -= 1
                print(f"⏳ Time extended! You now have {time_limit} seconds.")

        answer = None
        while True:
            if time.time() - start_time > time_limit:
                print("\n⏰ Time's up!")
                answer = ""
                break

            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                answer = input().lower()
                break
            time.sleep(0.1)

        # Check answer
        if answer == current_q["answer"]:
            play_sound("correct")
            print(GEM_ART)
            print("\n✅ Correct! A gem glows in your hand.")
            score += 100 * room  # More points for harder rooms
            rooms_completed += 1
        else:
            play_sound("wrong")
            print(MONSTER_ART)
            print("\n❌ Wrong! A Forgetting Monster appears!")

            if hint_tokens > 0:
                use_hint = input(
                    f"Use a hint? You have {hint_tokens} left. (Y/N): ").lower()
                if use_hint == 'y':
                    hint_tokens -= 1
                    print(f"\n💡 HINT: {current_q['hint']}")
                    answer = input("Try again: ").lower()
                    if answer == current_q["answer"]:
                        play_sound("correct")
                        print("\n✅ Correct (with hint)!")
                        score += 50 * room
                        rooms_completed += 1
                        continue

            lives -= 1
            if lives <= 0:
                print("\n💀 The monster consumes your knowledge... Game Over!")
                break

            # Bonus question to defeat monster
            print("\nAnswer this to defeat the monster:")
            bonus_q = random.choice(
                [q for q in topic_questions if q != current_q])
            bonus_answer = input(f"{bonus_q['question']}: ").lower()
            if bonus_answer == bonus_q["answer"]:
                play_sound("correct")
                print("\n✨ Monster defeated! You regain your footing.")
            else:
                play_sound("wrong")
                print("\nThe monster laughs as it fades away...")

        print(
            f"\nScore: {score} | Lives: {lives} | Rooms: {rooms_completed}/5")
        time.sleep(2)

    # Game end
    if lives > 0 and rooms_completed >= 3:
        play_sound("win")
        print("\n" + "="*50)
        print(LIBRARY_ART)
        print(f"""
        🎉 CONGRATULATIONS {player_name.upper()}!
        You've restored {rooms_completed} rooms of the Library!
        Final Score: {score}
        """)
        save_score(player_name, score, topic)
    else:
        print("\nThe library remains in darkness... Try again!")

    show_leaderboard()
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
