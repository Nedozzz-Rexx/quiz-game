import csv
from typing import Dict

class ScoreManager:
    def __init__(self, high_score_file: str):
        """
        Initializes a new instance of the ScoreManager class with the specified high score file.

        Parameters:
            high_score_file (str): The file path of the high score file.
        """
        self.high_score_file = high_score_file
        self.high_scores = self.load_high_scores()

    def load_high_scores(self) -> Dict[str, int]:
        """
        Load the high scores from the high scores CSV file.

        Returns:
            dict: A dictionary containing the player names as keys and their scores as values.
        """
        try:
            with open(self.high_score_file, mode='r') as file:
                reader = csv.reader(file)
                return {rows[0]: int(rows[1]) for rows in reader}
        except FileNotFoundError:
            return {}

    def save_high_scores(self) -> None:
        """
        Saves the high scores to a CSV file.
        """
        try:
            with open(self.high_score_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                for name, score in self.high_scores.items():
                    writer.writerow([name, score])
        except Exception as e:
            print(f"An error occurred while saving high scores: {e}")

    def update_high_scores(self, player_name: str, score: int) -> None:
        """
        Updates the high scores with the given player name and score.

        Parameters:
            player_name (str): The name of the player.
            score (int): The score of the player.
        """
        if player_name in self.high_scores:
            self.high_scores[player_name] = max(score, self.high_scores[player_name])
        else:
            self.high_scores[player_name] = score
        self.save_high_scores()

    def display_high_scores(self) -> None:
        """
        Displays the high scores in descending order.
        """
        sorted_scores = sorted(self.high_scores.items(), key=lambda item: item[1], reverse=True)
        for name, score in sorted_scores:
            print(f"{name}: {score}")
