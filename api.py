import requests
import json
import os
import logging
import random
import re
import time

# Set up logging for debugging purposes, but default to WARNING to reduce verbosity
logging.basicConfig(level=logging.WARNING)

def generate_api_url(difficulty, question_type):
    """
    Generates a URL for the Open Trivia Database API based on the given difficulty and question type.

    Parameters:
        difficulty (str): The difficulty level of the questions.
        question_type (str): The type of questions.

    Returns:
        str: The generated URL.

    Example:
        >>> generate_api_url("easy", "multiple")
        'https://opentdb.com/api.php?amount=50&difficulty=easy&type=multiple'
    """
    base_url = "https://opentdb.com/api.php"
    amount = 50
    url = f"{base_url}?amount={amount}&difficulty={difficulty}&type={question_type}"
    logging.info(f"Generated API URL: {url}")
    return url

def clean_text(text):
    """
    Cleans the given text by removing special characters and whitespace.

    Parameters:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.

    This function removes special characters starting with '&' followed by one or more word characters and ending with ';'. 
    It then removes any characters that are not alphanumeric or whitespace from the text. 
    Finally, it replaces consecutive whitespace characters with a single space and strips any leading or trailing whitespace.

    Example:
        >>> clean_text("Hello, &world;! This is a test #123.")
        'Hello world! This is a test'
    """
    text = re.sub(r"&\w+;", "", text)
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def fetch_questions_from_api(url):
    '''
    Fetches questions from the API by making a GET request to the specified URL.

    Args:
        url (str): The URL of the API.

    Returns:
        list: A list of cleaned questions fetched from the API.

    This function makes a GET request to the specified URL and retrieves the response. It then checks the status code of the response. If the status code is 200, it proceeds to parse the JSON response. The function retrieves the 'response_code' from the JSON data. If the 'response_code' is 0, it iterates over the 'results' in the JSON data and cleans the 'question' using the 'clean_text' function. The cleaned questions are appended to a list. The list of cleaned questions is logged and returned.

    If the 'response_code' is not 0, it logs an error message based on the 'response_code' value.

    If the status code of the response is not 200, it logs an error message with the status code and the response text.

    If the status code is 429 (rate limit exceeded), it logs a warning message and retries the request after a delay.

    If the response status code is not 200, or the 'response_code' is not 0, or the 'response_code' is not a known value, an empty list is returned.
    '''
    retries = 3
    for attempt in range(retries):
        response = requests.get(url)
        logging.info(f"API Response Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            response_code = data.get('response_code', 1)
            if response_code == 0:
                cleaned_questions = []
                for result in data['results']:
                    result['question'] = clean_text(result['question'])
                    cleaned_questions.append(result)
                logging.info(f"Fetched questions from API: {cleaned_questions}")
                return cleaned_questions
            elif response_code == 1:
                logging.error("API Error: No results available for the query.")
                break
            elif response_code == 2:
                logging.error("API Error: Invalid parameter in the API request.")
                break
            elif response_code == 3:
                logging.error("API Error: Session token does not exist.")
                break
            elif response_code == 4:
                logging.error("API Error: Session token has returned all possible questions.")
                break
            else:
                logging.error(f"API Error: Unknown response code {response_code}.")
                break
        else:
            logging.error(f"Failed to fetch questions from API. Status code: {response.status_code}, Response: {response.text}")
            if response.status_code == 429:
                logging.warning("Rate limit exceeded. Retrying after a delay...")
                print("Loading... (Rate limit exceeded, retrying)")
                time.sleep(5 * (attempt + 1))
            else:
                break
    return []

def save_questions_to_file(questions, filename):
    """
    Saves the given list of questions to a JSON file at the specified filename.

    Args:
        questions (list): A list of dictionaries representing questions, where each dictionary has keys 'type', 'difficulty', 'category', 'question', 'correct_answer', and 'incorrect_answers'.
        filename (str): The name of the file to save the questions to.

    Returns:
        None

    Raises:
        None

    Side Effects:
        - Creates the directory specified by the filename if it does not already exist.
        - Writes the questions to the specified file in JSON format.

    Example Usage:
        questions = [
            {'type': 'multiple', 'difficulty': 'easy', 'category': 'General Knowledge', 'question': 'What is the capital of France?', 'correct_answer': 'Paris', 'incorrect_answers': ['London', 'Berlin', 'Madrid']},
            {'type': 'boolean', 'difficulty': 'hard', 'category': 'History', 'question': 'Was the Roman Empire founded by Augustus?', 'correct_answer': 'True', 'incorrect_answers': ['False']}
        ]
        save_questions_to_file(questions, 'questions.json')
    """

    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'w') as file:
        json.dump(questions, file)
    logging.info(f"Saved questions to file: {filename}")

