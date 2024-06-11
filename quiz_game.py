import os
import time
from utils import getch, clear_screen
import sys  # to use animation effect
import random  # to use shuffle function

class QuizGame:

    def __init__(self, questions, score_manager):
        """
        Initializes a new instance of the QuizGame class.

        Args:
            questions (list): A list of question objects.
            score_manager (ScoreManager): An instance of the ScoreManager class.

        Returns:
            None

        This constructor initializes the QuizGame object with the provided questions and score manager.
        It also initializes the score attribute to 0.
        """
        self.questions = questions
        self.score_manager = score_manager
        self.score = 0

    def print_ascii_art(self, file_path):
        """
        Prints ASCII art from a text file.

        Args:
            file_path (str): The path to the text file containing the ASCII art.

        Returns:
            None
        """
        try:
            with open(file_path, "r") as file:
                ascii_art = file.read()
                print(ascii_art)
        except FileNotFoundError:
            print("Error: ASCII art file not found.")

    def print_with_animation(self, text):
        """
        Prints the given text with an animation effect.

        Args:
            text (str): The text to be printed with animation.

        Returns:
            None

        This function iterates over each character in the given text and prints it one by one.
        It flushes the output after each character to ensure immediate display.
        The function also adds a small delay of 0.03 seconds between each character to create an animation effect.
        """
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)  # Adjust the speed of animation here

    def print_countdown(self):
        """
        Prints a countdown from 3 to 1, followed by "Let's go!" and a delay of 1 second.
        Clears the screen after the countdown and delay.

        This function does not take any parameters.

        This function does not return any value.
        """
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)
        print("Let's go!")
        time.sleep(1)
        clear_screen()

    def announce_start(self):
        """
        Announces the start of the quiz and prints a countdown from 3 to 1.
        
        This function does not take any parameters.
        
        This function does not return any value.
        """
        print("Get ready! The quiz is about to start!")
        self.print_countdown()

    def announce_easy_questions(self):
        """
        Announces the start of the easy questions and prints a countdown from 3 to 1.

        This function does not take any parameters.

        This function does not return any value.
        """
        clear_screen()
        print("We're starting with the easy questions. Think you can get them all right?")
        self.print_countdown()

    def announce_medium_questions(self):
        """
        Announces the start of the medium questions and prints a countdown from 3 to 1.

        This function does not take any parameters.

        This function does not return any value.
        """
        clear_screen()
        print("Were these too easy? Now the questions will have medium difficulty.")
        self.print_countdown()

    def announce_hard_questions(self):
        """
        Announces the start of the hard questions and prints a countdown from 3 to 1.

        This function does not take any parameters.

        This function does not return any value.
        """
        clear_screen()
        print("Now it's time for the hard questions. Good luck!")
        self.print_countdown()

    def randomize_answers(self, question):
        """
        Randomizes the order of the answers for a given question.

        Args:
            question (Question): The question object containing the correct answer and incorrect answers.

        Returns:
            list: A list of answers in randomized order, with the correct answer included.
        """
        all_answers = question.incorrect_answers[:]
        all_answers.append(question.correct_answer)
        random.shuffle(all_answers)
        return all_answers

    def play(self):
        """
        Plays the quiz game.

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

        if self.score == 45:  # This is the most points a person can score, meaning they won!
            self.print_ascii_art('congrats.txt')
            
            time.sleep(5)
            clear_screen()
        else:
            input("Press any key to return to the main menu")


