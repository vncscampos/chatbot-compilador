#!/bin/python3

from lexico import Lexico
from translator import Translator
import sys

import nltk
nltk.download('punkt')

stopwords = []
try:
    # https://github.com/stopwords-iso/stopwords-pt/blob/master/stopwords-pt.txt
    file = open('stopwords.txt', 'r', encoding='utf8')
    stopwords = [line[:-1] for line in file]
except FileNotFoundError as err:
    sys.exit()

lexico = Lexico(stopwords)
translator = Translator(stopwords)

texts = (
'Como faço para reiniciar o notebook da Apple?',
'Qual melhor computador para jogar?',
'Como faço para atualizar os drivers do computador?',
'Meu notebook está fazendo barulho.',
'Notebook da lenovo está devagar.',
'O computador estava quente e desligou.',
'Formatei o computador mas ele não liga.',
'Meu computador é potente mas está travando muito.',
'Sim, meu computador é novo',
)


finish = True
while(finish):
    query = input('>> ')
    lexico.analysis(query)
    # ans = translator.translate(table)
    # print('\nChatbot: ',ans)
    # finish = False
    