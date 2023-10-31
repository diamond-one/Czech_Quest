
def restart_script():
    """
    Restarts the current script, clearing all existing data in memory.
    """
    print("Restarting the game...")
    os.execv(sys.executable, ['python'] + sys.argv)

def print_help():
    """
    Displays available commands and their descriptions to the user.
    """
    help_text = """
    Available Commands:
    :q!      - Quit the game immediately.
    :su      - Switch to a different user.
    :score   - Display the current scoreboard.
    :new     - Start a new game, as if you've just logged in.
    :help    - Display this help message showing available commands.
    :show    - Show the words currently in your learning pool.
    :hint    - Show a hint for the current word (if hints are enabled).
    :shint   - Show a hint on the first sighting of a word (if hints are enabled).
    """
    print(help_text)

def handle_commands(user_input, common_1000, progress, session_words, username):
    if user_input == ":q!":
        print("Quitting game...")
        exit()
    elif user_input == ":su":
        print("Switching user...")
        restart_script()
    elif user_input == ":score":
        print("Displaying scoreboard...")
        # Display the scoreboard
    elif user_input == ":new":
        restart_script()
    elif user_input == ":help":
        print_help()
    elif user_input == ":show":
        print("Words in pool:")
        # Show words in the pool
    elif user_input == ":hint":
        print("Showing hint...")
        # Add logic for showing hint
    elif user_input == ":shint":
        print("Showing hint on first sighting...")
        # Add logic for showing hint on first sighting
    else:
        return False  # Indicates that it was not a command
    return True  # Indicates that it was a command
