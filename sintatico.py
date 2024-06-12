from lexico import Lexico

class Sintatico:
  def __init__(self):
    self.lexico = Lexico('teste.txt')
    self.tokens = self.lexico.obter_proximo_token()
    self.token = ''
    self.classe = ''

  
  def erro(self, erro):
    raise SyntaxError(f'{erro}')

  
  def obter_proximo_token(self):
    try:
      token, classe = next(self.tokens)
      self.token = token
      self.classe = classe
      print(f'{token} - {classe}')
    except StopIteration:
      pass

  
  # PROGRAMAS E BLOCOS
  def analisar(self):
    
    self.obter_proximo_token()
    if(self.token.strip() != 'principal'):
      self.erro('Principal esperado!')

    self.obter_proximo_token()
    if(self.classe != 'identificador'):    
      self.erro('Identificador esperado!')

    self.obter_proximo_token()
    if(self.token.strip() != ';'):
      self.erro("';' esperado!")

    self.obter_proximo_token()
    self.bloco()

  
  def bloco(self):

    if(self.token.strip() == 'type'):
      self.declara_tipo()
      
    if(self.token.strip() == 'var'):
      self.declara_var()

    if(self.token == 'procedure' or self.token == 'function'):
      self.definica_sub_rotinas()

    self.comando_composto()

  
  # DECLARAÇÕES
  def declara_tipo(self):

    self.obter_proximo_token()

    while(self.classe == 'identificador'):

      if(self.classe != 'identificador'):
        self.erro('identificador esperado!')
      
      self.obter_proximo_token()
      if(self.token.strip() != '='):
        self.erro('= esperado!')

      self.tipo()
      self.obter_proximo_token()
      if(self.token.strip() != ';'):
        self.erro('; esperado!')

      self.obter_proximo_token()

  
  def declara_var(self):
    
    self.obter_proximo_token()
    self.lista_de_identificadores()
    
    if self.token.strip() != ":":
      self.erro("':' esperado")
      
    self.obter_proximo_token()
    self.tipo()
    
    self.obter_proximo_token()
    while self.token.strip() == ";":
      self.obter_proximo_token()
      self.lista_de_identificadores()
      if self.token.strip() != ":":
        self.erro("':' esperado")
        
      self.obter_proximo_token()
      self.tipo()
      
      self.obter_proximo_token()

  
  def definica_sub_rotinas(self):
    
    while self.token.strip() in ["procedure", "function"]:
      if self.token.strip() == "procedure":
          self.declara_procedimento()
      elif self.token == "function":
         self.declara_funcao()

  
  def declara_procedimento(self):
    
    if self.token.strip() == "procedure":
      self.obter_proximo_token()
      if self.classe != "identificador":
        self.erro("Identificador esperado")
          
      self.obter_proximo_token()
      if self.token.strip() == "(":
        self.parametros_formais()
        
      if self.token.strip() != ";":
        self.erro("';' esperado")
        
      self.obter_proximo_token()
      self.bloco()


  def declara_funcao(self):
    
    if self.token.strip() == "function":
      self.obter_proximo_token()
      if self.token.strip() != "identificador":
        self.erro("Identificador esperado")
        
      self.obter_proximo_token()
      if self.token.strip() == "(":
        self.parametros_formais()
        
      if self.token.strip() != ":":
        self.erro("':' esperado")
        
      self.obter_proximo_token()
      if self.classe != "identificador":
        self.erro("Identificador esperado")
        
      self.obter_proximo_token()
      if self.token.strip() != ";":
        self.erro("';' esperado")
        
      self.obter_proximo_token()
      self.bloco()

  
  def parametros_formais(self):
    if self.token.strip() == "(":
      self.obter_proximo_token()
      self.lista_de_identificadores()
      
      if self.token.strip() != ":":
          self.erro("':' esperado")
        
      self.obter_proximo_token()
      if self.classe != "identificador":
          self.erro("Identificador esperado")
        
      self.obter_proximo_token()
      while self.token.strip() == ";":
        self.obter_proximo_token()
        self.lista_de_identificadores()
      
        if self.token.strip() != ":":
            self.erro("':' esperado")
          
        self.obter_proximo_token()
        if self.classe != "identificador":
            self.erro("Identificador esperado")
        self.obter_proximo_token()
        
      if self.token.strip() != ")":
          self.erro("')' esperado")
        
      self.obter_proximo_token()

  
  def lista_de_identificadores(self):
    
    if self.classe != "identificador":
      self.erro("Identificador esperado")
    self.obter_proximo_token()
    
    while self.token == ",":
      self.obter_proximo_token()
      if self.classe != "identificador":
          self.erro("Identificador esperado")
      self.obter_proximo_token()

  
  def tipo(self):
    
    self.obter_proximo_token()
    if not ((self.classe == 'palavra_reservada') and (self.token.strip() == 'int') or (self.token.strip() == 'boolean') or (self.token.strip() == 'double') or (self.token.strip() == 'char')):
      self.erro("'tipo' esperado!")


  # COMANDOS
  def comando_composto(self):

    if(self.token.strip() != 'begin'):
      self.erro('begin esperado!')
    
    self.obter_proximo_token()
    self.comando_sem_rotulo()
    
    if self.token.strip() != ";":
      self.erro("';' esperado")
      
    while self.token.strip() == ";":
      self.obter_proximo_token()
      self.comando_sem_rotulo()
      self.obter_proximo_token()
    
    if(self.token.strip() != 'end'):
      self.erro('end esperado!')


  def comando_sem_rotulo(self):
    print(self.token)
    if self.classe == "identificador":
      self.obter_proximo_token()
      if self.token.strip() == ":=":
        self.atribuicao()
      elif self.token.strip() == "(":
        self.chamada_de_procedimento()
      else:
        self.erro("':=' ou '(' esperado")
    elif self.token.strip() == "if":
      self.comando_condicional()
    elif self.token.strip() == "while":
      self.comando_repetitivo()
    else:
      self.erro("Comando sem rótulo esperado")

  
  def atribuicao(self):

    self.obter_proximo_token()
    self.expressao()

  def chamada_de_procedimento(self):
    if self.classe != "identificador":
      self.erro("Identificador esperado")
      
    self.obter_proximo_token()
    if self.token.strip() == "(":
      self.obter_proximo_token()
      self.lista_de_expressoes()
      
      if self.token.strip() != ")":
        self.erro("')' esperado")
      self.obter_proximo_token()


  def comando_condicional(self):
    if self.token.strip() == "if":
      self.obter_proximo_token()
      self.expressao()
      
      if self.token.strip() != "then":
        self.erro("'then' esperado")
        
      self.obter_proximo_token()
      self.comando_sem_rotulo()
      
      if self.token.strip() == "else":
        self.obter_proximo_token()
        self.comando_sem_rotulo()


  def comando_repetitivo(self):
    if self.token.strip() == "while":
      self.obter_proximo_token()
      self.expressao()
      if self.token.strip()  != "do":
          self.erro("'do' esperado")
        
      self.obter_proximo_token()
      self.comando_sem_rotulo()

  
  #EXPRESSÕES
  def lista_de_expressoes(self):
    self.expressao()
    
    while self.token.strip() == ",":
      self.obter_proximo_token()
      self.expressao()

  
  def expressao(self):
    self.expressao_simples()
    if self.token.strip() in ["=", "<>", "<", "<=", ">", ">="]:
      self.relacao()
      self.expressao_simples()

  
  def relacao(self):
    if self.token.strip() in ["=", "<>", "<", "<=", ">", ">="]:
      self.obter_proximo_token()
    else:
        self.erro("Operador de relação esperado")

  
  def expressao_simples(self):
    if self.token.strip() in ["+", "-"]:
      self.obter_proximo_token()
      
    self.termo()
    
    while self.token.strip()  in ["+", "-", "or"]:
      self.operador1()
      self.termo()


  def termo(self):
    self.fator()
    while self.token.strip() in ["*", "div", "and"]:
      self.operador2()
      self.fator()


  def operador1(self):
    if self.token.strip() in ["+", "-", "or"]:
      self.obter_proximo_token()
    else:
      self.erro("Operador '+' ou '-' ou 'or' esperado")


  def operador2(self):
    if self.token.strip() in ["*", "div", "and"]:
      self.obter_proximo_token()
    else:
      self.erro("Operador '*' ou 'div' ou 'and' esperado")

  
  def fator(self):
    if self.classe == "identificador":
      self.obter_proximo_token()
      if self.token == "(":
        self.chamada_de_funcao()
    elif self.classe == "dígito":
      self.obter_proximo_token()
    elif self.token == "(":
      self.obter_proximo_token()
      self.expressao()
      if self.token.strip() != ")":
        self.erro("')' esperado")
      self.obter_proximo_token()
    else:
      self.erro("Fator esperado")


  def variavel(self):
    if self.classe != "identificador":
      self.erro("Identificador esperado")
    self.obter_proximo_token()


  def chamada_de_funcao(self):
    if self.classe != "identificador":
      self.erro("Identificador esperado")
      
    self.obter_proximo_token()
    if self.token.strip() == "(":
      self.obter_proximo_token()
      self.lista_de_expressoes()
      if self.token.strip() != ")":
        self.erro("')' esperado")
      self.obter_proximo_token()
