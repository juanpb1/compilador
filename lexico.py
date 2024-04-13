class Lexico:

  def __init__(self, arquivo_base):
    #Inicializa as variáveis de instância
    self.arquivo_base = arquivo_base
    self.lexico = ''
    self.estado_atual = 'q0'
    self.estado_inicial = 'q0'
    self.estados_finais = ['q1', 'q3', 'q5', 'q6', 'q9', 'q11', 'q7',]
    self.current_index = 0
    self.numero_da_linha = 1
    self.simbolos_especiais = ['(', ')', '{', '}', ',', ';', ':',
                                '!', '=', '+', '-', '*', '@']
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
      else:
          self.lexico += caractere
          self.automato(caractere)
      self.index_next()
      
  #Estados
  def qO(self, caractere):
    if caractere.isalpha():
      self.estado_atual = 'q1'
      self.q1(caractere)
    else:
      self.possuiErroLexico = True
      

  def q1(self, caractere):
    if caractere.isalpha() or caractere.isdigit():
      self.estado_atual = 'q1'
    elif '_':
      self.estado_atual = 'q2'
    else :
      self.possuiErroLexico = True

  def q2(self, caractere):
    if caractere.isalpha():
      self.estado_atual = 'q2'
      return
    else:
      self.possuiErroLexico = True

  def q3(self, caractere):
      if caractere.isalpha() or caractere.isdigit():
        self.estado_atual = 'q2'
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
      case _:
        self.possuiErroLexico = True

  def classifica_token(self, estado):
    if not self.possuiErroLexico and self.lexico != '':
      if estado in self.estados_finais:
        print(f'{self.lexico} => IDENTIFICADOR')
    else:
      if self.lexico != '':
        print(f'{self.lexico} => NÃO RECONHECIDO')
      #self.possuiErroLexico = False
      
  def main(self):
    self.obter_caractere()