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
            question_type = input("Choose question type (multiple, boolean): ").lower()
            while question_type not in ["multiple", "boolean"]:
                print("Invalid choice. Please choose 'multiple' or 'boolean'.")
                question_type = input("Choose question type (multiple, boolean): ").lower()

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
