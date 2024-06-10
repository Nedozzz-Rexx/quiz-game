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
        If the user's answer is incorrect, a "Incorrect. Game over." message is printed and the loop is broken.
        After the quiz is completed, the final score is saved using the `score_manager` and displayed to the user.

        Parameters:
            self (QuizGame): The current instance of the QuizGame class.

        Returns:
            None
        """
        #self.clear_screen()  # Clear the screen before starting the quiz game
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

            self.clear_screen()  # Clear the screen before displaying the question
            print(question.question)  # Change here from question.text to question.question

            if question.difficulty == "boolean":
                print("Choose either '1' for True or '2' for False.")
                valid_options = ["1", "2"]
            else:
                for idx, answer in enumerate(question.answers):
                    print(f"{idx + 1}. {answer}")
                valid_options = [str(i) for i in range(1, len(question.answers) + 1)]

            user_answer = input("Your answer: ").strip().lower()

            # Validate input and handle accordingly
            if user_answer not in valid_options:
                print("Invalid input. Please choose a valid option.")
                print(valid_options)

            while user_answer not in valid_options:
                user_answer = input("Your answer: ").strip().lower()

            # Translate boolean answers from numbers to words
            if question.difficulty == "boolean":
                user_answer = "True" if user_answer == "1" else "False"

            # Convert the answer back to the full text if necessary
            if user_answer.isdigit():
                user_answer = question.answers[int(user_answer) - 1]

            self.clear_screen()  # Clear the screen after displaying the question

            if question.check_answer(user_answer):
                points = question.calculate_points()  # Remove current_difficulty argument
                self.score += points
                print("Correct! Next question!")
                question_count += 1
                print(f"Your current score is {self.score}")  # Print the current score after each question
                time.sleep(1.5)  # Pause for 1 second
            else:
                print("Incorrect. Game over.")
                break

        print(f"Your final score is {self.score}")
        name = input("Enter your name to save your score: ").strip()
        self.score_manager.update_high_scores(name, self.score)
        print("Score saved!")
        time.sleep(2)
        self.clear_screen()  # Clear the screen after the quiz game ends


