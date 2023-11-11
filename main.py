import random
import pandas as pd
import json
import os
from gtts import gTTS
import tempfile
import atexit
import glob
import pygame
pygame.init()

from utilities.keepScore import update_score, save_progress_to_json, load_progress_from_json, display_scoreboard
from utilities.command_handler import handle_commands, get_audio_status, print_help
from utilities.title import print_title_art

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

# Global variable to keep track of words answered correctly
correctly_answered_words = set()

def win_or_lose_audio(win):
    if win:
        sound_file = "content/win_audio.wav"
    else:
        sound_file = "content/lost_audio.wav"

    sound = pygame.mixer.Sound(sound_file)
    sound.play()

# Load data from Excel file
def load_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df.to_dict(orient='index')

# Load progress from JSON
def load_progress_from_json(username):
    try:
        with open(f"data/progress_{username}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save progress to JSON
def save_progress_to_json(username, progress):
    with open(f"data/progress_{username}.json", "w") as file:
        json.dump(progress, file)

def update_progress(progress, word_id, is_correct):
    if word_id not in progress:
        progress[word_id] = 1  # Starting level in Leitner system
    else:
        if is_correct:
            progress[word_id] += 1  # Move up a level
            correctly_answered_words.add(word_id)  # Add to correctly answered words
        else:
            progress[word_id] = max(1, progress[word_id] - 1)  # Move down a level, but not below 1

def select_word(common_1000, progress, session_words):
    word_ids = list(common_1000.keys())
    random.shuffle(word_ids)

    # Focused Repetition & Adaptive Spacing: Prioritize words that have been answered incorrectly or are new
    for word_id in word_ids:
        if word_id not in session_words:  # Ensure the word hasn't been used in the current session
            level = progress.get(word_id, 1)
            if level == 1 or level == 2:  # Higher priority for new or frequently wrong words
                return word_id

    # # Confidence Boost Words: Include words that the user knows well
    # if len(session_words) % 3 == 0:  # Every 5th word
    #     known_words = [word_id for word_id, level in progress.items() if level > 1 and word_id not in session_words]
    #     if known_words:
    #         return random.choice(known_words)

    # # Interleaved Practice: Mix new words with words that need to be reviewed
    # for word_id in word_ids:
    #     if word_id not in session_words:  # Ensure the word hasn't been used in the current session
    #         return word_id

    return random.choice(word_ids)  # Fallback in case all words have been used in the session

def select_new_word(common_1000, progress, session_words):
    word_ids = list(common_1000.keys())
    random.shuffle(word_ids)

    # Collect eligible new words
    eligible_new_words = [word_id for word_id in word_ids if word_id not in session_words]

    # If there are no eligible new words, select any word not in session
    if not eligible_new_words:
        eligible_new_words = [word_id for word_id in word_ids if word_id not in session_words]

    return random.choice(eligible_new_words)

def clear_temp_files():
    pattern = os.path.join(tempfile.gettempdir(), "*.mp3")
    temp_files = glob.glob(pattern)
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except PermissionError:
            print(f"Permission denied for {temp_file}. File might be in use.")
            pygame.time.delay(100)  # Wait a bit before trying again
        except Exception as e:
            print(f"Error deleting {temp_file}: {e}")

def play_text(czech_word, audio_text):
    def play_audio(audio_text):
        tts = gTTS(text=audio_text, lang='cs', tld='cz')
        fd, temp_filename = tempfile.mkstemp()
        os.close(fd)

        try:
            tts.save(temp_filename)
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        finally:
            pygame.mixer.music.stop()
            atexit.register(os.remove, temp_filename)

    play_audio(czech_word)
    play_audio(audio_text)

def main():
    print_title_art()
    print_help()
    print("Czech Quest.. prepare yourself for 1000 word mastery!\n")

    # Initialize pygame and load data
    pygame.mixer.init()
    common_1000 = load_data_from_excel('content/common_1000/common_1000.xlsx')

    username_input = input("\nEnter your username: ")
    username = username_input.lower().capitalize()  # Convert to lowercase for consistency

    # Load the progress for the user
    progress = load_progress_from_json(username)

    # Display the scoreboard for the user
    display_scoreboard()
    print("____________________________________________________")

    # Initialize session words
    session_words = set()

    # Define maximum session size
    max_session_size = 5

    # Select initial session words
    while len(session_words) < max_session_size:
        new_word_id = select_new_word(common_1000, progress, session_words)
        session_words.add(new_word_id)

    word_id = None  # Initialize word_id outside the loop

    while True:
        if word_id is None:
            word_id = select_word(common_1000, progress, session_words)
            session_words.add(word_id)  # Add the selected word to the session_words set
            czech_word = common_1000[word_id]['Czech']
            czech_sentence = common_1000[word_id]['Czech Sentence']
            eng_sentence_translation = common_1000[word_id]['English Translation']
            eng_sentence_lower = eng_sentence_translation.strip().lower()
            correct_answer = common_1000[word_id]['English']
            print("\nWhat is:", czech_word, "in English?")
            print("Used in a sentence: ", czech_sentence)

            if get_audio_status() == True:
                temp_file = play_text(czech_word, czech_sentence)

        guess = input("\nEnter your guess or a command: ").strip().lower()
        command_executed = handle_commands(guess, common_1000, progress, session_words, username)

        if command_executed:
            continue  # If a command was executed, repeat the loop without changing the word

        is_correct = guess == correct_answer.lower() or guess == eng_sentence_lower

        if is_correct:
            win = True
            win_or_lose_audio(win)
            print("____________________________________________________")
            print(f"\n{Colors.GREEN}                      CORRECT           {Colors.RESET}")
            print("____________________________________________________")

            # Print the mnemonic before resetting the word_id
            print("\nMnemonic:", common_1000[word_id]['Mnemonic'])
            # Update progress before resetting word_id
            update_progress(progress, word_id, is_correct)
            save_progress_to_json(username, progress)
            # Then discard the word_id and reset
            session_words.discard(word_id)
            word_id = None  # Reset word_id to select a new word in the next iteration
            # word_id = select_word(common_1000, progress, session_words)
            # session_words.add(word_id)  # Add the selected word to the session_words set

        else:
            win = False
            win_or_lose_audio(win)
            print("____________________________________________________")
            print(f"\n{Colors.RED}                        INCORRECT           {Colors.RESET}")

            print("____________________________________________________")
            # Print Mnemonic even if incorrect
            print("\nMnemonic:", common_1000[word_id]['Mnemonic'])
            # Update progress for incorrect guess before resetting word_id
            update_progress(progress, word_id, is_correct)
            save_progress_to_json(username, progress)
            print("\nMeaning: ", correct_answer)
            word_id = None  # Reset word_id to select a new word in the next iteration


        print("\n", czech_sentence, ":", eng_sentence_translation)  # Display audio text
        print(f"\n{Colors.BLUE} o_________________________o___________________________o{Colors.RESET}")

        # Ask the user if they want to continue or enter a command
        user_input = input("Soak that in for a moment. Want more or enter a command: ").strip().lower()

        # Check if the input is a command
        if user_input.startswith(':'):  # Assuming commands start with ':'
            command_executed = handle_commands(user_input, common_1000, progress, session_words, username)
            if command_executed:
                continue  # If a command was executed, repeat the loop without changing the word

        clear_temp_files()

if __name__ == "__main__":
    main()
