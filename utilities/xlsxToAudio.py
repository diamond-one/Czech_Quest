import os
import sys
import pandas as pd
from gtts import gTTS

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Add the root directory of your project to sys.path
sys.path.append(os.path.join(current_directory, ".."))

# Load data from Excel file
def load_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df

# Function to generate audio files
def generate_audio_files(df):
    for index, row in df.iterrows():
        current_word = row['Czech']
        output_audio = gTTS(current_word, lang='cs', tld='cz')
        
        # Construct the relative path for saving the audio file
        audio_save_path = os.path.join(current_directory, "..", "content", "common_1000", f"{index+1}_{current_word}.mp3")
        output_audio.save(audio_save_path)
        
        #DEBUG
        print(current_word)
        
        if index >= 10:  # Change this number to generate more or fewer files
            break

# Load the data
common_1000_df = load_data_from_excel(os.path.join(current_directory, "..", "content", "common_1000", "common_1000.xlsx"))

# Generate audio files
generate_audio_files(common_1000_df)
