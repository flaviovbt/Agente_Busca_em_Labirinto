from classes.Agente import Agente
from time import sleep

from classes.Labirinto import Labirinto

labirinto = Labirinto("mapas/labirinto1.pbm", 90)

agente = Agente(labirinto, admissivel=0)

agente.salvar_header()

while(agente.mover() != 1):
    sleep(0)
