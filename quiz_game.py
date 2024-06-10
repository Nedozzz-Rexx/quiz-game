import os
import time
from utils import getch, clear_screen
import sys  # to use animation effect
import random  # to use shuffle function

class QuizGame:

    def print_with_animation(self, text):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)  # Adjust the speed of animation here

    def __init__(self, questions, score_manager):
        self.questions = questions
        self.score_manager = score_manager
        self.score = 0

    def print_countdown(self):
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)
        print("Let's go!")
        time.sleep(1)
        clear_screen()

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

    def randomize_answers(self, question):
        all_answers = question.incorrect_answers[:]
        all_answers.append(question.correct_answer)
        random.shuffle(all_answers)
        return all_answers

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

        for idx, question in enumerate(self.questions, start=1):
            if question_count == 5:
                self.announce_medium_questions()
                current_difficulty = "medium"
            elif question_count == 10:
                self.announce_hard_questions()
                current_difficulty = "hard"

            clear_screen()
    
            self.print_with_animation(f"Question {idx}: ")
            self.print_with_animation(question.question + "\n")

            randomized_answers = self.randomize_answers(question)

            for index, answer in enumerate(randomized_answers):
                print(f"{index + 1}. {answer}")
            
            valid_options = [str(i) for i in range(1, len(randomized_answers) + 1)]

            user_answer = input("Your answer: ").strip().lower()

            # Validate input and handle accordingly
            while user_answer not in valid_options:
                print("Invalid input. Please choose a valid option.")
                user_answer = input("Your answer: ").strip().lower()

            user_answer = randomized_answers[int(user_answer) - 1]

            if question.check_answer(user_answer):
                points = question.calculate_points()
                self.score += points
                print("Correct! Next question!")
                question_count += 1
                print(f"Your current score is {self.score}")
                time.sleep(1.5)  # Pause for 1.5 seconds to show "Correct!" message
            else:
                correct_answer = question.correct_answer
                if question.difficulty == "boolean":
                    correct_answer = "True" if correct_answer == "True" else "False"
                print(f"Incorrect. The correct answer is: {correct_answer}. Game over.")
                time.sleep(2)  # Pause to show the correct answer
                clear_screen()
                break

        print(f"Your final score is {self.score}")
        name = input("Enter your name to save your score: ").strip()
        self.score_manager.update_high_scores(name, self.score)
        print("Score saved!")
        time.sleep(2)
        clear_screen()
