import csv
from typing import Dict, List
from datetime import datetime

class ScoreManager:
    def __init__(self, high_score_file: str):
        """
        Initializes a new instance of the ScoreManager class with the specified high score file.

        Parameters:
            high_score_file (str): The file path of the high score file.
        """
        self.high_score_file = high_score_file
        self.high_scores = self.load_high_scores()

    def load_high_scores(self) -> List[Dict[str, str]]:
        """
        Load the high scores from the high scores CSV file.

        Returns:
            list: A list of dictionaries containing player names, scores, and dates.
        """
        high_scores = []
        try:
            with open(self.high_score_file, mode='r') as file:
                reader = csv.reader(file)
                for rows in reader:
                    if len(rows) == 3:
                        try:
                            high_scores.append({"name": rows[0], "score": int(rows[1]), "date": rows[2]})
                        except ValueError:
                            # Skip rows with invalid integer values
                            continue
        except FileNotFoundError:
            return high_scores
        return high_scores

    def save_high_scores(self) -> None:
        """
        Saves the high scores to a CSV file.
        """
        try:
            with open(self.high_score_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                for entry in self.high_scores:
                    writer.writerow([entry["name"], entry["score"], entry["date"]])
        except Exception as e:
            print(f"An error occurred while saving high scores: {e}")

    def update_high_scores(self, player_name: str, score: int) -> None:
        """
        Updates the high scores with the given player name and score.

        Parameters:
            player_name (str): The name of the player.
            score (int): The score of the player.
        """
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated = False
        for entry in self.high_scores:
            if entry["name"] == player_name:
                if score > entry["score"]:
                    entry["score"] = score
                    entry["date"] = date_str
                updated = True
                break
        if not updated:
            self.high_scores.append({"name": player_name, "score": score, "date": date_str})
        
        # Sort and keep all scores, but only the top 10 scores will be displayed
        self.high_scores = sorted(self.high_scores, key=lambda x: x["score"], reverse=True)
        self.save_high_scores()

    def display_high_scores(self) -> None:
        """
        Displays the top 10 high scores in descending order with ranks.
        """
        titles = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
        print("High Scores:""\n")
        for idx, entry in enumerate(self.high_scores[:10]):  # Display only the top 10 scores
            title = titles[idx] if idx < len(titles) else f"{idx+1}th"
            print(f"{title}: {entry['name']} - {entry['score']} (on {entry['date']})\n")
