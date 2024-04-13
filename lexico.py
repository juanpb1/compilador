class Lexico:

  def __init__(self, arquivo_base):
    #Inicializa as variáveis de instância
    self.arquivo_base = arquivo_base
    self.lexico = ''
    self.estado_atual = 'q0'
    self.estado_inicial = 'q0'
    self.estados_finais = ['q1', 'q3', 'q5', 'q6', 'q8', 'q10',]
    self.current_index = 0
    self.numero_da_linha = 1
    self.simbolos_especiais = ['(', ')', '{', '}', ',', ';', ':',
                                '!', '=', '+', '-', '*', '@']
    self.palavras_reservadas = [
      'if', 'then', 'else', 'while', 'do', 'until', 'repeat', 'int', 'double',
      'char', 'case', 'switch', 'end', 'procedure', 'function', 'for', 'begin'
    ]
    self.possuiErroLexico = False

    #Ler o arquivo
    with open(self.arquivo_base, 'r') as file:
      self.arquivo = file.read()
    self.tamArquivo = len(self.arquivo)

  #Atualiza o index para buscar o proximo caractere
  def index_atual(self):
    return self.current_index

  def index_next(self):
    self.current_index += 1
  
  #Percorre o arquivo
  def obter_caractere(self):
    while(self.index_atual() < self.tamArquivo):
      caractere = self.arquivo[self.index_atual()]
      if(caractere == '\n' or caractere == ' ' or 
         self.index_atual() == self.tamArquivo -1):
        self.classifica_token(self.estado_atual)
        self.numero_da_linha += 1
        self.lexico = ''
        self.estado_atual = 'q0'
      else:
          self.lexico += caractere
          self.automato(caractere)
        
      self.index_next()
      
  #Estados
  def qO(self, caractere):
    if caractere.isalpha():
      self.estado_atual = 'q1'
    elif caractere == '-':
      self.estado_atual = 'q7'
    elif caractere.isdigit():
      self.estado_atual = 'q8'
    else:
      self.possuiErroLexico = True
      
  def q1(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q1'
    elif caractere == '_':
      self.estado_atual = 'q2'
    elif caractere == '.':
      self.estado_atual = 'q4'
    elif caractere.isalpha():
      self.estado_atual = 'q6'
    else :
      self.possuiErroLexico = True

  def q2(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q3'
      return
    else:
      self.possuiErroLexico = True

  def q3(self, caractere):
      if caractere.isalpha() or caractere.isdigit():
        self.estado_atual = 'q3'
      else:
        self.possuiErroLexico = True
  
  def q4(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q5'
    else:
      self.possuiErroLexico = True

  def q5(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q5'
    else:
      self.possuiErroLexico = True

  def q6(self, caractere):
    if caractere.isalpha():
      self.estado_atual = 'q6'
    else:
      self.possuiErroLexico = True

  def q7(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q8'
    else:
      self.possuiErroLexico = True

  def q8(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q8'
    elif caractere == '.':
      self.estado_atual = 'q9'
    else:
      self.possuiErroLexico = True

  def q9(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q10'
    else:
      self.possuiErroLexico = True

  def q10(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q10'
    else:
      self.possuiErroLexico = True 
      
  #Verifica o tipo de estado 
  def automato(self, caractere):
    match self.estado_atual:
      case 'q0':
        self.qO(caractere) 
        return
      case 'q1':
        self.q1(caractere)
        return
      case 'q2':
        self.q2(caractere)
        return
      case 'q3':
        self.q3(caractere)
        return
      case 'q4':
        self.q4(caractere)
        return
      case 'q5':
        self.q5(caractere)
        return
      case 'q6':
        self.q6(caractere)
        return
      case 'q7':
        self.q7(caractere)
        return
      case 'q8':
        self.q8(caractere)
        return
      case 'q9':
        self.q9(caractere)
        return
      case 'q10':
        self.q10(caractere)
        return
      case _:
        self.possuiErroLexico = True

  #Classifica o tipo do token
  def classifica_token(self, estado):
    if not self.possuiErroLexico and self.lexico != '':
      if estado in self.estados_finais:
        if self.lexico in self.palavras_reservadas:
          print(f'{self.lexico} => PALAVRA RESERVADA')
        elif estado in ['q8', 'q10']:
          print(f'{self.lexico} => DÍGITO')
        else:
          print(f'{self.lexico} => IDENTIFICADOR')
    else:
      if self.lexico != '':
        print(f'{self.lexico} => NÃO RECONHECIDO')
        self.possuiErroLexico = False
      
  def main(self):
    self.obter_caractere()