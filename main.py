import random as random
from content.common_1000.common_1000_dic import common_1000
from utilities.keepScore import update_score, save_scores_to_json, load_scores_from_json

from gtts import gTTS
import tempfile
import os
import atexit
import glob

import pygame

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

linebreak = "____________________________________________________________________________________"

# Call the function at the start of your game
print_title_art()

# Game Intro
print("Czech Quest.. prepare yourself for 1000 word mastery. \n In this game you will be tested on the 1000 most used words in the Czech langauge \n")
print("This is not an excuse to ditch the grammer lessons, because you'll still need those to make sentences, however Czech Quest is another tool up your sleeve.")

def main(): 
    print("Starting main function...")  # Debug print
    scores = load_scores_from_json()
    pygame.mixer.init()
    username = input("Enter your username: ")  # Moved outside the loop
    while True:
        rnd_seed = random.randrange(1,20)
        czechWord = common_1000[rnd_seed][0]
        correct_answer = common_1000[rnd_seed][1]

        print("\nWhat is:", czechWord, "in English?")
        temp_file = play_text(czechWord)

        while True:
            choice = input("\nPress 'a + ENTER' to hear audio again, or just 'ENTER' to continue: ")
            if choice == 'a':
                temp_file = play_text(czechWord)
            elif choice == '':
                guess = input("Enter your guess: ").strip().lower()
                is_correct = guess == correct_answer.lower()
                update_score(scores, username, is_correct)
                print("Calling save_scores_to_json...") # Debug 
                save_scores_to_json(scores)

                if is_correct:
                    print("\nCorrect")
                else:
                    print("\nHmm, that's not right yet")
                break
            else:
                print("\nInvalid choice detected. Moving on to guessing phase.")
                guess = input("Enter your guess: ").strip().lower()
                is_correct = guess == correct_answer.lower()
                update_score(scores, username, is_correct)
                print("Calling save_scores_to_json...") # Debug
                save_scores_to_json(scores)

                if is_correct:
                    print("\nCorrect")
                else:
                    print("\nHmm, that's not right yet")
                break
        
        print("\nMeaning: ", correct_answer)
        print(common_1000[rnd_seed][2])
        print("\nVíc prosím? Press ENTER")
        input()
        print("__________________________Pojďme Gooo__________________________")

clear_temp_files()

if __name__ == "__main__":
    main()
