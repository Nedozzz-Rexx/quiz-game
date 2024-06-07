from main_menu import Menu
from score_manager import ScoreManager
from quiz_game import QuizGame
from api import get_random_questions
from question import Question

def main():
    """
    The main function that runs the game.
    """
    menu = Menu('menu.txt', 'instructions.txt')
    score_manager = ScoreManager("high_scores.csv")

    while True:
        menu.display()
        choice = menu.get_choice()
        if choice == "1":
            question_type = None
            while question_type not in ["multiple", "boolean"]:
                print("Choose question type:")
                print("1. Multiple Choice Questions (MCQ)")
                print("2. True or False (T or F)")
                print("3. Go back to the main menu")
                question_type_choice = input("Your choice: ")
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
                questions = [Question(q['question'], q['incorrect_answers'] + [q['correct_answer']], q['correct_answer'], q['difficulty']) for q in questions_data]
                quiz_game = QuizGame(questions, score_manager)
                quiz_game.play()
        elif choice == "2":
            score_manager.display_high_scores()
        elif choice == "3":
            menu.display_instructions()
        elif choice == "4":
            print("Thank you for playing! Come play again soon!")
            break
        else:
            print("Make sure to pick a number from 1 - 4.")

if __name__ == "__main__":
    main()
