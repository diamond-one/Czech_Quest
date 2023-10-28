import random as random
from content.common_1000.common_1000_dic import common_1000
from gtts import gTTS
import tempfile
import os
import atexit
import glob

import pygame
import keyboard
import time

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

def main(): 
    pygame.mixer.init()
    while True:
        rnd_seed = random.randrange(1,1001)
        czechWord = common_1000[rnd_seed][0]
        print("What is:", czechWord, "in English?")
        temp_file = play_text(czechWord)

        while True:
            print("Press 'a' to hear audio again, press 'g' to guess: ", end='', flush=True)
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'a':
                    temp_file = play_text(czechWord)
                elif event.name == 'g':
                    guess = input("\nEnter your guess: ")
                    print(f"You guessed: {guess}")
                    break
                else:
                    print("\nInvalid choice. Please press 'a' or 'g'.")

        print("____________________________________________________________________________________")
        meaning = common_1000[rnd_seed][1]
        print ("Meaning: ", meaning)
        print("____________________________________________________________________________________")
        print (common_1000[rnd_seed][2])
        print ("Víc prosím?")
        input()
        print("__________________________Pojďme Gooo__________________________")

clear_temp_files()
if __name__ == "__main__":
    main()
