import csv
import random

class KoreanLearningClient:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.random_pair = None


    def get_random_pair(self):
        pairs = []
        with open(self.csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                korean_word, english_translation = row
                pairs.append((korean_word.strip(), english_translation.strip()))

        random_pair = random.choice(pairs)
        return random_pair

    def generate_options(self, correct_translation):
        with open(self.csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            pairs = [row for row in reader]
            random_pairs = random.sample(pairs, 3)
            options = [pair[1] for pair in random_pairs]
            options.append(correct_translation)
            random.shuffle(options)
            return options

