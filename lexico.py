from typing import List
import re
import sys
from token_lexico import Token
from nltk.stem.snowball import SnowballStemmer

TK_PERGUNTA = 'pergunta'
TK_ACAO = 'acao'
TK_AFIRMACAO = 'afirmacao'
TK_ADJETIVO = 'adjetivo'
TK_DEFEITO = 'defeito'
TK_FABRICANTE = 'fabricante'
TK_DISPOSITIVO = 'dispositivo'

class Lexico:
    def __init__(self):
        self.__pergunta = ('qual', 'quais', 'quanto', 'quantos', 'quantas', 'como', 'quando')
        self.__acao = ('ligar', 'reiniciar', 'desligar', 'jogar', 'atualizar', 'comprar', 'comprei', 'atualizei', 'liguei', 'desliguei', 'reiniciei', 'configurar', 'instalar', 'configurei', 'formatar', 'formatei', 'ligou', 'reiniciou')
        self.__afirmacao = ('sim', 'não')
        self.__defeito = ('quebrado','lento','devagar','quente','vírus','travou','travado','parou','parado','barulho','ruído','congelou','não liga','não quer ligar','não ligou')
        self.__adjetivo = (self.__defeito, 'rápido','potente','barato','caro','novo','melhor')
        self.__fabricante = ('apple','dell','samsung','lenovo','multilaser','logitech','acer','positivo','asus')
        self.__dispositivo = ('teclado','mouse','monitor','tela','notebook','computador','tablet','headset','headphone','fone de ouvido','drivers','impressora', 'PC', 'CPU', 'processador')

        try:
            file = open('stopwords.txt', 'r', encoding="utf8")
            self.__stopwords = [line[:-1] for line in file]
        except FileNotFoundError as err:
            print(err)
            sys.exit()
        pass

    def analysis(self, text: str):
        text = text.lower()
        text = self.__scanning(text) #Escaneia a-zA-Z0-9 e pontuações
        text = self.__remove_stopwords(text) #Remove palavras que estão na stopwords

        self.__lexeme_lists()

        tokenfy = []
        for word in text:
            if(word in self.__pergunta):
                tokenfy.append(Token(TK_PERGUNTA, word).toString())

            if(self.__lexeme(word) in self.__acao):
                tokenfy.append(Token(TK_ACAO, word).toString())

            if(word in self.__defeito):
                tokenfy.append(Token(TK_DEFEITO, word).toString())

            if(word in self.__adjetivo):
                tokenfy.append(Token(TK_ADJETIVO, word).toString())

            if(word in self.__fabricante):
                tokenfy.append(Token(TK_FABRICANTE, word).toString())

            if(word in self.__dispositivo):
                tokenfy.append(Token(TK_DISPOSITIVO, word).toString())

            if(word in self.__afirmacao):
                tokenfy.append(Token(TK_AFIRMACAO, word).toString())

        print(tokenfy)

    def __scanning(self, text: str):
        text = re.sub('[^a-záàâãéèêíóôõúçA-Z0-9 \n]', '', text)
        new_text = text.split(' ')
        return new_text

    def __remove_stopwords(self, text: List[str]):
        temp_text = text
        for word in temp_text:
            if(word in self.__stopwords):
                text = list(filter((word).__ne__, text))
        return text

    def __lexeme(self, word: str):
        snow_stemmer = SnowballStemmer(language='portuguese')
        return snow_stemmer.stem(word)

    def __lexeme_lists(self):
        temp = []
        for word in self.__acao:
            temp.append(self.__lexeme(word))
        self.__acao = temp

        # temp = []
        # for word in self.__adjetivo:
        #     temp.append(self.__lexeme(word))
        # self.__adjetivo = temp
