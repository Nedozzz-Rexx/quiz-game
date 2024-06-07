import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

def fetch_questions_from_api(url):
    try:
        response = requests.get(url)
        logging.info("API Response Status Code: %d", response.status_code)
        if response.status_code == 200:
            data = response.json()
            if data['response_code'] == 0:
                return data['results']
        else:
            logging.error("API request failed with status code %d", response.status_code)
    except Exception as e:
        logging.error("An error occurred during API request: %s", str(e))
    return []

# Example usage
url = "https://opentdb.com/api.php?amount=5&difficulty=easy&type=multiple"
questions = fetch_questions_from_api(url)
if questions:
    logging.info("Fetched questions from API: %s", questions)
else:
    logging.error("Failed to fetch questions from API")
