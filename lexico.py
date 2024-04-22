class Lexico:

  #  VERIFICAR O TOKEN DENTRO DO ESTADO, SE NÃO PERTENCE A SEQUENCIA, ELE VERIFICA SE O
  # ESTADO É FINAL E ELE EXIBE O TIPO DO TOKEN
  
  def __init__(self, arquivo_base):
    #Inicializa as variáveis de instância
    self.arquivo_base = arquivo_base
    self.token = ''
    self.estado_inicial = 'q0'
    self.estados_finais = ['q1', 'q3', 'q5', 'q8', 'q10', 'q11']
    self.estado_atual = self.estado_inicial
    self.current_index = 0
    self.numero_da_linha = 1
    self.simbolos_especiais = [
      ';', ',', '.', '+', '-', '*', '(', ')', '{',
      '}', '/', '@', '<=', '<>',':=', '>=', '+='
    ]
    # Reconhecer apenas os símbolos especiais um caractere
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

      if(caractere == '\n' or caractere == ' ' or 
         self.index_atual() + 1 >= self.lenArquivo):
        if(self.index_atual() + 1 >= self.lenArquivo):
          self.token += caractere
        self.classifica_token(self.estado_atual)
      else:
        self.token += caractere
        self.automato(caractere)
      
      # if not (caractere.isspace()):
      #   self.token += caractere
      #   self.automato(caractere)

      self.index_next()
      
  #Estados
  def qO(self, caractere):
    if caractere.isalpha():
      self.estado_atual = 'q1'
    else:
      self.classifica_token(self.estado_atual)
      
  def q1(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q1'
    elif caractere == '_':
      self.estado_atual = 'q2'
    elif caractere == '.':
      self.estado_atual = 'q4'
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
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q4(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q5'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

  def q5(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q5'
    else:
      self.reset_token()
      self.classifica_token(self.estado_atual)

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
      case _:
        return

  #Classifica o tipo do token
  def classifica_token(self, estado):
    if(estado in self.estados_finais):
      match estado:
        case 'q1' | 'q3' | 'q5':
          if(self.token.strip(' ') in self.palavras_reservadas):
            print(f'{self.token} => PALAVRA RESERVADA.')
          else:
            print(f'{self.token} => IDENTIFICADOR.')
        case 'q8', 'q10':
            print(f'{self.token} => DÍGITO.')
        case 'q11':
          print(f'{self.token} => SÍMBOLO ESPECIAL.')
        case _:
          print('ERRO LÉXICO.')
    else:
      if(self.token != '\n' and self.token != " "):
        print(f'{self.token} => NÃO RECONHECIDO no ESTADO {estado}.')

    self.token = ''
    self.estado_atual = self.estado_inicial
      
  def main(self):
    self.percorre_arquivo()