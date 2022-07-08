#!/bin/python3
from lexico import Lexico
from translator import Translator
from file_reader import File

file_reader = File()
stopwords = file_reader.read_stopwords()
answers = file_reader.read_answers()

lexico = Lexico(stopwords)
translator = Translator(stopwords, answers)

finish = True
while(finish):
    query = input('>> ')
    table = lexico.analysis(query)
    translator.tfidf_calc(table)
    ans = translator.response(query)
    print('Chatbot: ', ans)
    finish = False