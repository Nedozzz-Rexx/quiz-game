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
    base_url = "https://opentdb.com/api.php"
    amount = 50
    url = f"{base_url}?amount={amount}&difficulty={difficulty}&type={question_type}"
    logging.info(f"Generated API URL: {url}")
    return url

def clean_text(text):
    text = re.sub(r"&\w+;", "", text)
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def fetch_questions_from_api(url):
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
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'w') as file:
        json.dump(questions, file)
    logging.info(f"Saved questions to file: {filename}")

def load_questions_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    logging.info(f"Loaded questions from file: {filename}")
    return data

def get_questions(difficulty, question_type):
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


