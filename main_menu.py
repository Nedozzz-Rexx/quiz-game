class Menu:
    def __init__(self, menu_file, instructions_file):
        """
        Initializes a new instance of the Menu class with the specified menu file and instructions file.

        Parameters:
            menu_file (str): The file path of the menu file.
            instructions_file (str): The file path of the instructions file.
        """
        self.menu_file = menu_file
        self.instructions_file = instructions_file

    def display(self):
        """
        Displays the content of the menu file.

        This function opens the menu file specified during the initialization of the Menu class and reads its content. 
        It then prints the content to the console.

        Parameters:
            self (Menu): The current instance of the Menu class.

        Returns:
            None
        """
        with open(self.menu_file, 'r') as file:
            menu_content = file.read()
        print(menu_content)

    def display_instructions(self):
        """
        Displays the instructions content from the instructions file.

        This function opens the instructions file specified during the initialization of the Menu class and reads its content. 
        It then prints the content to the console.

        Parameters:
            self (Menu): The current instance of the Menu class.

        Returns:
            None
        """
        with open(self.instructions_file, 'r') as file:
            instructions_content = file.read()
        print(instructions_content)

    def get_choice(self):
        """
        Get the user's choice by prompting them to enter their choice.

        Returns:
            str: The user's choice as a string.
        """
        return input("Are you excited?! Go ahead and pick your choice: ")
