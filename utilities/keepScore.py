import json
import os

def update_score(scores, username, is_correct):
    if username not in scores:
        scores[username] = {"correct": 0, "wrong": 0}
    if is_correct:
        scores[username]["correct"] += 1
    else:
        scores[username]["wrong"] += 1


def save_scores_to_json(scores):
    # Print the current working directory for debugging  # DEBUG
    # print("Current working directory:", os.getcwd()) # DEBUG

    # Construct the file path relative to the current working directory
    file_path = os.path.join(os.getcwd(), "data", "scores.json")
    # print("Attempting to save to:", file_path)   # DEBUG

    try:
        with open(file_path, "w") as file:
            json.dump(scores, file)
            # print("Scores saved successfully.") # DEBUG

    except Exception as e:
        print(f"Error saving scores: {e}")


def load_scores_from_json():
    file_path = os.path.join("data", "scores.json")  # Correctly construct the file path
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
