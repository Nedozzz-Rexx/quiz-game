import requests
import json
import os
import logging
import random

# Comment out the desired logging level for normal execution or debugging
logging.basicConfig(level=logging.WARNING)  # For normal execution
# logging.basicConfig(level=logging.DEBUG)  # For debugging

def generate_api_url(difficulty, question_type):
    """
    Generates a URL for the Open Trivia Database API with the given difficulty and question type.

    Args:
        difficulty (str): The difficulty of the questions. Must be one of 'easy', 'medium', or 'hard'.
        question_type (str): The type of questions. Must be one of 'multiple' or 'boolean'.

    Returns:
        str: The generated URL for the API.

    """
    base_url = "https://opentdb.com/api.php"
    amount = 5
    url = f"{base_url}?amount={amount}&difficulty={difficulty}&type={question_type}"
    logging.info(f"Generated API URL: {url}")
    return url

def fetch_questions_from_api(url):
    """
    Fetches questions from the Open Trivia Database API based on the given URL.

    Args:
        url (str): The URL of the Open Trivia Database API.

    Returns:
        list: A list of questions fetched from the API. 
        If the API request fails or the response code is not 0, an empty list is returned.

    Raises:
        None

    Logs:
        - Information: The API response status code.
        - Information: The fetched questions from the API if the response code is 0.
        - Error: If the API request fails or the response code is not 0.

    """
    response = requests.get(url)
    logging.info(f"API Response Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if data['response_code'] == 0:
            logging.info(f"Fetched questions from API: {data['results']}")
            return data['results']
    logging.error("Failed to fetch questions from API")
    return []

def save_questions_to_file(questions, filename):
    """
    Saves a list of questions to a file with the given filename.

    Parameters:
        questions (list): A list of questions to be saved.
        filename (str): The name of the file to save the questions to.

    Returns:
        None

    Raises:
        None

    Logs:
        - Information: The file path where the questions were saved.

    """
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'w') as file:
        json.dump(questions, file)
    logging.info(f"Saved questions to file: {filename}")

def load_questions_from_file(filename):
    """
    Load questions from a file.

    This function reads the contents of a file with the given filename and
    loads the data as a JSON object. The loaded data is then returned.

    Parameters:
        filename (str): The name of the file to load the questions from.

    Returns:
        dict: The loaded questions as a JSON object.

    Logs:
        - Information: The file path where the questions were loaded from.
    """
    with open(filename, 'r') as file:
        data = json.load(file)
    logging.info(f"Loaded questions from file: {filename}")
    return data

def get_questions(difficulty, question_type):
    """
    Retrieves questions from a file or fetches them from the API if the file does not exist or is invalid.

    Parameters:
        difficulty (str): The difficulty level of the questions. Must be one of 'easy', 'medium', or 'hard'.
        question_type (str): The type of questions. Must be one of 'multiple' or 'boolean'.

    Returns:
        list: A list of questions retrieved from the file or API.

    Raises:
        Exception: If the questions cannot be fetched from the API.

    Logs:
        - Information: If the file is not found or has invalid JSON format, a message is logged indicating that the questions are being fetched from the API.
        - Information: The generated API URL is logged.
        - Information: The questions are saved to a file after being fetched from the API.
        - Error: If the API request fails with a non-200 status code.
        - Error: If an error occurs during the API request.

    """
    filename = f"data/{difficulty}_{question_type}_questions.json"
    try:
        return load_questions_from_file(filename)
    except (FileNotFoundError, json.JSONDecodeError):
        logging.info(f"File not found or invalid JSON format: {filename}. Fetching from API.")
        url = generate_api_url(difficulty, question_type)
        questions = fetch_questions_from_api(url)
        if questions:
            save_questions_to_file(questions, filename)
            return questions
        else:
            raise Exception("Failed to fetch questions from API.")

def get_random_questions(question_type):
    """
    Returns a list of 15 random questions from the specified question type.

    Args:
        question_type (str): The type of question to retrieve.

    Returns:
        list: A list of 15 random questions.

    Raises:
        None

    """
    questions = []
    difficulties = ["easy", "medium", "hard"]
    for difficulty in difficulties:
        difficulty_questions = get_questions(difficulty, question_type)
        questions.extend(difficulty_questions)

    # Shuffle and return 15 questions, 5 from each difficulty level
    random.shuffle(questions)
    return questions[:15]

# For testing purposes
#if __name__ == "__main__":
 #   easy_mcq_questions = get_questions("easy", "multiple")
  #  print(easy_mcq_questions)
