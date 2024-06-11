# utils.py
import os
import sys
import tty
import termios

def clear_screen():
    """
    Clears the terminal screen.

    This function checks the operating system and clears the screen accordingly.
    On Windows, it uses the 'cls' command, while on Unix-based systems (Linux, macOS),
    it uses the 'clear' command.

    Parameters:
        None

    Returns:
        None
    """
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-based systems (Linux, macOS)
        os.system('clear')

def getch():
    """
    Get a single character from the user's input.

    This function reads a single character from the user's input. It first checks the
    operating system to determine the appropriate method for reading the character.
    On Windows, it uses the `msvcrt.getch()` function to get the character. On Unix-based
    systems (Linux, macOS), it sets the terminal to raw mode, reads a single character,
    and then restores the terminal settings.

    Returns:
        str: The single character read from the user's input.

    Raises:
        None
    """
    if os.name == 'nt':  # For Windows
        import msvcrt
        return msvcrt.getch().decode('utf-8')
    else:  # For Unix-based systems (Linux, macOS)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
