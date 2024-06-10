import os
import time
from utils import getch, clear_screen
class QuizGame:
    def __init__(self, questions, score_manager):
        self.questions = questions
        self.score_manager = score_manager
        self.score = 0

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_countdown(self):
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)
        print("Let's go!")
        time.sleep(1)
        self.clear_screen()

    def announce_start(self):
        print("Get ready! The quiz is about to start!")
        self.print_countdown()

    def announce_easy_questions(self):
        print("We're starting with the easy questions. Think you can get them all right?")
        self.print_countdown()

    def announce_medium_questions(self):
        print("Were these too easy? Now the questions will have medium difficulty.")
        self.print_countdown()

    def announce_hard_questions(self):
        print("Now it's time for the hard questions. Good luck!")
        self.print_countdown()

    def play(self):
        """
        Play the quiz game.

        This method iterates over each question in the `questions` list and presents it to the user.
        For each question, the answers are displayed with corresponding numbers.
        The user is prompted to enter their answer, which is then checked against the correct answer.
        If the user's answer is correct, the score is incremented by the question's points and a "Correct!" message is printed.
        If the user's answer is incorrect, the correct answer is revealed and the loop is broken.
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

            clear_screen()
            print(question.question)

            if question.difficulty == "boolean":
                print("Choose either '1' for True or '2' for False.")
                valid_options = ["1", "2"]
            else:
                for idx, answer in enumerate(question.answers):
                    print(f"{idx + 1}. {answer}")
                valid_options = [str(i) for i in range(1, len(question.answers) + 1)]

            user_answer = input("Your answer: ").strip().lower()

            # Validate input and handle accordingly
            if question.difficulty == "boolean":
                while user_answer not in valid_options:
                    print("Invalid input. Please choose '1' for True or '2' for False.")
                    user_answer = input("Your answer: ").strip().lower()
                user_answer = "True" if user_answer == "1" else "False"
            else:
                while user_answer not in valid_options:
                    print("Invalid input. Please choose a valid option.")
                    user_answer = input("Your answer: ").strip().lower()
                user_answer = question.answers[int(user_answer) - 1]

            if question.check_answer(user_answer):
                points = question.calculate_points()  # Remove current_difficulty argument
                self.score += points
                print("Correct!")
                time.sleep(1)  # Pause to show "Correct!" message
                question_count += 1
            else:
                correct_answer = question.correct_answer
                if question.difficulty == "boolean":
                    correct_answer = "True" if correct_answer == "True" else "False"
                print(f"Incorrect. The correct answer is: {correct_answer}. Game over.")
                time.sleep(2)  # Pause to show the correct answer
                break

            print(f"Your current score is {self.score}")  # Print the current score after each question
            time.sleep(1)  # Pause to show the current score

        print(f"Your final score is {self.score}")
        name = input("Enter your name to save your score: ").strip()
        self.score_manager.update_high_scores(name, self.score)
        print("Score saved!")
        time.sleep(2)
        clear_screen()


