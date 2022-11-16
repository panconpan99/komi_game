import estado
from collections import deque
import sys, os, math
import tabla
class busqueda:
    #algoritmo minimax
    def __init__(self, EI, s_max, s_min):
        self.estado_inicial = estado(EI, None, "Origen", 0)
        self.estado_solucion = None
        self.s_max = s_max
        self.s_min = s_min
        self.estados_descubiertos = 0
    
    def calcular_heuristica(self,e):
        m=e.get_estado()
        
        #aca calculara los espacios alrededor del grupo
        return
    
    def inicia_busqueda():
        #algo hara aca tranquilo ekisdede
        return
