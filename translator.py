from typing import List
from token_lexico import Token
import numpy as np
import re
import json

class Translator:
    def __init__(self, stopwords, answers, has_new_answers: bool):
        self.__answers: List[str] = answers
        self.__stopwords: List[str] = stopwords

        if(has_new_answers):
            self.__inverted_index = self.generate_inverted_index()
        else:
            try:
                file = open('inverted_index.json')
                self.__inverted_index = json.load(file)
                file.close()
            except:
                self.__inverted_index = self.generate_inverted_index()

    def translate(self, table: List[Token]):
        tf_idf = 0
        index = 0

        for token in table:
            word = token.text

            if(word in self.__inverted_index):
                    occurrences = self.__inverted_index[word]
                    for j in occurrences:
                        document = self.__answers[j]

                        temp_tf_idf = self.term_freq(document, word) * self.inverse_doc_freq(word)

                        if(tf_idf < temp_tf_idf):
                            tf_idf = temp_tf_idf
                            index = j

        return self.__answers[index]


    def term_freq(self, document: str, word: str):
        N = len(re.findall(r'\w+', document))
        occurrence = document.lower().count(word)
        return occurrence/N
    
    def document_freq(self, word):
        return len(self.__inverted_index[word])

    def inverse_doc_freq(self, word):
        return np.log(len(self.__answers)/self.document_freq(word)+1)

    def generate_inverted_index(self):
        inverted_index = {}

        for index, text in enumerate(self.__answers):
            answer = self.pre_processing(text)

            for word in answer:
                if word not in inverted_index.keys():
                    inverted_index[word] = [index]
                elif index not in inverted_index[word]:
                    inverted_index[word].append(index)

        return inverted_index

    def pre_processing(self, text):
        text = text.lower()
        text = re.sub('[!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n]', '', text).split(' ')
        for word in text:
            if(word in self.__stopwords):
                text = list(filter((word).__ne__, text))

        return text

    def save_inverted_index(self):
        with open('inverted_index.json', 'w') as outfile:
            json.dump(self.__inverted_index, outfile)
            outfile.close()
