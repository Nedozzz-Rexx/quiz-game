class Question:
    def __init__(self, text, answers, correct_answer, difficulty):
        """
        Initializes a new instance of the Question class with the specified text, answers, correct answer, and difficulty.

        Parameters:
            text (str): The text of the question.
            answers (list): A list of possible answers to the question.
            correct_answer (str): The correct answer to the question.
            difficulty (str): The difficulty level of the question.

        Returns:
            None
        """
        self.text = text
        self.answers = answers
        self.correct_answer = correct_answer
        self.difficulty = difficulty
        self.points = self.calculate_points(difficulty)

    def calculate_points(self, difficulty):
        """
        Calculate the points for a given difficulty level.

        Args:
            self (Question): The Question object.
            difficulty (str): The difficulty level of the question.

        Returns:
            int: The number of points for the given difficulty level.

        Raises:
            None

        Examples:
            >>> question = Question("What is the capital of France?", ["Paris", "London", "Berlin"], "Paris", "easy")
            >>> question.calculate_points("easy")
            1
            >>> question.calculate_points("medium")
            3
            >>> question.calculate_points("hard")
            5
        """
        if difficulty == "easy":
            return 1
        elif difficulty == "medium":
            return 3
        elif difficulty == "hard":
            return 5

    def check_answer(self, user_answer):
        """
        Check if the user's answer matches the correct answer, ignoring case.

        Args:
            user_answer (str): The user's answer to the question.

        Returns:
            bool: True if the user's answer matches the correct answer, ignoring case. False otherwise.
        """
        return user_answer.lower() == self.correct_answer.lower()
