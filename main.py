#!/bin/python3
from lexico import Lexico
from translator import Translator
from file_reader import File
import nltk
nltk.download('punkt')

file_reader = File()
stopwords = file_reader.read_stopwords()
answers, has_new_answers = file_reader.read_answers()

lexico = Lexico(stopwords)
translator = Translator(stopwords, answers, has_new_answers)

print('\nChatbot: Olá, como posso ajudar?')

while(True):
    query = input('\n>> ')

    if(query.lower() == 'tchau'):
        print('\nChatbot: Até logo!')
        break


    table = lexico.analysis(query)
    
    ans = translator.translate(table)
    print('\nChatbot: ', ans)

translator.save_inverted_index()
file_reader.save_size_answers()