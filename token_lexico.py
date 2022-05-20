from abc import ABC, abstractmethod

class TokenInterface(ABC):
    def __init__(self):
        self.__type: str
        self.__text: str

class Token(TokenInterface):
    def __init__(self, type, text):
        self.__type = type
        self.__text = text
        
    def toString(self):
        return "<type={}, text={}>".format(self.__type, self.__text)
