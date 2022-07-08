#!/bin/python3
from lexico import Lexico
from translator import Translator
from file_reader import File

file_reader = File()
stopwords = file_reader.read_stopwords()
answers = file_reader.read_answers()

lexico = Lexico(stopwords)
translator = Translator(stopwords, answers)

while(True):
    query = input('>> ')

    if(query == 'TCHAU'):
        break

    table = lexico.analysis(query)
    ans = translator.translate(table)
    print('Chatbot: ', ans)

translator.save_inverted_index()