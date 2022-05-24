#!/bin/python3

from lexico import Lexico

lexico = Lexico()

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

for text in texts:
    print('-> ', text, '\n')
    lexico.analysis(text)
    print('_____'*11)
