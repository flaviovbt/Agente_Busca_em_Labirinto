from math import fabs

class Agente:


  def __init__(self, labirinto, admissivel=True):
    self.labirinto = labirinto

    #coordenadaAgente é referente a posição inicial do meu agente no labirinto.
    self.coordenadaAgente = self.labirinto.agente_posicoes
    
    #celulaAgente é referente a posição atual do agente.
    self.celulaAgente = self.labirinto.labirinto[self.coordenadaAgente[0]][self.coordenadaAgente[1]]
    
    self.abertos = set()
    self.fechados = {self.celulaAgente}
    self.caminho = []
    self.abrirCelula = self.__abrirCelula if admissivel == True else self.__abrirCelula2
    
    self.arvores_de_recompensa = []

  def printarVariaveis(self , celulaAgente):
    print(f'Celula Atual: \n')
    print(f'Posicao X do Agente: [{celulaAgente.x}]')
    print(f'Posicao Y do Agente: [{celulaAgente.y}]')
    print(f'Funcao Avaliacao: [{celulaAgente.f_avaliacao}]')
    print(f'Tipo: [{celulaAgente.tipo}]')
    print(f'Custo: [{celulaAgente.cost}]')
    print(f'Manhattan || Area: [{celulaAgente.manhattan}]')
    print(f'Coordenadas Celula Pai: [{celulaAgente.pai}]')


  #Acões
  def mover(self):

    if(len(self.labirinto.recompensas) == 0):
      print(self)
      self.printarVariaveis(self.celulaAgente)
      self.salvar_mover()
      self.salvar_footer()
      return 1
      
    self.getCelulasAdjacentes()
    
    celulaExpansao = max(self.abertos, key=lambda celula: celula.f_avaliacao)
    self.fechados.add(celulaExpansao)
    self.abertos.discard(celulaExpansao)

    self.coordenadaAgente = [celulaExpansao.y, celulaExpansao.x]
    if celulaExpansao.tipo == 'r':
      with open(f'{self.labirinto.seed}-arvores_finais.txt', 'a', encoding='utf-8') as f:
        f.write(self.string_mover())
      celula = [item for item in self.labirinto.recompensas if item[0] == celulaExpansao.y and item[1] == celulaExpansao.x][0]
      self.labirinto.recompensas.remove(celula)
      self.__caminhoFinal(celulaExpansao)
      
      # Se achou uma recompensa, redefine o tabuleiro para o estado inicial
      for aberto in self.abertos:
        aberto.cost = float('inf')
        aberto.pai = None
      for fechado in self.fechados:
        fechado.cost = float('inf')
        fechado.pai = None
      self.abertos = set()
      self.fechados = set()

      #Pequenas alterações para que o jogo possa continuar da recompensa que ele acabou de pegar
      self.celulaAgente = celulaExpansao 
      self.celulaAgente.cost = 0
      self.fechados.add(self.celulaAgente)
      self.celulaAgente.tipo = '0'
      return 0
    self.celulaAgente = celulaExpansao # Altero a celula onde o agente se encontra para a celula q foi expandida
    
    print(self) # Printa o labirinto

    self.printarVariaveis(self.celulaAgente) # Printa as informações a respeito da celula atual do agente
   
    self.salvar_mover()

  #Algoritmo

  def getCelulasAdjacentes(self):
    pos_y_agente, pos_x_agente = self.coordenadaAgente
    """
      Retorna as celulas adjacentes passiveis de movimentacao. O tabuleiro eh visto na perspectiva do canto inferior direito (a iteracao eh feita de cima para baixo)
    """    
    up = self.labirinto.labirinto[pos_y_agente-1][pos_x_agente]
    self.abrirCelula(up)

    down = self.labirinto.labirinto[pos_y_agente+1][pos_x_agente]
    self.abrirCelula(down)

    right = self.labirinto.labirinto[pos_y_agente][pos_x_agente+1]
    self.abrirCelula(right)
    
    left = self.labirinto.labirinto[pos_y_agente][pos_x_agente-1]
    self.abrirCelula(left)
    

  # Abre as celulas utilizando heuristica admissivel
  def __abrirCelula(self, celulaExpansao):
    """
      Aqui eh feito o calculo da funcao heuristica para cada um dos alvos
    """
    if celulaExpansao.tipo != '1' and celulaExpansao.cost > self.celulaAgente.cost:

      self.abertos.add(celulaExpansao)
      
      if celulaExpansao in self.fechados:
        self.fechados.discard(celulaExpansao)

      celulaExpansao.pai = self.celulaAgente
      celulaExpansao.cost = self.celulaAgente.cost + 1
      f_avaliacao = []

      for i, recompensa in enumerate(self.labirinto.recompensas):
        celulaExpansao.manhattan[i] = fabs(recompensa[0]-celulaExpansao.y)+fabs(recompensa[1]-celulaExpansao.x)
        f_avaliacao.append(recompensa[2] - 0.7*celulaExpansao.cost - celulaExpansao.manhattan[i])
      celulaExpansao.f_avaliacao =  max(f_avaliacao)

  # Abre as celulas utilizando heuristica não admissivel
  def __abrirCelula2(self, celulaExpansao):
    """
      Aqui eh feito o calculo da funcao heuristica para cada um dos alvos
    """
    if celulaExpansao.tipo != '1' and celulaExpansao.cost > self.celulaAgente.cost:

      self.abertos.add(celulaExpansao)
      
      if celulaExpansao in self.fechados:
        self.fechados.discard(celulaExpansao)

      celulaExpansao.pai = self.celulaAgente
      celulaExpansao.cost = self.celulaAgente.cost + 1
      f_avaliacao = []

      for i, recompensa in enumerate(self.labirinto.recompensas):
        #Aqui consideramos a Area ao invés de manhattan para heuristica não admissivel
        celulaExpansao.manhattan[i] = (fabs(recompensa[0]-celulaExpansao.y)+1 if fabs(recompensa[0]-celulaExpansao.y) > 0 else 0)*(fabs(recompensa[1]-celulaExpansao.x)+1 if fabs(recompensa[1]-celulaExpansao.x) > 0 else 0)

        f_avaliacao.append(recompensa[2] - 0.7*celulaExpansao.cost - celulaExpansao.manhattan[i])
      celulaExpansao.f_avaliacao =  max(f_avaliacao)
      
  # Função recursiva que é executada no final da execução, que basicamente entra o pai de todas as celulas de forma iterativa
  def __caminhoFinal(self, celula):
    pai = celula.pai
    if pai:
      self.__caminhoFinal(pai)
    self.caminho.append(celula)

  def __str__(self):
    str_lab = self.labirinto.list_str()
    for passo in self.caminho:
      str_lab[passo.y][passo.x] ='🟪\u200c'
    for fechado in self.fechados:
      str_lab[fechado.y][fechado.x] = '🟩\u200c'
    for aberto in self.abertos:
      str_lab[aberto.y][aberto.x] = '🟦\u200c'
    str_lab[self.coordenadaAgente[0]][self.coordenadaAgente[1]] = '🟥\u200c'
    str_str = []
    for l in str_lab:
      str_str.append(''.join(l))

    str_lab = '\n'.join(str_str)
    return f"{str_lab}\n"


  def string_mover(self):
    def arvore(abertos, fechados):
      string = ''
      for item in fechados:
        string = f'{string}[{item}, {item.pai}, {item.f_avaliacao}], '
      for item in abertos:
        string = f'{string}[{item}, {item.pai}, {item.f_avaliacao}], '
      string = f'{string}]\n'
  
      return string
    
    def lista(lista):
      string = ''
      for item in lista:
        string = f'{string}({item.x}, {item.y}), '
      string = f'{string}]\n'
      return string

    string = ''


    string = f'{string}Abertos: ['
    string = f'{string}{lista(self.abertos)}'
    string = f'{string}Fechados: ['
    string = f'{string}{lista(self.fechados)}'
    string = f'{string}Arvore: ['
    string = f'{string}{arvore(self.abertos, self.fechados)}\n'

    string = f'{string}{self}\n'
  
    return string

  def salvar_mover(self):
    string = self.string_mover()
    
    with open(f'{self.labirinto.seed}.txt', 'a', encoding='utf-8') as f:
      f.write(string)

  def salvar_header(self):
    string = ''
    def lista(lista):
      string = ''
      for item in lista:
        string = f'{string}(Valor: {item[2]}, x: {item[1]}, y:{item[0]}), '
      string = f'{string}]\n'
      return string
    string = f'{string}Seed: {self.labirinto.seed}\n'
    string = f'{string}Recompensas: ['
    string = f'{string}{lista(self.labirinto.recompensas)}'
    string = f'{string}Agente: [x: {self.labirinto.agente_posicoes[1]}, y: {self.labirinto.agente_posicoes[0]}]\n'
    string = f'{string}{self}\n'
    with open(f'{self.labirinto.seed}.txt', 'w', encoding='utf-8') as f:
      f.write(string)

    with open(f'{self.labirinto.seed}-arvores_finais.txt', 'w', encoding='utf-8') as f:
      f.write(string)

  def salvar_footer(self):
    string = f'custo: {len(self.caminho)-3}\n'

    with open(f'{self.labirinto.seed}.txt', 'a', encoding='utf-8') as f:
      f.write(string)

    with open(f'{self.labirinto.seed}-arvores_finais.txt', 'a', encoding='utf-8') as f:
      f.write(string)
