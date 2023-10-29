import random
import pandas as pd
import json
import os
from utilities.keepScore import update_score, save_scores_to_json, load_scores_from_json, display_scoreboard
from gtts import gTTS
import tempfile
import atexit
import glob
import pygame

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

# Global variable to keep track of words answered correctly
correctly_answered_words = set()

def update_progress(progress, word_id, is_correct):
    if word_id not in progress:
        progress[word_id] = 1  # Starting level in Leitner system
    else:
        if is_correct:
            progress[word_id] += 1  # Move up a level
            correctly_answered_words.add(word_id)  # Add to correctly answered words
        else:
            progress[word_id] = max(1, progress[word_id] - 1)  # Move down a level, but not below 1

# Select a word based on Leitner system
def select_word(common_1000, progress, session_words):
    word_ids = list(common_1000.keys())
    random.shuffle(word_ids)

    # Focused Repetition & Adaptive Spacing: Prioritize words that have been answered incorrectly or are new
    for word_id in word_ids:
        if word_id not in session_words:  # Ensure the word hasn't been used in the current session
            level = progress.get(word_id, 1)
            if level == 1 or level == 2:  # Higher priority for new or frequently wrong words
                return word_id

    # Confidence Boost Words: Include words that the user knows well
    if len(session_words) % 5 == 0:  # Every 5th word
        known_words = [word_id for word_id, level in progress.items() if level > 3 and word_id not in session_words]
        if known_words:
            return random.choice(known_words)

    # Interleaved Practice: Mix new words with words that need to be reviewed
    for word_id in word_ids:
        if word_id not in session_words:  # Ensure the word hasn't been used in the current session
            return word_id

    return random.choice(word_ids)  # Fallback in case all words have been used in the session


# Failsafe deletion of tempfiles created from play_text function
def clear_temp_files():
    pattern = os.path.join(tempfile.gettempdir(), "*.mp3")
    temp_files = glob.glob(pattern)
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except Exception as e:
            print(f"Error deleting {temp_file}: {e}")

def play_text(text):
    tts = gTTS(text=text, lang='cs', tld='cz')
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
    return temp_filename

def print_title_art():
    title = """
 ██████╗███████╗███████╗ ██████╗██╗  ██╗     ██████╗ ██╗   ██╗███████╗███████╗████████╗
██╔════╝╚══███╔╝██╔════╝██╔════╝██║  ██║    ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
██║       ███╔╝ █████╗  ██║     ███████║    ██║   ██║██║   ██║█████╗  ███████╗   ██║   
██║      ███╔╝  ██╔══╝  ██║     ██╔══██║    ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
╚██████╗███████╗███████╗╚██████╗██║  ██║    ╚██████╔╝╚██████╔╝███████╗███████║   ██║   
 ╚═════╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝     ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
    """
    print(title)

# Call the function at the start of your game
print_title_art()

# Game Intro
print("Czech Quest.. prepare yourself for 1000 word mastery! \n")

def main():
    print("Starting main function...")
    scores = load_scores_from_json()
    common_1000 = load_data_from_excel('content/common_1000/common_1000.xlsx')
    pygame.mixer.init()

    username_input = input("Enter your username: ")
    username = username_input.lower()

    display_scoreboard(scores)
    progress = load_progress_from_json(username)

    session_words = set()  # Keep track of words used in the current session

    while True:
        if len(session_words) < 5:
            word_id = select_word(common_1000, progress, session_words)
            session_words.add(word_id)  # Add the selected word to the session set
        else:
            word_id = random.choice(list(session_words))

        czechWord = common_1000[word_id]['Czech']
        correct_answer = common_1000[word_id]['English']

        print("\nWhat is:", czechWord, "in English?")
        temp_file = play_text(czechWord)

        guess = input("\nEnter your guess: ").strip().lower()
        is_correct = guess == correct_answer.lower()

        # Get the previous streak before updating the score
        previous_streak = scores.get(username, {}).get("streak", 0)

        # Update the score with the current answer and previous streak
        update_score(scores, username, is_correct, previous_streak)

        save_scores_to_json(scores)

        if is_correct:
            print("\nCorrect")
            session_words.remove(word_id)  # Remove the word from the session set
        else:
            print("\nHmm, that's not right yet")

        # Update progress based on user's answer
        update_progress(progress, word_id, is_correct)
        save_progress_to_json(username, progress)

        print("\nMeaning: ", correct_answer)
        print(common_1000[word_id]['Mnemonic'])
        print("__________________________Pojďme Gooo__________________________")

clear_temp_files()

if __name__ == "__main__":
    main()