import csv
import os
from collections import defaultdict

from dotenv import load_dotenv

import openai

import data_from_api

load_dotenv()

FILE_PATH = "datasource.txt"
FILE_OTPUT_PATH = "/Users/andreybolshakov/PycharmProjects/Test_tasks/Welltory/file_analyzed.csv"


# read txt fiel and return list of dictionaries
def read_txt_file(FILE_PATH):
    with open(FILE_PATH, 'r') as f:
        # read file as list of strings
        lines = f.readlines()
        # create list of dictionaries
        reviews = []
        for line in lines[1:]:
            # create dictionary
            dictionary = {'Author': line.split('/')[0], 'review text': line.split('/')[1], 'Date': line.split('/')[2]}
            # add dictionary to list
            reviews.append(dictionary)
    return reviews


def analyze_reviews(reviews):
    """
    Analyzes the sentiment of each review using OpenAI's GPT-3 API and returns a dictionary mapping each author's email
    address to their review's rating on a scale from 1 to 10.
    """
    request = '''
Rate the assessment emotional of user reviews on a scale of 1 to 10,
where 10 is the most positive and 1 is the most negative.
Try not to give the same ratings.
Output only the rating number. | format:plain
    '''
    # Load OpenAI API key from environment variable
    openai.api_key = os.environ['OPENAI_API_KEY']

    # Create a defaultdict to store each author's review and its rating
    author_ratings = defaultdict(int)

    # Loop over all reviews and analyze their sentiment using OpenAI's GPT-3 API
    for review in reviews:
        author = review['Author']
        text = review['review text']
        prompt = f"{request}\n{text}"
        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=64)
        rating = response.choices[0].text.strip()
        # author_ratings[author] = int(rating)
        # check if rating is not digitized, find in sthe string only digits and convert to int
        if not rating.isdigit():
            rating = ''.join(filter(str.isdigit, rating))
            author_ratings[author] = int(rating)
        else:
            author_ratings[author] = int(rating)

    return author_ratings


def generate_email_list(reviews, analyzed_reviews):
    email_list = []
    for review in reviews:
        email_list.append({'Author': review['Author'], 'rate': analyzed_reviews[review['Author']]})
        email_list.sort(key=lambda x: x['rate'], reverse=True)
    return email_list


def write_to_csv(file_path, email_list):
    file_name = file_path.split('/')[-1].split('.')[0]
    new_file_name = f"{file_name}_analyzed.csv"
    with open(new_file_name, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=email_list[0].keys())
        writer.writeheader()
        for email in email_list:
            writer.writerow(email)


if __name__ == '__main__':
    data_from_api.main()
    data = read_txt_file(FILE_PATH)
    analyzed_reviews = analyze_reviews(data)
    email_list = generate_email_list(data, analyzed_reviews)
    write_to_csv(FILE_PATH, email_list)
