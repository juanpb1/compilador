from lexico import Lexico

analise_lexica = []

teste = Lexico('teste.txt')
analise_lexica = teste.main()
for token in analise_lexica:
  print('--------------------------------------')
  if(token['classe'] == 'ERRO'):
    print(f'ERRO AO TENTAR RECONHECER O TOKEN "{token["token"]}"')
    break
  else:
    print(f'TOKEN: {token["token"]} | CLASSE: {token["classe"]}')

print('--------------------------------------')