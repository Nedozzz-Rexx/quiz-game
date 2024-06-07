import requests
import json
import os
import logging

# Comment out the desired logging level for normal execution or debugging
logging.basicConfig(level=logging.WARNING)  # For normal execution
# logging.basicConfig(level=logging.DEBUG)  # For debugging

def generate_api_url(difficulty, question_type):
    base_url = "https://opentdb.com/api.php"
    amount = 5
    url = f"{base_url}?amount={amount}&difficulty={difficulty}&type={question_type}"
    logging.info(f"Generated API URL: {url}")
    return url

def fetch_questions_from_api(url):
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
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'w') as file:
        json.dump(questions, file)
    logging.info(f"Saved questions to file: {filename}")

def load_questions_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
        # Comment out the detailed logging of content
        # logging.info(f"Reading from file {filename}: {content}")
        data = json.loads(content)
    logging.info(f"Loaded questions from file: {filename}")
    return data

def get_questions(difficulty, question_type):
    filename = f"data/{difficulty}_{question_type}_questions.json"
    try:
        return load_questions_from_file(filename)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.info(f"File not found or invalid JSON format: {filename}. Fetching from API.")
        url = generate_api_url(difficulty, question_type)
        questions = fetch_questions_from_api(url)
        if questions:
            save_questions_to_file(questions, filename)
            return questions
        else:
            raise Exception("Failed to fetch questions from API.")

# For testing purposes
#if __name__ == "__main__":
 #   easy_mcq_questions = get_questions("easy", "multiple")
  #  print(easy_mcq_questions)
