from lexico import Lexico
from sintatico import Sintatico

# lexico = Lexico('teste.txt')
# for token, tipo in lexico.obter_proximo_token():
#   if token != '' and tipo != '':
#     print(f'{token} - {tipo}')
#   #pass

sintatico = Sintatico()
sintatico.analisar()