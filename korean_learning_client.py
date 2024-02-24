import csv
import random
import os
import shutil

class KoreanLearningClient:
    def __init__(self, csv_file_path, words_to_learn_path):
        self.csv_file_path = csv_file_path
        self.words_to_learn_path = words_to_learn_path
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

    def remove_word_pair(self, word_pair):
        if not os.path.exists(self.words_to_learn_path):
            shutil.copy(self.csv_file_path, self.words_to_learn_path)
        with open(self.words_to_learn_path, 'r', encoding='utf-8') as file:
            data = [row for row in csv.reader(file) if row != word_pair]


        with open(self.words_to_learn_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)


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

