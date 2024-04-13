class Lexico:

  def __init__(self, arquivo_base):
    #Inicializa as variáveis de instância
    self.arquivo_base = arquivo_base
    self.numero_da_linha = 1
    self.fim_da_linha = '\n'
    self.simbolos_especiais = ['(', ')', '{', '}', ',', ';', ':',
                               '!', '=', '+', '-', '*', '@']

    #Ler o arquivo
    #with open(self.arquivo_base, 'r') as file:
    #self.arquivo = file.read()
    self.arquivo = open(self.arquivo_base, 'r')
  
  def qO(self, caractere):
    match caractere:
      case caractere.isalpha():
        self.q1(caractere)
      case _ :
        return f'Erro léxico na linha {self.numero_da_linha}.'

  def q1(self, caractere):
    match caractere:
      case caractere.isalpha():
        self.q1(caractere)
      case caractere.isdigit():
        self.q1(caractere)
      case '_':
        self.q2(caractere)
      case _:
        return f'Erro léxico na linha {self.numero_da_linha}.'

  def q2(self, caractere):
    match caractere:
      case '_':
        s