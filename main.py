from main_menu import Menu
from score_manager import ScoreManager
from quiz_game import QuizGame
from api import get_questions
from question import Question

def main():
    menu = Menu('menu.txt', 'instructions.txt')
    score_manager = ScoreManager("high_scores.csv")

    while True:
        menu.display()
        choice = menu.get_choice()
        if choice == "1":
            difficulty = input("Choose difficulty (easy, medium, hard): ").lower().strip()
            while difficulty not in ["easy", "medium", "hard"]:
                print("Invalid choice. Please choose 'easy', 'medium', or 'hard'.")
                difficulty = input("Choose difficulty (easy, medium, hard): ").lower().strip()

            question_type = input("Choose question type (multiple, boolean): ").lower().strip()
            while question_type not in ["multiple", "boolean"]:
                print("Invalid choice. Please choose 'multiple' or 'boolean'.")
                question_type = input("Choose question type (multiple, boolean): ").lower().strip()

            try:
                questions_data = get_questions(difficulty, question_type)
                questions = [Question(q['question'], q['incorrect_answers'] + [q['correct_answer']], q['correct_answer'], difficulty) for q in questions_data]
                quiz_game = QuizGame(questions, score_manager)
                quiz_game.play()
            except Exception as e:
                print(f"An error occurred while fetching questions: {e}")
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