def load_questions_from_file(filename):
    """
    Load questions from a JSON file.

    Args:
        filename (str): The name of the file to load.

    Returns:
        dict: The loaded JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not in JSON format.
    """
    with open(filename, 'r') as file:
        data = json.load(file)
    logging.info(f"Loaded questions from file: {filename}")
    return data

def get_questions(difficulty, question_type):
    """
    Retrieves a list of questions from a file or from the API based on the difficulty and question type.

    Args:
        difficulty (str): The difficulty level of the questions (easy, medium, hard).
        question_type (str): The type of questions (multiple, true_false).

    Returns:
        list: A list of questions. If the list contains at least 15 questions, it is returned. Otherwise, more questions are fetched from the API. If the API fails, questions from the file are returned if available.

    Raises:
        FileNotFoundError: If the file containing the questions is not found.
        json.JSONDecodeError: If the file containing the questions is not in JSON format.

    """
    filename = f"data/{difficulty}_{question_type}_questions.json"
    try:
        questions = load_questions_from_file(filename)
        if len(questions) >= 15:
            logging.info(f"Loaded {len(questions)} questions from file: {filename}")
            return questions
        else:
            logging.warning(f"Loaded only {len(questions)} questions from file: {filename}. Fetching more from API.")
    except (FileNotFoundError, json.JSONDecodeError):
        logging.info(f"File not found or invalid JSON format: {filename}. Fetching from API.")

    url = generate_api_url(difficulty, question_type)
    questions = fetch_questions_from_api(url)
    if questions:
        save_questions_to_file(questions, filename)
        return questions
    else:
        logging.warning(f"Returning questions from file due to API failure: {filename}")
        try:
            return load_questions_from_file(filename)
        except (FileNotFoundError, json.JSONDecodeError):
            logging.error(f"No valid questions available for {difficulty} {question_type}.")
            return []

def get_random_questions(question_type):
    """
    Retrieves a specified number of random questions from the Open Trivia Database API for each difficulty level.

    Parameters:
        question_type (str): The type of questions to retrieve.

    Returns:
        list: A list of randomly selected questions from the API, with each question containing the following fields:
            - type (str): The type of question.
            - difficulty (str): The difficulty level of the question.
            - category (str): The category of the question.
            - question (str): The question itself.
            - correct_answer (str): The correct answer to the question.
            - incorrect_answers (list): A list of incorrect answers to the question.

    Raises:
        Exception: If there is an error fetching questions from the API.

    Example:
        >>> get_random_questions("multiple")
        [
            {
                "type": "multiple",
                "difficulty": "easy",
                "category": "Entertainment: Film",
                "question": "Who played Deputy Marshal Samuel Gerard in the 1993 film The Fugitive",
                "correct_answer": "Tommy Lee Jones",
                "incorrect_answers": ["Harrison Ford", "Harvey Keitel", "Martin Landau"]
            },
            ...
        ]
    """
    selected_questions = []
    difficulties = ["easy", "medium", "hard"]
    num_questions_per_difficulty = 5  # Adjust this number as needed
    
    print("Loading question...")

    for difficulty in difficulties:
        try:
            difficulty_questions = get_questions(difficulty, question_type)
            random.shuffle(difficulty_questions)  # Shuffle questions within the difficulty level
            selected_questions.extend(difficulty_questions[:num_questions_per_difficulty])
        except Exception as e:
            logging.error(f"Error fetching questions for {difficulty} {question_type}: {e}")
            continue

    return selected_questions


