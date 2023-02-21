import csv

FILE_PATH = "https://docs.google.com/spreadsheets/d/1RpHXQgM1_1zIrLdbjM7HxpgfLNvDBWrqTZSeHd7CikA/edit?usp=sharing"
FILE_OTPUT_PATH = "/Users/andreybolshakov/PycharmProjects/Test_tasks/Welltory/file_analyzed.csv"


def read_csv_file(filepath):
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def analyze_reviews(reviews):
    for review in reviews:
        text = review['review text']
        # Perform analysis of the text
        # Set the rating in the "Rate" field
        review['Rate'] = 5  # Replace this with the actual rating determined from the analysis

    # Sort the reviews by rating in descending order
    reviews.sort(key=lambda x: x['Rate'], reverse=True)
    return reviews


def write_analyzed_reviews_to_csv(file_path, reviews):
    file_name = file_path.split('/')[-1].split('.')[0]
    new_file_name = f"{file_name}_analyzed.csv"
    with open(new_file_name, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=reviews[0].keys())
        writer.writeheader()
        for review in reviews:
            writer.writerow(review)


def generate_email_list(reviews):
    email_list = []
    for review in reviews:
        email_list.append(f"{review['Author']} - rate: {review['Rate']}")
    return email_list


if __name__ == '__main__':
    file_path = "path/to/file.csv"
    reviews = read_csv_file(FILE_PATH)
    analyzed_reviews = analyze_reviews(reviews)
    write_analyzed_reviews_to_csv(FILE_PATH, analyzed_reviews)
    email_list = generate_email_list(analyzed_reviews)
    print(email_list)
