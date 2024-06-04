class Menu:
    def __init__(self, menu_file, instructions_file):
        self.menu_file = menu_file
        self.instructions_file = instructions_file

    def display(self):
        with open(self.menu_file, 'r') as file:
            menu_content = file.read()
        print(menu_content)

    def display_instructions(self):
        with open(self.instructions_file, 'r') as file:
            instructions_content = file.read()
        print(instructions_content)

    def get_choice(self):
        return input("Enter your choice: ")
