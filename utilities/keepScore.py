import json
import os

def update_score(progress, username, is_correct, previous_streak):
    if 'scores' not in progress:
        progress['scores'] = {"correct": 0, "points": 0, "streak": 0, "longest_streak": 0}

    user_scores = progress['scores']
    if 'points' not in user_scores:
        user_scores['points'] = 0
    if 'streak' not in user_scores:
        user_scores['streak'] = 0
    if 'longest_streak' not in user_scores:
        user_scores['longest_streak'] = 0

    if is_correct:
        user_scores["correct"] += 1
        user_scores["points"] += 10  # 10 points for correct answer
        user_scores["streak"] += 1
        # Check for streak bonus
        if user_scores["streak"] >= 5:
            user_scores["points"] += 10  # Additional 10 points for streak
        # Update longest streak if current streak is greater
        if user_scores["streak"] > user_scores["longest_streak"]:
            user_scores["longest_streak"] = user_scores["streak"]
    else:
        user_scores["points"] -= 5  # Deduct 5 points for wrong answer
        user_scores["streak"] = 0  # Reset streak on wrong answer

    # Update longest streak if previous streak was greater
    if previous_streak > user_scores["longest_streak"]:
        user_scores["longest_streak"] = previous_streak

def save_progress_to_json(username, progress):
    file_path = os.path.join(os.getcwd(), "data", f"progress_{username}.json")
    try:
        with open(file_path, "w") as file:
            json.dump(progress, file)
    except Exception as e:
        print(f"Error saving progress: {e}")

def load_progress_from_json(username):
    file_path = os.path.join("data", f"progress_{username}.json")
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

import os
import json

def display_scoreboard():
    scores_directory = os.path.join(os.getcwd(), "data")
    all_scores = []

    # Iterate through all progress files and collect scores
    for filename in os.listdir(scores_directory):
        if filename.startswith("progress_") and filename.endswith(".json"):
            file_path = os.path.join(scores_directory, filename)
            try:
                with open(file_path, "r") as file:
                    user_progress = json.load(file)
                    if 'scores' in user_progress:
                        username = filename.replace("progress_", "").replace(".json", "")
                        user_scores = user_progress['scores']
                        all_scores.append((username, user_scores['points'], user_scores['longest_streak']))
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # Sort the scores in descending order based on points
    all_scores.sort(key=lambda x: x[1], reverse=True)

    # Display the top three scores
    print("\n LEADERBOARD")
    print("\nTop 3 Players:")
    for i, (username, points, longest_streak) in enumerate(all_scores[:3], start=1):
        print(f"{i}. {username} - Points: {points}, Longest Streak: {longest_streak}")

    if not all_scores:
        print("No scores found. Let's start playing!\n")

