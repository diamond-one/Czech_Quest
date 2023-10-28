"""
This tool loops through vocab dict in 'content.py' 
and exports audio files of words to \audio folder
"""
import os
import sys
from gtts import gTTS

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Add the root directory of your project to sys.path
sys.path.append(os.path.join(current_directory, ".."))

from content.common_1000.common_1000_dic import common_1000

dictKey = 1

while True: 
    
    current_word = common_1000[dictKey][0]
    output_audio = gTTS(current_word, lang='cs', tld='cz')
    
    # Construct the relative path for saving the audio file
    audio_save_path = os.path.join(current_directory, "..", "content", "common_1000", f"{dictKey}_{current_word}.mp3")
    output_audio.save(audio_save_path)
    
    #DEBUG
    print(current_word)
    
    if dictKey >= 2:
        break
    dictKey += 1