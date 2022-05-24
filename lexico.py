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
        self.__acao = ('ligar', 'reiniciar', 'desligar', 'jogar', 'atualizar', 'comprar', 'configurar', 'instalar', 'formatar','limpar', 'usar', 'imprimir')
        self.__negacao = ('nunca', 'não', 'sem')
        self.__afirmacao = ('sim', self.__negacao)
        self.__defeito = ('quebrado','lento','devagar','quente','vírus','travado','parado','barulho','ruído','congelou')
        self.__adjetivo = (self.__defeito, 'rápido','potente','barato','caro','novo','melhor')
        self.__fabricante = ('apple','dell','samsung','lenovo','multilaser','logitech','acer','positivo','asus')
        self.__dispositivo = ('teclado','mouse','monitor','tela','notebook','computador','tablet','headset','headphone', 'fone de ouvido','drivers','impressora')

        try:
            # https://github.com/stopwords-iso/stopwords-pt/blob/master/stopwords-pt.txt
            file = open('stopwords.txt', 'r', encoding="utf8")
            self.__stopwords = [line[:-1] for line in file]
        except FileNotFoundError as err:
            print(err)
            sys.exit()
        pass

    def analysis(self, text: str):
        text = text.lower() #Passar o texto para minúsculo
        text = self.__scanning(text) #Escaneia a-zA-Z0-9 e pontuações
        text = self.__remove_stopwords(text) #Remove palavras que estão na stopwords

        table: List[Token] = self.__create_symbol_table(text) #Cria tabela de símbolos passando texto sem stopwords

        self.print_symbol_table(table)

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
        # https://www.nltk.org/_modules/nltk/stem/snowball.html
        snow_stemmer = SnowballStemmer(language='portuguese')
        return snow_stemmer.stem(word)

    def __lexeme_list(self, list):
        temp = []
        for word in list:
            if(type(word) is str):
                temp.append(self.__lexeme(word))
        return temp

    def __create_symbol_table(self, text: List[str]):
        table: List[Token] = []
        
        for word in text:
            if(not self.__is_key_word(word)):
                if(self.__lexeme(word) in self.__lexeme_list(self.__acao)):
                    if(word not in table):
                        table.append(Token(TK_ACAO, word))

                elif (self.__lexeme(word) in self.__lexeme_list(self.__defeito)):
                    if(word not in table):
                        table.append(Token(TK_DEFEITO, word))  

                elif(word in self.__fabricante):
                    if(word not in table):
                        table.append(Token(TK_FABRICANTE, word))  

                elif(word in self.__dispositivo):
                    if(word not in table):
                        table.append(Token(TK_DISPOSITIVO, word))
                        
                elif(any(self.__lexeme(word) in sublist for sublist in self.__lexeme_list(self.__adjetivo))):
                    if(word not in table):
                        table.append(Token(TK_ADJETIVO, word))  

                elif(any(word in sublist for sublist in self.__afirmacao)):
                    if(word not in table):
                        table.append(Token(TK_AFIRMACAO, word))  

        return table

    def __is_key_word(self, word: str):
        if(word in self.__pergunta):
            return True

        return False

    def print_symbol_table(self, table: List[Token]):
        print('_'*5,'TABELA DE SÍMBOLOS', '_'*5)
        for token in table:
            print(token.toString())
        print('')