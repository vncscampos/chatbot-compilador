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
        self.__pergunta = ('qual', 'quais', 'quanto', 'como', 'quando')
        self.__acao = ('ligar', 'reiniciar', 'desligar', 'jogar', 'atualizar', 'comprar', 'configurar', 'instalar', 'formatar','limpar', 'usar')
        self.__afirmacao = ('sim', 'não')
        self.__defeito = ('quebrado','lento','devagar','quente','vírus','travado','parado','barulho','ruído','congelado')
        self.__adjetivo = (self.__defeito, 'rápido','potente','barato','caro','novo','melhor')
        self.__fabricante = ('apple','dell','samsung','lenovo','multilaser','logitech','acer','positivo','asus')
        self.__dispositivo = ('teclado','mouse','monitor','tela','notebook','computador','tablet','headset','headphone','drivers','impressora', 'PC', 'CPU', 'processador')

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

        self.print_token_list(text)
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
            if(self.__is_key_word(word) == False):
                if(self.__lexeme(word) in self.__lexeme_list(self.__pergunta)):
                    table.append(Token(TK_PERGUNTA, word))

                if(self.__lexeme(word) in self.__lexeme_list(self.__acao)):
                    table.append(Token(TK_ACAO, word))

                if(self.__lexeme(word) in self.__lexeme_list(self.__defeito)):
                    table.append(Token(TK_DEFEITO, word))

                if(self.__lexeme(word) in self.__lexeme_list(self.__adjetivo)):
                    table.append(Token(TK_ADJETIVO, word))

        return table

    def __is_key_word(self, word: str):
        if(word in self.__pergunta):
            return True

        if(word in self.__acao):
            return True

        if(word in self.__defeito):
            return True

        if(word in self.__adjetivo):
            return True

        if(word in self.__fabricante):
            return True

        if(word in self.__dispositivo):
            return True

        if(word in self.__afirmacao):
            return True
        
        return False

    def print_symbol_table(self, table: List[Token]):
        print('_'*5,'TABELA DE SÍMBOLOS', '_'*5)
        for token in table:
            print(token.toString())
        print('\n')

    def print_token_list(self, text: List[str]):
        list_token = []
        print('_'*5, 'LISTA DE TOKENS', '_'*5)
        for word in text:
            if(self.__lexeme(word) in self.__lexeme_list(self.__pergunta)):
                list_token.append(Token(TK_PERGUNTA, word).toString())

            if(self.__lexeme(word) in self.__lexeme_list(self.__acao)):
                list_token.append(Token(TK_ACAO, word).toString())

            if(self.__lexeme(word) in self.__lexeme_list(self.__defeito)):
                list_token.append(Token(TK_DEFEITO, word).toString())

            if(self.__lexeme(word) in self.__lexeme_list(self.__adjetivo)):
                list_token.append(Token(TK_ADJETIVO, word).toString())

            if(word in self.__fabricante):
                list_token.append(Token(TK_FABRICANTE, word).toString())

            if(word in self.__dispositivo):
                list_token.append(Token(TK_DISPOSITIVO, word).toString())

            if(word in self.__afirmacao):
                list_token.append(Token(TK_AFIRMACAO, word).toString())

        print(list_token, '\n')