import sys
import nltk
import re
import heapq
import numpy as np
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Translator:
    def __init__(self, stopwords):
        self.__inverted_file = []
        self.__tfidf_matrix = []
        self.__stopwords = stopwords

        try:
            for i in range(7):
                file_name = 'answers/ans' + str(i+1) + '.txt'
                file = open(file_name, 'r', encoding='utf8')
                text = file.readlines()
                msg = ''
                for j in range(len(text)):
                    msg += text[j]
                self.__inverted_file.append(msg)
        except FileNotFoundError as err:
            print(err)
            sys.exit()

        # self.__create_tfidf()
        
    def translate(self, table):
        ans = ''
        score = 0

        query = ''
        for tab in table:
            query += tab.text + ' '

        for i in range(len(self.__inverted_file)):
            list_text = [query, self.__inverted_file[i]]
            vectorizer = TfidfVectorizer(stop_words=self.__stopwords)
            vectorizer.fit_transform(list_text)
            tfidf_text1, tfidf_text2 = vectorizer.transform([list_text[0]]), vectorizer.transform([list_text[1]])

            print(vectorizer)

            cs_score = np.round(cosine_similarity(tfidf_text1, tfidf_text2)[0][0], 2)
            if(score < cs_score):
                score = cs_score
                ans = self.__inverted_file[i]
        
        return ans


    def __create_tfidf(self):
        for i in range(len(self.__inverted_file)):
            text = self.__inverted_file[0]
            dataset = self.__pre_processing(text)
            word2count = self.__create_histogram(dataset)
            freq_words = heapq.nlargest(50,word2count, key=word2count.get)
            word_idfs = self.__create_idf(dataset, freq_words)
            tfidf_matrix = self.__calculate_freq(dataset, word_idfs, freq_words)
            self.__tfidf_matrix.append(tfidf_matrix)

    def __pre_processing(self, text):
        dataset = nltk.sent_tokenize(text)
        for i in range (len(dataset)):
            dataset[i] = dataset[i].lower() #converte todas as palavras para letras minusculas
        return dataset

    def __create_histogram(self, dataset):
        word2count = {}
        for data in dataset:
            words = nltk.word_tokenize(data)
            for word in words:
                if word not in word2count.keys():
                    word2count[word] = 1
                else:
                    word2count[word] += 1

        return word2count

    def __create_idf(self, dataset, freq_words):
        word_idfs = {}
        for word in freq_words:
            doc_count = 0 
            for data in dataset:
                if word in nltk.word_tokenize(data):
                    doc_count += 1
            word_idfs[word] = np.log((len(dataset)/doc_count)+1)
            
        return word_idfs

    def __calculate_freq(self, dataset, word_idfs, freq_words):
        tf_matrix = {}

        for word in freq_words:
            doc_tf = []
            for data in dataset:
                frequency = 0
                for w in nltk.word_tokenize(data):
                    if w == word:
                        frequency += 1
                tf_word = frequency/len(nltk.word_tokenize(data))
                doc_tf.append(tf_word)
            tf_matrix[word] = doc_tf

        tfidf_matrix = []

        for word in tf_matrix.keys():
            tfidf = []
            for value in tf_matrix[word]:
                score = value * word_idfs[word]
                tfidf.append(score)
            tfidf_matrix.append(tfidf)
            
        return tfidf_matrix
