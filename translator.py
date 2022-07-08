from typing import List
from token_lexico import Token
import numpy as np
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from iteration_utilities import duplicates
from iteration_utilities import unique_everseen
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
        list_occurrences = []
        query = ''

        for token in table:
            word = token.text

            if(word in self.__inverted_index):
                list_occurrences += self.__inverted_index[word]

            query += word + ' '

        score = 0
        answer_index = 0

        temp_list = list(unique_everseen(duplicates(list_occurrences)))

        if(len(temp_list) != 0):
           list_occurrences = temp_list

        for index in list_occurrences:
            document = self.__answers[index].lower()

            list_text = [query, document]
            vectorizer = TfidfVectorizer(stop_words=self.__stopwords)
            vectorizer.fit_transform(list_text)
            tfidf_text1, tfidf_text2 = vectorizer.transform([list_text[0]]), vectorizer.transform([list_text[1]])
            temp_score = np.round(cosine_similarity(tfidf_text1, tfidf_text2)[0][0], 8)

            if(score < temp_score):
                score = temp_score
                answer_index = index

        return self.__answers[answer_index]

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
        with open('files/inverted_index.json', 'w') as outfile:
            json.dump(self.__inverted_index, outfile)