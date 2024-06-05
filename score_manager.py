import csv

class ScoreManager:
    def __init__(self, high_score_file):
        """
        Initializes a new instance of the ScoreManager class with the specified high score file.

        Parameters:
            high_score_file (str): The file path of the high score file.

        Returns:
            None
        """
        self.high_score_file = high_score_file
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        """
        Load the high scores from the high scores csv file.

        This function reads the high score file and returns a dictionary containing the player names as keys and their corresponding scores as values. 
        If the file does not exist, an empty dictionary is returned.

        Returns:
            dict: A dictionary containing the player names as keys and their scores as values.
        """
        try:
            with open(self.high_score_file, mode='r') as file:
                reader = csv.reader(file)
                return {rows[0]: int(rows[1]) for rows in reader}
        except FileNotFoundError:
            return {}

    def save_high_scores(self):
        """
        Saves the high scores to a CSV file.

        This function opens the high score file specified during the initialization of the ScoreManager class in write mode and writes the high scores to it.
        The high scores are stored in a dictionary where the keys are the player names and the values are the corresponding scores.
        Each high score is written as a row in the CSV file, with the player name and score separated by a comma.

        Parameters:
            self (ScoreManager): The current instance of the ScoreManager class.

        Returns:
            None
        """
        with open(self.high_score_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for name, score in self.high_scores.items():
                writer.writerow([name, score])

    def update_high_scores(self, player_name, score):
        """
        Updates the high scores with the given player name and score.

        Args:
            player_name (str): The name of the player.
            score (int): The score of the player.

        This function checks if the player's name already exists in the high scores dictionary.
        If it does, it updates the score with the maximum value between the new score and the existing score.
        If the player's name does not exist, it adds the player's name and score to the high scores dictionary. 
        Finally, it saves the updated high scores to a CSV file.

        Returns:
            None
        """
        if player_name in self.high_scores:
            self.high_scores[player_name] = max(score, self.high_scores[player_name])
        else:
            self.high_scores[player_name] = score
        self.save_high_scores()

    def display_high_scores(self):
        """
        Displays the high scores in descending order.

        This function prints the high scores in descending order, with the player names and their corresponding scores. 
        It uses the `high_scores` dictionary to retrieve the scores and sorts them in descending order. 
        The scores are then printed in the format "{name}: {score}".

        Parameters:
            self (ScoreManager): The current instance of the ScoreManager class.

        Returns:
            None
        """
        print("High Scores:")
        sorted_scores = sorted(self.high_scores.items(), key=lambda item: item[1], reverse=True)
        for name, score in sorted_scores:
            print(f"{name}: {score}")
