import csv
import os
from collections import defaultdict
from typing import Dict, List

from dotenv import load_dotenv
import openai

import data_from_api

load_dotenv()

DATA_SOURCE_FILE_PATH = "datasource.txt"
FILE_OTPUT_PATH = "/Users/andreybolshakov/PycharmProjects/Test_tasks/Welltory/datasource_analyzed.csv"
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']


def read_reviews_from_file(file_path: str) -> List[Dict[str, str]]:
    """Reads a file with reviews and returns a list of dictionaries representing each review.

    Args:
        file_path (str): The path of the file containing the reviews.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing each review. Each dictionary has three keys:
            "Author", "review text", and "Date".
    """
    with open(file_path, 'r') as f:
        # read file as list of strings
        lines = f.readlines()
        # create list of dictionaries
        reviews = [{'Author': line.split('/')[0], 'review text': line.split('/')[1], 'Date': line.split('/')[2]}
                   for line in lines[1:]]
    return reviews


def get_api_key():
    return os.environ['OPENAI_API_KEY']


def get_openai_response(text):
    request = '''
    Rate the assessment emotional of user reviews on a scale of 1 to 10,
    where 10 is the most positive and 1 is the most negative.
    Try not to give the same ratings.
    Output only the rating number. | format:plain
    '''
    openai.api_key = get_api_key()
    prompt = f"{request}\n{text}"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=64)
    return response.choices[0].text.strip()


def clean_rating(rating):
    if not rating.isdigit():
        rating = ''.join(filter(str.isdigit, rating))
    return int(rating)


def get_author_ratings(reviews):
    author_ratings = defaultdict(int)
    for review in reviews:
        author = review['Author']
        text = review['review text']
        rating = get_openai_response(text)
        author_ratings[author] = clean_rating(rating)
    return author_ratings


def generate_email_list(reviews, analyzed_reviews):
    email_list = [{'Author': review['Author'], 'rate': analyzed_reviews[review['Author']]} for review in reviews]
    email_list.sort(key=lambda x: x['rate'], reverse=True)
    return email_list


def write_to_csv(file_path, email_list):
    output_file_path = os.path.join(os.path.dirname(file_path), "datasource_analyzed.csv")
    with open(output_file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=email_list[0].keys())
        writer.writeheader()
        for email in email_list:
            writer.writerow(email)


if __name__ == '__main__':
    data_from_api.main()
    data = read_reviews_from_file(DATA_SOURCE_FILE_PATH)
    analyzed_reviews = get_author_ratings(data)
    email_list = generate_email_list(data, analyzed_reviews)
    write_to_csv(FILE_OTPUT_PATH, email_list)
    print(f"Done, data has been written to {FILE_OTPUT_PATH}")
