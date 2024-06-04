from main_menu import Menu

def main():
    menu = Menu('menu.txt', 'instructions.txt')
    #score_manager = ScoreManager("high_scores.csv")
    #quiz_game = QuizGame(question_source, score_manager)  # question_source to be defined later

    while True:
        menu.display()
        choice = menu.get_choice()
        if choice == "1":
            difficulty = input("Choose difficulty (easy, moderate, hard): ")
            #quiz_game.generate_questions(difficulty)
            #quiz_game.play()
        elif choice == "2":
            #quiz_game.show_high_scores()
            print("Gotcha")
        elif choice == "3":
            menu.display_instructions()
        elif choice == "4":
            print("Thank you for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
