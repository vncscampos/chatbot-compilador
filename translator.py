from typing import List
from token_lexico import Token
import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Translator:
    def __init__(self, stopwords):
        self.__inverted_file = []
        self.__tfidf_matrix = {}
        self.__stopwords = stopwords

        try:
            for i in range(9):
                file_name = 'answers/ans' + str(i+1) + '.txt'
                file = open(file_name, 'r', encoding='utf8')
                text = file.readlines()
                msg = ''
                for j in range(len(text)):
                    msg += text[j]

                temp_dict = self.__tfidf_matrix
                ans_index = {i: {}}
                temp_dict.update(ans_index)
                self.__tfidf_matrix = temp_dict
                self.__inverted_file.append(msg)

        except FileNotFoundError as err:
            print(err)
            sys.exit()

    def response(self, query: str):
        ans = ''
        score = -1
        founded_words = 0
        query = query.split()

        for key in self.__tfidf_matrix:
            temp_score = 0
            temp_founded_words = 0

            for word in query:
                answer_words: dict = self.__tfidf_matrix[key]

                if(word in answer_words):
                    temp_founded_words += 1
                    temp_score += answer_words[word]
            

            if(founded_words < temp_founded_words):
                founded_words = temp_founded_words
                score = temp_score
                ans = self.__inverted_file[key]

            if(founded_words == temp_founded_words):
                if(score < temp_score):
                    founded_words = temp_founded_words
                    score = temp_score
                    ans = self.__inverted_file[key]

        return ans

    def tfidf_calc(self, table: List[Token]):
        for token in table:
            word = token.text

            for ans in range(len(self.__inverted_file)):
                list_text = [word, self.__inverted_file[ans]]
                vectorizer = TfidfVectorizer(stop_words=self.__stopwords)
                vectorizer.fit_transform(list_text)
                tfidf_text1, tfidf_text2 = vectorizer.transform([list_text[0]]), vectorizer.transform([list_text[1]])
                score = np.round(cosine_similarity(tfidf_text1, tfidf_text2)[0][0], 4)

                if(score != 0):
                    word_score = {}
                    word_score[word] = score

                    ans_texts: dict = self.__tfidf_matrix[ans]
                    ans_texts.update(word_score)

                    self.__tfidf_matrix[ans] = ans_texts
        
        self.__print_tfidf_matrix()

    def __print_tfidf_matrix(self):
        for index in range(8):
            print('{} = {}'.format(index, self.__tfidf_matrix[index]))

    


