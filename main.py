from lexico import Lexico
from tabulate import tabulate

analise_lexica = []
tabelas_tokens = []

teste = Lexico('teste.txt')
analise_lexica = teste.main()

for token in analise_lexica:
  if(token['classe'] == 'ERRO'):
    tabelas_tokens.append(
      [
        token['token'], '-' * len(token['token']), 
        'ERRO LÉXICO', f" LINHA {token['linha']}"
      ]
    )
    break
  else:
    tabelas_tokens.append(
      [
        token['token'], '-' * len(token['token']), 
        token['classe'], '-' * len(token['classe'])
      ]
    )

print(tabulate(tabelas_tokens, headers=["TOKEN", "", "CLASSE", ""], tablefmt="grid"))