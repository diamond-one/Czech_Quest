import json
import os

def update_score(scores, username, is_correct, previous_streak):
    if username not in scores:
        scores[username] = {"correct": 0, "points": 0, "streak": 0, "longest_streak": 0}

    user_scores = scores[username]
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
        user_scores["points"] -= 10  # Deduct 10 points for wrong answer
        user_scores["streak"] = 0  # Reset streak on wrong answer

    # Update longest streak if previous streak was greater
    if previous_streak > user_scores["longest_streak"]:
        user_scores["longest_streak"] = previous_streak


def save_scores_to_json(scores):
    file_path = os.path.join(os.getcwd(), "data", "scores.json")
    try:
        with open(file_path, "w") as file:
            json.dump(scores, file)
    except Exception as e:
        print(f"Error saving scores: {e}")

def load_scores_from_json():
    file_path = os.path.join("data", "scores.json")
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def display_scoreboard(scores):
    if scores:
        print("\nLeaderboard:")
        # Sort users based on their total points in descending order
        sorted_users = sorted(scores.items(), key=lambda x: x[1]['points'], reverse=True)
        
        for username, user_scores in sorted_users:
            print("═════════════════════════════════════════")
            print(f"Player: {username}")
            print(f"Total Points: {user_scores['points']}")
            print(f"Longest Streak: {user_scores['longest_streak']}")
            print("═════════════════════════════════════════")
    else:
        print("No scores found. Let's start playing!\n")
