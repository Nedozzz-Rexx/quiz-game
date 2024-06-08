import os
import time

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

    def clear_screen(self):
        """
        Clears the terminal screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_countdown(self):
        """
        Prints a countdown from 3 to 1.
        """
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)
        print("Let's go!")
        time.sleep(1)
        self.clear_screen()

    def announce_start(self):
        """
        Announce the start of the quiz with a countdown.
        """
        print("Get ready! The quiz is about to start!")
        self.print_countdown()

    def announce_easy_questions(self):
        """
        Announce the start of the easy questions.
        """
        print("We're starting with the easy questions. Think you can get them all right?")
        self.print_countdown()

    def announce_medium_questions(self):
        """
        Announce the start of the medium questions.
        """
        print("Were these too easy? Now the questions will have medium difficulty.")
        self.print_countdown()

    def announce_hard_questions(self):
        """
        Announce the start of the hard questions.
        """
        print("Now it's time for the hard questions. Good luck!")
        self.print_countdown()

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
        self.announce_start()

        # Announce the start of easy questions
        self.announce_easy_questions()
        current_difficulty = "easy"
        question_count = 0

        for question in self.questions:
            if question_count == 5:
                self.announce_medium_questions()
                current_difficulty = "medium"
            elif question_count == 10:
                self.announce_hard_questions()
                current_difficulty = "hard"

            print(question.text)
            for idx, answer in enumerate(question.answers):
                print(f"{idx + 1}. {answer}")
            user_answer = input("Your answer: ")

            # Check if the user entered a number or the answer itself
            if user_answer.isdigit():
                user_answer = question.answers[int(user_answer) - 1]

            if question.check_answer(user_answer):
                # Calculate the points based on the difficulty level of the question
                points = question.calculate_points(current_difficulty)
                self.score += points
                print("Correct!")
                question_count += 1
            else:
                print("Incorrect. Game over.")
                break

        print(f"Your final score is {self.score}")
        name = input("Enter your name to save your score: ")
        self.score_manager.update_high_scores(name, self.score)
        print("Score saved!")
        time.sleep(2)
        self.clear_screen()
