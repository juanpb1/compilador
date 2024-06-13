class Lexico:

  def __init__(self, arquivo_base):
    #Inicializa as variáveis de instância
    self.arquivo_base = arquivo_base
    self.caractere = ''
    self.token = ''
    self.erroLexico = False
    self.estado_inicial = 'q0'
    self.estados_finais = ['q1', 'q3', 'q5', 'q6', 'q8', 'q10', 'q11', 'q17',
                           'q22', 'q26']
    self.estado_atual = self.estado_inicial
    self.current_index = 0
    self.numero_da_linha = 1
    self.simbolos_especiais = [
      ';', ',', '.', '+', '-', '*', '(', ')', '{','}', '/', '@',]
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

  def pula_linha(self, caractere):
    if(caractere == '\n'):
      self.numero_da_linha += 1

  #Percorre o arquivo
  def percorre_arquivo(self):
    while True:
      if self.erroLexico:
        break

      self.caractere = self.arquivo[self.index_atual()]
      self.token += self.caractere
      resultado = self.automato(self.caractere)

      if resultado:
        token, tipo = resultado
        yield token, tipo

      self.index_next()
      
      if self.index_atual() >= self.lenArquivo:
        break

    if self.token:
      resultado = self.classifica_token(self.estado_atual)
      if resultado:
        token, tipo = resultado
        yield token, tipo
  
  #Estados
  def q0(self, caractere):
    if caractere.isalpha():
      self.estado_atual = 'q1'
    elif caractere.isdigit():
      self.estado_atual = 'q8'
    elif caractere == '<':
      self.estado_atual = 'q12'
    elif caractere in [':', '>', '+']:
      self.estado_atual = 'q13'
    elif caractere == '!':
      self.estado_atual = 'q14'
    elif caractere == '/':
      self.estado_atual = 'q23'
    elif caractere in self.simbolos_especiais:
      self.estado_atual = 'q11'
    else:
      return self.classifica_token(self.estado_atual)
    return None
  
  def q1(self, caractere):
    if caractere == '_':
      self.estado_atual = 'q2'
    elif caractere == '.':
      self.estado_atual = 'q4'
    elif caractere.isalpha():
      self.estado_atual = 'q6'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
      
  def q2(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q3'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
      
  def q3(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q3'
    elif caractere == '_':
      self.estado_atual = 'q2'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
      
  def q4(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q5'
    elif caractere == '.':
      self.estado_atual = 'q4'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
      
  def q5(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q5'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
  
  def q6(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q6'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
  
  def q7(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q8'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
      
  def q8(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q8'
    elif caractere == '.':
      self.estado_atual = 'q9'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
      

  def q9(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q10'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
      
  def q10(self, caractere):
    if caractere.isdigit():
      self.estado_atual = 'q10'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
      
  def q11(self, caractere):
    if caractere == '@':
      self.estado_atual = 'q20'
    elif caractere == '/':
      self.estado_atual = 'q24'
    elif self.token[0] == '-' and caractere.isdigit():
      self.estado_atual = 'q8'
    elif caractere.isspace() or caractere == '\n':
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
      
  def q12(self, caractere):
    if(caractere in ['=', '>']):
      self.estado_atual = 'q11'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None

  def q13(self, caractere):
    if(caractere == '='):
      self.estado_atual = 'q11'
    else:
      self.reset_token(caractere)
      self.estado_atual = 'q11'
      return self.classifica_token(self.estado_atual)
    return None

  def q14(self, caractere):
    if(caractere == '!'):
      self.estado_atual = 'q15'
    elif (caractere.isalpha() or caractere.isdigit() or 
          caractere == ' ' or caractere == '\n'):
      self.estado_atual = 'q16'
    else: 
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None

  def q15(self, caractere):
    if caractere == '\n' or self.index_atual() + 2 >= self.lenArquivo:
      self.estado_atual = 'q17'
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    else: 
      self.estado_atual = 'q15'
    return None

  def q16(self, caractere):
    if(caractere == '!'):
      self.estado_atual = 'q17'
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    else:
      self.estado_atual = 'q16'
    return None

  def q19(self, caractere):
    if(caractere.isalpha() or caractere.isdigit() or caractere == ' '):
      self.estado_atual = 'q20'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None

  def q20(self, caractere):
    if(caractere.isalpha() or caractere.isdigit() or caractere == ' '):
      self.estado_atual = 'q21'
    else:
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    return None
    
  def q21(self, caractere):
    if caractere == '\n' or self.index_atual() + 2 >= self.lenArquivo:
      self.estado_atual = 'q22'
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    else: 
      self.estado_atual = 'q21'
    return None

  def q24(self, caractere):
    if(caractere == '/'):
      self.estado_atual = 'q25'
    else:
      self.estado_atual = 'q24'

  def q25(self, caractere):
    if(caractere == '/'):
      self.estado_atual = 'q26'
      self.reset_token(caractere)
      return self.classifica_token(self.estado_atual)
    else:
      self.estado_atual = 'q24'
    return None
  
  #Verifica o tipo de estado 
  def automato(self, caractere):
    match self.estado_atual:
      case 'q0':
        return self.q0(caractere) 
      case 'q1':
        return self.q1(caractere) 
      case 'q2':
        return self.q2(caractere)   
      case 'q3':
        return self.q3(caractere) 
      case 'q4':
        return self.q4(caractere) 
      case 'q5':
        return self.q5(caractere) 
      case 'q6':
        return self.q6(caractere) 
      case 'q7':
        return self.q7(caractere) 
      case 'q8':
        return self.q8(caractere) 
      case 'q9':
        return self.q9(caractere) 
      case 'q10':
        return self.q10(caractere) 
      case 'q11':
        return self.q11(caractere) 
      case 'q12':
        return self.q12(caractere) 
      case 'q13':
        return self.q13(caractere) 
      case 'q14':
        return self.q14(caractere) 
      case 'q15':
        return self.q15(caractere)   
      case 'q16':
        return self.q16(caractere)     
      case 'q19':
        return self.q19(caractere) 
      case 'q20':
        return self.q20(caractere) 
      case 'q21':
        return self.q21(caractere) 
      case 'q24':
        self.q24(caractere) 
      case 'q25':
        return self.q25(caractere) 
      case _:
        return

  def erro(self):
    raise Exception(f"'{self.token}' não reconhecido")
  
  #Classifica o tipo do token
  def classifica_token(self, estado):
    token = self.token
    tipo = ''
    if(estado in self.estados_finais):
      match estado:
        case 'q1' | 'q3' | 'q5'| 'q6':
          if(self.token.strip() in self.palavras_reservadas):
            tipo = 'palavra_reservada'
          else:
            tipo = 'identificador'
        case 'q8' | 'q10':
          tipo = 'dígito'
        case 'q11':
          tipo = 'símbolo_especial'
        case 'q17' | 'q22' | 'q26':
          tipo = 'comentario'
        case _:
          print(f'ERRO AO TENTAR RECONHECER O Token: {self.token}\n')
    else:
      if(self.token != '\n' and self.token and not self.token.isspace()):
        print("\nERRO LÉXICO")
        print(f"Token '{self.token}' não reconhecido!")
        self.erroLexico = True
        
    self.token = ''
    self.estado_atual = self.estado_inicial
    return token, tipo
  
  def obter_proximo_token(self):
    for token, tipo in self.percorre_arquivo():
      if((token != '' and tipo != '' and tipo != 'comentario')):
        yield token, tipo
    #self.percorre_arquivo()