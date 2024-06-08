class Lexico:

  def __init__(self, arquivo_base):
    #Inicializa as variáveis de instância
    self.arquivo_base = arquivo_base
    self.token = ''
    self.erroLexico = False
    self.estado_inicial = 'q0'
    self.estados_finais = ['q1', 'q3', 'q5', 'q6', 'q8', 'q10', 'q11', 'q17',
                           'q22', 'q26']
    self.estado_atual = self.estado_inicial
    self.current_index = 0
    self.numero_da_linha = 1
    self.simbolos_especiais = [
      ';', ',', '.', '+', '-', '*', '(', ')', '{','}', '/', '@', ]
    self.palavras_reservadas = [
      'if', 'then', 'else', 'while', 'do', 'until', 'repeat', 'int', 'double',
      'char', 'case', 'switch', 'end', 'procedure', 'function', 'for', 'begin',
      'boolean', 'type', 'var'
    ]

    #Ler o arquivo
    with open(self.arquivo_base, 'r') as file:
      self.arquivo = file.read()
    self.lenArquivo = len(self.arquivo)
  
  #Atualiza o index para buscar o proximo caractere
  def index_atual(self):
    return self.current_index

  def index_next(self):
    self.current_index += 1

  def index_back(self):
    self.current_index -= 1

  def reset_token(self, caractere):
    if(caractere == '\n'):
      self.numero_da_linha -= 1
    self.index_back()
    self.token = self.token[:-1]

  def isComentario(self):
    return self.estado_atual not in {'q15', 'q16', 'q21', 'q24', 'q25'}

  def pula_linha(self, caractere):
    if(caractere == '\n'):
      self.numero_da_linha += 1
  
  #Percorre o arquivo
  def percorre_arquivo(self):
    while(self.index_atual() < self.lenArquivo):
      if(self.erroLexico):
        break
      caractere = self.arquivo[self.index_atual()]
      self.token += caractere
      self.automato(caractere)
      if((caractere == '\n' and self.isComentario()) or 
        (caractere.isspace() and self.isComentario()) or
        self.index_atual() + 1 >= self.lenArquivo):
        self.classifica_token(self.estado_atual)

      self.pula_linha(caractere)
      self.index_next()
      
  #Estados
  def q0(self, caractere):
    if caractere.isalpha():
      self.estado_atual = 'q1'
    # elif caractere == '-':
    #   self.estado_atual = 'q7'
    elif caractere.isdigit():
      self.estado_atual = 'q8'
    elif caractere == '<':
      self.estado_atual = 'q12'
    elif caractere in [':', '>', '+']:
      self.estado_atual = 'q13'
    elif caractere in self.simbolos_especiais:
      self.estado_atual = 'q11'
    elif caractere == '!':
      self.estado_atual = 'q14'
    elif caractere == '/':
      self.estado_atual = 'q23'
    else:
      self.classifica_token(self.estado_atual)
      
  def q1(self, caractere):
    if caractere == '_':
      self.estado_atual = 'q2'
    elif caractere == '.':
      self.estado_atual = 'q4'
    elif caractere.isalpha():
      self.estado_atual = 'q6'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q2(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q3'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q3(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q3'
    elif caractere == '_':
      self.estado_atual = 'q2'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q4(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q5'
    elif caractere == '.':
      self.estado_atual = 'q4'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q5(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q5'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)
  
  def q6(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q6'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)
  
  def q7(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q8'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)
      
  def q8(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q8'
    elif caractere == '.':
      self.estado_atual = 'q9'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q9(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q10'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q10(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q10'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q11(self, caractere):
    if caractere == '@':
      self.estado_atual = 'q20'
    elif caractere == '/':
      self.estado_atual = 'q24'
    elif self.token[0] == '-' and caractere.isdigit():
      self.estado_atual = 'q8'
    elif caractere != ' ' or caractere == '\n':
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)
    else:
      self.classifica_token(self.estado_atual)
  
  def q12(self, caractere):
    if(caractere in ['=', '>']):
      self.estado_atual = 'q11'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q13(self, caractere):
    if(caractere == '='):
      self.estado_atual = 'q11'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q14(self, caractere):
    if(caractere == '!'):
      self.estado_atual = 'q15'
    elif (caractere.isalpha() or caractere.isdigit() or 
          caractere == ' ' or caractere == '\n'):
      self.estado_atual = 'q16'
    else: 
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q15(self, caractere):
    if caractere == '\n' or self.index_atual() + 2 >= self.lenArquivo:
      self.estado_atual = 'q17'
      self.reset_token(caractere)
      #self.classifica_token(self.estado_atual)
    else: 
      self.estado_atual = 'q15'

  def q16(self, caractere):
    if(caractere == '!'):
      self.estado_atual = 'q17'
      self.reset_token(caractere)
    else:
      self.estado_atual = 'q16'

  def q19(self, caractere):
    if(caractere.isalpha() or caractere.isdigit() or caractere == ' '):
      self.estado_atual = 'q20'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q20(self, caractere):
    if(caractere.isalpha() or caractere.isdigit() or caractere == ' '):
      self.estado_atual = 'q21'
    else:
      self.reset_token(caractere)
      self.classifica_token(self.estado_atual)

  def q21(self, caractere):
    if caractere == '\n' or self.index_atual() + 2 >= self.lenArquivo:
      self.estado_atual = 'q22'
      self.reset_token(caractere)
      #self.classifica_token(self.estado_atual)
    else: 
      self.estado_atual = 'q21'

  def q24(self, caractere):
    if(caractere == '/'):
      self.estado_atual = 'q25'
    else:
      self.estado_atual = 'q24'

  def q25(self, caractere):
    if(caractere == '/'):
      self.estado_atual = 'q26'
      self.reset_token(caractere)
    else:
      self.estado_atual = 'q24'
  
  #Verifica o tipo de estado 
  def automato(self, caractere):
    state_actions = {
      'q0': self.q0,
      'q1': self.q1,
      'q2': self.q2,
      'q3': self.q3,
      'q4': self.q4,
      'q5': self.q5,
      'q6': self.q6,
      'q7': self.q7,
      'q8': self.q8,
      'q9': self.q9,
      'q10': self.q10,
      'q11': self.q11,
      'q12': self.q12,
      'q13': self.q13,
      'q14': self.q14,
      'q15': self.q15,
      'q16': self.q16,
      'q19': self.q19,
      'q20': self.q20,
      'q21': self.q21,
      'q24': self.q24,
      'q25': self.q25,
    }

    action = state_actions.get(self.estado_atual)
    if action:
        action(caractere)

  def erro(self):
    raise Exception(f"'{self.token}' não reconhecido")
  
  #Classifica o tipo do token
  def classifica_token(self, estado):
    if(estado in self.estados_finais):
      match estado:
        case 'q1' | 'q3' | 'q5'| 'q6':
          if(self.token.strip(' ') in self.palavras_reservadas):
            print(f'Token: {self.token} => Tipo: PALAVRA RESERVADA\n')
          else:
            print(f'Token: {self.token} => Tipo: IDENTIFICADOR\n')
        case 'q8' | 'q10':
            print(f'Token: {self.token} => Tipo: DÍGITO\n')
        case 'q11':
          print(f'Token: {self.token} => Tipo: SÍMBOLO ESPECIAL\n')
        case 'q17' | 'q22' | 'q26':
          print(f'Token: {self.token} => Tipo: COMENTÁRIO\n')
        case _:
          print(f'ERRO AO TENTAR RECONHECER O Token: {self.token}\n')
    else:
      if(self.token != '\n' and self.token and not self.token.isspace()):
        
        print("\nERRO LÉXICO")
        print(f"Token '{self.token}' não reconhecido!")
        self.erroLexico = True

    self.token = ''
    self.estado_atual = self.estado_inicial
  
  def main(self):
    self.percorre_arquivo()