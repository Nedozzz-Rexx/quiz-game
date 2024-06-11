class Question:
    def __init__(self, question_type, difficulty, category, question, correct_answer, incorrect_answers, answers=None):
        """
        Initializes a new instance of the Question class with the specified attributes.

        Parameters:
            question_type (str): The type of the question.
            difficulty (str): The difficulty level of the question.
            category (str): The category of the question.
            question (str): The text of the question.
            correct_answer (str): The correct answer to the question.
            incorrect_answers (list): A list of incorrect answers.
            answers (list, optional): A list of all answers including correct and incorrect ones.
                If not provided, it defaults to [correct_answer] + incorrect_answers.

        Returns:
            None
        """
        self.type = question_type
        self.difficulty = difficulty
        self.category = category
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.answers = answers if answers is not None else [correct_answer] + incorrect_answers
        self.points = None  # Initialize points as None initially

    def calculate_points(self):
        """
        Calculate the points for the question based on its difficulty level.

        Returns:
            int: The number of points for the question.

        Raises:
            ValueError: If the difficulty level is invalid.
        """
        if self.difficulty == "easy":
            return 1
        elif self.difficulty == "medium":
            return 3
        elif self.difficulty == "hard":
            return 5
        else:
            raise ValueError("Invalid difficulty level.")


    def check_answer(self, user_answer):
        """
        Check if the user's answer matches the correct answer.

        Args:
            user_answer (str): The user's answer to the question.

        Returns:
            bool: True if the user's answer matches the correct answer, False otherwise.
        """
        return user_answer.lower() == self.correct_answer.lower()

    def update_points(self):
        """
        Update the points for the question based on its difficulty level.

        This method should be called after creating the Question object to initialize the points attribute.
        """
        self.points = self.calculate_points()