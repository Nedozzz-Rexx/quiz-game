class QuizGame:
    def __init__(self, questions, score_manager):
        """
        Initializes a new instance of the QuizGame class with the specified questions and score manager.

        Parameters:
            questions (List[Question]): A list of Question objects representing the questions in the quiz.
            score_manager (ScoreManager): An instance of the ScoreManager class responsible for managing the scores.

        Returns:
            None
        """
        self.questions = questions
        self.score_manager = score_manager
        self.score = 0

    def play(self):
        """
        Play the quiz game.

        This method iterates over each question in the `questions` list and presents it to the user.
        For each question, the answers are displayed with corresponding numbers.
        The user is prompted to enter their answer, which is then checked against the correct answer.
        If the user's answer is correct, the score is incremented by the question's points and a "Correct!" message is printed.
        If the user's answer is incorrect, a "Incorrect. Game over." message is printed and the loop is broken.
        After the quiz is completed, the final score is saved using the `score_manager` and displayed to the user.

        Parameters:
            self (QuizGame): The current instance of the QuizGame class.

        Returns:
            None
        """
        for question in self.questions:
            print(question.text)
            for idx, answer in enumerate(question.answers):
                print(f"{idx + 1}. {answer}")
            user_answer = input("Your answer: ")

            # Check if the user entered a number or the answer itself
            if user_answer.isdigit():
                user_answer = question.answers[int(user_answer) - 1]

            if question.check_answer(user_answer):
                self.score += question.points
                print("Correct!")
            else:
                print("Incorrect. Game over.")
                break
        
        print(f"Your final score is {self.score}")
        name = input("Enter your name to save your score: ")
        self.score_manager.update_high_scores(name, self.score)
        print("Score saved!")
