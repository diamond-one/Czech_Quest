import random
import pandas as pd
import json
import os
from utilities.keepScore import update_score, save_progress_to_json, load_progress_from_json, display_scoreboard
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
    if len(session_words) % 3 == 0:  # Every 5th word
        known_words = [word_id for word_id, level in progress.items() if level > 1 and word_id not in session_words]
        if known_words:
            return random.choice(known_words)

    # Interleaved Practice: Mix new words with words that need to be reviewed
    for word_id in word_ids:
        if word_id not in session_words:  # Ensure the word hasn't been used in the current session
            return word_id

    return random.choice(word_ids)  # Fallback in case all words have been used in the session

def select_new_word(common_1000, progress, session_words):
    word_ids = list(common_1000.keys())
    random.shuffle(word_ids)

    # Collect eligible new words
    eligible_new_words = [word_id for word_id in word_ids if word_id not in session_words]

    # If all words are above level 2, select based on Leitner system
    if not eligible_new_words:
        for word_id in word_ids:
            level = progress.get(word_id, 1)
            if random.random() < (1 / level) and word_id not in session_words:
                return word_id

    # Filter eligible new words based on the word limit
    eligible_new_words = eligible_new_words[:min(5, len(eligible_new_words))]

    return random.choice(eligible_new_words)


# Failsafe deletion of tempfiles created from play_text function
def clear_temp_files():
    pattern = os.path.join(tempfile.gettempdir(), "*.mp3")
    temp_files = glob.glob(pattern)
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except PermissionError:
            print(f"Permission denied for {temp_file}. File might be in use.")
        except Exception as e:
            print(f"Error deleting {temp_file}: {e}")

def play_text(czech_word, audio_text):
    # Play the Czech word audio
    tts_czech = gTTS(text=czech_word, lang='cs', tld='cz')
    fd_czech, temp_filename_czech = tempfile.mkstemp()
    os.close(fd_czech)

    try:
        tts_czech.save(temp_filename_czech)
        pygame.mixer.music.load(temp_filename_czech)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        pygame.mixer.music.stop()
        atexit.register(os.remove, temp_filename_czech)

    # Play the Audio Text
    tts_audio_text = gTTS(text=audio_text, lang='cs', tld='cz')
    fd_audio_text, temp_filename_audio_text = tempfile.mkstemp()
    os.close(fd_audio_text)

    try:
        tts_audio_text.save(temp_filename_audio_text)
        pygame.mixer.music.load(temp_filename_audio_text)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        pygame.mixer.music.stop()
        atexit.register(os.remove, temp_filename_audio_text)

    return temp_filename_audio_text  # Return the temp audio file for cleanup



def print_title_art():
    title = """
 ██████╗███████╗███████╗ ██████╗██╗  ██╗     ██████╗ ██╗   ██╗███████╗███████╗████████╗
██╔════╝╚══███╔╝██╔════╝██╔════╝██║  ██║    ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
██║       ███╔╝ █████╗  ██║     ███████║    ██║   ██║██║   ██║█████╗  ███████╗   ██║   
██║      ███╔╝  ██╔══╝  ██║     ██╔══██║    ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
╚██████╗███████╗███████╗╚██████╗██║  ██║    ů██████╔╝Ś██████╔╝███████╗███████║   ██║   
 ╚═════╝Ś══════╝Ś══════╝ ů═════╝Ś═╝  ů═╝     ů══▀▀═╝  ů═════╝ ů══════╝Ś══════╝   ů═╝   
    """
    print(title)

# Call the function at the start of your game
print_title_art()

# Game Intro
print("                Czech Quest.. prepare yourself for 1000 word mastery! \n")

def main():
    print("Starting main function...")  # Debug print
    common_1000 = load_data_from_excel('content/common_1000/common_1000.xlsx')
    pygame.mixer.init()

    username_input = input("\nEnter your username: ")
    username = username_input.lower().capitalize()  # Convert to lowercase for consistency

    # Load the progress for the user
    progress = load_progress_from_json(username)

    # Display the scoreboard for the user
    display_scoreboard()
    print("____________________________________________________")

    # Initialize session words
    session_words = set()

    while True:
        word_id = select_word(common_1000, progress, session_words)
        czech_word = common_1000[word_id]['Czech']
        czech_sentence = common_1000[word_id]['Czech Sentence']  # Load audio text from the correct column
        eng_sentence_translation = common_1000[word_id]['English Translation']
        correct_answer = common_1000[word_id]['English']
        # print(eng_sentence_translation) # DEBUG
        print("\nWhat is:", czech_word, "in English?")
        print("in a sentance: ", czech_sentence)  # Display audio text

        temp_file = play_text(czech_word, czech_sentence)  # Play audio for both Czech word and audio text

        guess = input("Enter your guess: ").strip().lower()
        is_correct = guess == correct_answer.lower() or guess == eng_sentence_translation.lower()


        # Get the previous streak before updating the score
        previous_streak = progress.get(username, {}).get("streak", 0)

        # Update the score with the current answer and previous streak
        update_score(progress, username, is_correct, previous_streak)

        save_progress_to_json(username, progress)

        if is_correct:
            print("\nCorrect, Correct, Correct, Correct, Correct")
            # Remove the word from session words if the answer is correct
            session_words.discard(word_id)
        else:
            print("\nIncorrect, Incorrect, Incorrect, Incorrect, Incorrect")

        # Update progress based on the user's answer
        update_progress(progress, word_id, is_correct)
        save_progress_to_json(username, progress)

        print("____________________________________________________")
        print("\nMeaning: ", correct_answer)
        print("\nMnemonic:", common_1000[word_id]['Mnemonic'])
        print("____________________________________________________")        
        print("\n", czech_sentence, ":", eng_sentence_translation)  # Display audio text
        print("____________________________________________________")   
        print("____________________________________________________")     
        input()


        # Check if the session word limit is reached
        if len(session_words) < 5:
            # Add a new word to session words
            new_word_id = select_new_word(common_1000, progress, session_words)
            session_words.add(new_word_id)

        clear_temp_files()

if __name__ == "__main__":
    main()
