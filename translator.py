from typing import List
from token_lexico import Token
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import SnowballStemmer
import re

class Translator:
    def __init__(self, stopwords, answers):
        self.__answers = answers
        self.__stopwords = stopwords
        self.__inverted_file = {}

    def response(self, query: str):
        query = query.split()

        temp_score = 0
        answer_index = 0
        for word in query:
            if(word in self.__inverted_file):
                scores = self.__inverted_file[word]
                max_score = max(scores)
                max_index = scores.index(max_score)

                if(temp_score < max_score):
                    temp_score = max_score
                    answer_index = max_index


        return self.__answers[answer_index]

    def tfidf_calc(self, table: List[Token]):
        for token in table:
            word = token.text

            temp_list = [0] * (len(self.__inverted_file)-1)
            for i in range(len(self.__answers)):
                new_answer = self.__ans_lexeme(self.__answers[i])
                list_text = [self.__lexeme(word), new_answer]

                vectorizer = TfidfVectorizer(stop_words=self.__stopwords)
                vectorizer.fit_transform(list_text)
                tfidf_text1, tfidf_text2 = vectorizer.transform([list_text[0]]), vectorizer.transform([list_text[1]])
                score = np.round(cosine_similarity(tfidf_text1, tfidf_text2)[0][0], 4)

                temp_list.insert(i, score)
            
            word_index = {}
            word_index[word] = temp_list
            temp_dict = self.__inverted_file
            temp_dict.update(word_index)
            self.__inverted_file = temp_dict

    def __ans_lexeme(self, answer: str):
        new_answer: str = answer.lower()

        new_answer: list = re.sub('[^a-záàâãéèêíóôõúçA-Z0-9 \n]', '', new_answer).split(' ')

        temp_text = new_answer
        for word in temp_text:
            if(word in self.__stopwords):
                text = list(filter((word).__ne__, new_answer))

        new_answer = text

        temp = ''
        for word in new_answer:
            if(type(word) is str):
                temp += self.__lexeme(word) + ' '

        new_answer = temp
        return new_answer

    def __lexeme(self, word: str):
        # https://www.nltk.org/_modules/nltk/stem/snowball.html
        snow_stemmer = SnowballStemmer(language='portuguese')
        return snow_stemmer.stem(word)
