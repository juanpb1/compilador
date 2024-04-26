class Lexico:

  def __init__(self, arquivo_base):
    #Inicializa as variáveis de instância
    self.arquivo_base = arquivo_base
    self.token = ''
    self.estado_inicial = 'q0'
    self.estados_finais = ['q1', 'q3', 'q5', 'q6', 'q8', 'q10', 'q11', 'q17']
    self.estado_atual = self.estado_inicial
    self.current_index = 0
    self.numero_da_linha = 1
    self.simbolos_especiais = [
      ';', ',', '.', '+', '-', '*', '(', ')', '{','}', '/', '@', ]
    self.palavras_reservadas = [
      'if', 'then', 'else', 'while', 'do', 'until', 'repeat', 'int', 'double',
      'char', 'case', 'switch', 'end', 'procedure', 'function', 'for', 'begin'
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

  def reset_token(self):
    self.index_back()
    self.token = self.token[:-1]
  
  #Percorre o arquivo
  def percorre_arquivo(self):
    while(self.index_atual() < self.lenArquivo):
      caractere = self.arquivo[self.index_atual()]
      self.token += caractere
      self.automato(caractere)
      if(caractere == '\n' or 
         (caractere.isspace() and self.estado_atual != 'q15') or 
         self.index_atual() + 1 >= self.lenArquivo):
        self.classifica_token(self.estado_atual)
      
      self.index_next()
      
  #Estados
  def qO(self, caractere):
    if caractere.isalpha():
      self.estado_atual = 'q1'
    elif caractere == '-':
      self.estado_atual = 'q7'
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
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q2(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q3'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q3(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q3'
    elif caractere == '_':
      self.estado_atual = 'q2'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q4(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q5'
    elif caractere == '.':
      self.estado_atual = 'q4'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q5(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q5'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)
  
  def q6(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q6'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)
  
  def q7(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q8'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)
      
  def q8(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q8'
    elif caractere == ',':
      self.estado_atual = 'q9'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q9(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q10'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q10(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q10'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q11(self, caractere):
    if caractere != ' ' or caractere == '\n':
      self.reset_token()
      self.classifica_token(self.estado_atual)
    else:
      self.classifica_token(self.estado_atual)
  
  def q12(self, caractere):
    if(caractere in ['=', '>']):
      self.estado_atual = 'q11'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q13(self, caractere):
    if(caractere == '='):
      self.estado_atual = 'q11'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q14(self, caractere):
    if(caractere == '!'):
      self.estado_atual = 'q15'
    elif (caractere.isalpha() or caractere.isdigit() or caractere == ' '):
      self.estado_atual = 'q16'
    else: 
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q15(self, caractere):
    if caractere == '\n' or self.index_atual() + 2 >= self.lenArquivo:
      self.estado_atual = 'q17'
      self.reset_token()
      #self.classifica_token(self.estado_atual)
    else: 
      self.estado_atual = 'q15'

  def q16(self, caractere):
    
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
      case 'q11':
        self.q11(caractere)
        return
      case 'q12':
        self.q12(caractere)
      case 'q13':
        self.q13(caractere)
      case 'q14':
        self.q14(caractere)
      case 'q15':
        self.q15(caractere)
      case _:
        return

  #Classifica o tipo do token
  def classifica_token(self, estado):
    if(estado in self.estados_finais):
      match estado:
        case 'q1' | 'q3' | 'q5'| 'q6':
          if(self.token.strip(' ') in self.palavras_reservadas):
            print(f'{self.token} => PALAVRA RESERVADA.')
          else: 
            print(f'{self.token} => IDENTIFICADOR.')
        case 'q8' | 'q10':
          print(f'{self.token} => DÍGITO.')
        case 'q11':
          print(f'{self.token} => SÍMBOLO ESPECIAL.')
        case 'q17':
         print(f'{self.token} => COMENTÁRIO.')
        case _:
          print(f'ERRO LÉXICO {estado}.')
    else:
      if(self.token != '\n' and self.token and not self.token.isspace()):
        print(f'{self.token} => NÃO RECONHECIDO no ESTADO {estado}.')

    self.token = ''
    self.estado_atual = self.estado_inicial
      
  def main(self):
    self.percorre_arquivo()