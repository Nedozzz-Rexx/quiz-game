from main_menu import Menu
from score_manager import ScoreManager
from quiz_game import QuizGame
from api import get_random_questions
from question import Question
import time
from utils import getch, clear_screen  # Import the functions from utils.py

def print_slow(text, delay=0.005):
    """
    Print each character of the text with a delay.
    
    Parameters:
        text (str): The text to print.
        delay (float): The delay (in seconds) between printing each character. Default is 0.1 seconds.
    """
    for line in text.splitlines():
        for char in line:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()  # Move to the next line after printing the entire line

def print_ascii_art(file_path):
    """
    Print ASCII art from a file.
    
    Parameters:
        file_path (str): The path to the ASCII art file.
    """
    with open(file_path, 'r') as file:
        ascii_art = file.read()
    print(ascii_art)

def main():
    """
    The main function of the program. It initializes a Menu object and a ScoreManager object. 
    It then enters a loop where it displays the menu, gets the user's choice, and performs the corresponding action. 
    The loop continues until the user chooses to exit.

    Parameters:
        None

    Returns:
        None
    """
    menu = Menu('menu.txt', 'instructions.txt')
    score_manager = ScoreManager("high_scores.csv")
    first_display = True

    while True:
        
        menu.display()
        choice = menu.get_choice()

        print("Choice:", choice)  # Add a print statement to check the user's choice

        if choice == "1":
            question_type = None
            while question_type not in ["multiple", "boolean"]:
                print("Choose question type:")
                print("1. Multiple Choice Questions (MCQ)")
                print("2. True or False (T or F)")
                print("3. Go back to the main menu")
                question_type_choice = input("Your choice: ").strip().lower()
                if question_type_choice == "1":
                    question_type = "multiple"
                elif question_type_choice == "2":
                    question_type = "boolean"
                elif question_type_choice == "3":
                    break  # Go back to the main menu
                else:
                    print("Invalid choice. Please choose 1, 2, or 3.")
                    continue

            if question_type:
                questions_data = get_random_questions(question_type)
                questions = [Question(
                    question_type=q['type'], 
                    difficulty=q['difficulty'], 
                    category=q['category'], 
                    question=q['question'], 
                    correct_answer=q['correct_answer'], 
                    incorrect_answers=q['incorrect_answers']
                ) for q in questions_data]
                quiz_game = QuizGame(questions, score_manager)
                quiz_game.play()
        elif choice == "2":
            clear_screen()
            print_ascii_art('score_screen.txt')
            score_manager.display_high_scores()
            print("Press any key to return to the main menu")
            getch()  # Wait for a key press
            clear_screen()  # Clear the screen
        elif choice == "3":
            clear_screen()
            menu.display_instructions()
            print("Press any key to return to the main menu")
            getch()  # Wait for a key press
            clear_screen()  # Clear the screen
        elif choice == "4":
            print_ascii_art('end_screen.txt')
            break
        else:
            print("Make sure to pick a number from 1 - 4.")

if __name__ == "__main__":
    main()
