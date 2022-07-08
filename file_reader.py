import sys
import pathlib

class File:
    def __init__(self):
        self.files_count = 0
        self.answers = []

        try:
            with open ('files/number_answers.txt', 'r') as file:
                self.files_count = int(file.readline())
        except:
            self.files_count = 0

    def read_stopwords(self):
        try:
            file = open('files/stopwords.txt', 'r', encoding='utf8')
            stopwords = [line[:-1] for line in file]
            file.close()

            return stopwords

        except FileNotFoundError as err:
            print(err)
            sys.exit()  

    def read_answers(self):
        answers: list = []

        initial_count = 0
        for path in pathlib.Path("./answers").iterdir():
            if path.is_file():
                initial_count += 1

        try:
            for i in range(initial_count):
                file_name = 'answers/ans' + str(i+1) + '.txt'
                file = open(file_name, 'r', encoding='utf8')
                text = file.readlines()
                msg = ''
                for j in range(len(text)):
                    msg += text[j]

                answers.append(msg)
                file.close()

            has_new_files = False
            if(len(answers) != self.files_count):
                has_new_files = True

            self.answers = answers

            return answers, has_new_files

        except FileNotFoundError as err:
            print(err)
            sys.exit()

    def save_size_answers(self):
        with open('files/number_answers.txt', 'w') as f:
            f.write(str(len(self.answers)))
            f.close()