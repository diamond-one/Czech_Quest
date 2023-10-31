# command_handler.py
from utilities.keepScore import display_scoreboard
import os
import sys
import subprocess

audio_enable = True

def restart_script():
    print("\nRestarting the game...")
    subprocess.call([sys.executable] + sys.argv)
    sys.exit()

def print_help():
    """
    Displays available commands and their descriptions to the user.
    """
    help_text = """
    Available Commands:
    :q!      - Quit the game immediately.
    :su      - Switch to a different user.
    :lb      - Display the current Leaderboard.
    :new     - Start a new game, as if you've just logged in.
    :help    - Display this help message showing available commands.
    :so      - Sound OFF/ON - Recomended when not using sound, so things are fast.
    :show    - Show the words currently in your learning pool.
    :hint    - ~~Show a hint for the current word (if hints are enabled).~~
    :shint   - ~~Show a hint on the first sighting of a word (if hints are enabled).~~
    """
    print(help_text)

def get_audio_status():
    return audio_enable

def toggle_audio():
    global audio_enable
    audio_enable = not audio_enable
    print("Audio is now", "on." if audio_enable else "off.")
    return audio_enable

def print_words_in_pool(common_1000, session_words):
    print("\nWords in current pool:")
    for word_id in session_words:
        word_data = common_1000[word_id]
        print(f"- {word_data['Czech']} (English: {word_data['English']})")

def handle_commands(user_input, common_1000, progress, session_words, username):
   
    if user_input == ":q!":
        print("\nQuitting game...")
        exit()

    elif user_input == ":su":
        print("\nSwitching user...")
        restart_script()

    elif user_input == ":lb":
        display_scoreboard()

    elif user_input == ":new":
        restart_script()

    elif user_input == ":help":
        print_help()

    elif user_input == ":so":
        toggle_audio()
        
    elif user_input == ":show":
        print_words_in_pool(common_1000, session_words)

    elif user_input == ":hint":
        print("\nShowing hint...")
        # Add logic for showing hint
        # needs hints added to xlsx

    elif user_input == ":shint":
        print("\nShowing hint on first sighting...")
        # Add logic for showing hint on first sighting
        # needs hints added to xlsx
