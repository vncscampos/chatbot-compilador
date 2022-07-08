import sys

class File:
    def __init__(self):
        pass

    def read_stopwords(self):
        try:
            file = open('stopwords.txt', 'r', encoding='utf8')
            stopwords = [line[:-1] for line in file]

            return stopwords

        except FileNotFoundError as err:
            print(err)
            sys.exit()  

    def read_answers(self):
        answers: list = []
        
        try:
            for i in range(9):
                file_name = 'answers/ans' + str(i+1) + '.txt'
                file = open(file_name, 'r', encoding='utf8')
                text = file.readlines()
                msg = ''
                for j in range(len(text)):
                    msg += text[j]

                answers.append(msg)

            return answers

        except FileNotFoundError as err:
            print(err)
            sys.exit()