from main_menu import Menu

def main():
    """
    The main function that runs the game.

    This function initializes the menu and score manager objects, and enters a loop to display the menu and handle user choices. 
    The menu is displayed using the `display` method of the `Menu` class, and the user's choice is obtained using the `get_choice` method of the `Menu` class.

    If the user selects option 1. The `play` method of the `QuizGame` class is then called to start the quiz.

    If the user selects option 2, the `show_high_scores` method of the `QuizGame` class is called to display the high scores.

    If the user selects option 3, the instructions are displayed using the `display_instructions` method of the `Menu` class.

    If the user selects option 4, a thank you message is displayed, and the loop is broken to exit the game.

    If the user selects an invalid option, an error message is displayed, and the loop continues to display the menu.

    This function does not take any parameters and does not return any values.
    """
    menu = Menu('menu.txt', 'instructions.txt')
    #score_manager = ScoreManager("high_scores.csv")
    #quiz_game = QuizGame(question_source, score_manager)  # question_source to be defined later

    while True:
        menu.display()
        choice = menu.get_choice()
        if choice == "1":
            print("Gotcha")
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
