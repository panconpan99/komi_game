import estado
from collections import deque
import sys, os, math
import tabla
class busqueda:
    #algoritmo minimax
    def __init__(self, s_max, s_min):
        #self.estado_inicial = estado(EI, None, "Origen", 0)
        self.estado_solucion = None
        self.s_max = s_max
        self.s_min = s_min
        self.estados_descubiertos = 0
    

    def calcular_rodeado(self,c,board,group):
        #e es estado
        #c color
        #m = e.get_estado()
        if c == "black":
            c_l=2
        else:
            c_l=1
        cant = 0
        for x,y in group:
            if board[x-1,y] in [c_l,""]:
                cant+=1
            if board[x,y-1] in [c_l,""]:
                cant+=1 
            if y<board.shape[0] - 1 and board[x,y+1] in [c_l,""]:
                cant+=1
            if x<board.shape[0] - 1 and board[x+1,y] in [c_l,""]:
                cant+=1
        return cant
    def espacios_vacios(self,board,group):
        cant=0
        for x,y in group:
            if board[x-1,y] == 0:
                cant+=1
            if board[x,y-1] == 0:
                cant+=1 
            if y<board.shape[0] - 1 and board[x,y+1] == 0:
                cant+=1
            if x<board.shape[0] - 1 and board[x+1,y] == 0:
                cant+=1
        return cant
    def calcular_heuristica(self,c,board):
        #aca calculara los espacios alrededor del grupo
        if c=="black":
            return self.calcular_rodeado(m,self.s_max)-self.calcular_rodeado(m,self.s_min)
        else:
            return self.calcular_rodeado(m,self.s_min)-self.calcular_rodeado(m,self.s_max)

    def heuristica_test(self,c,board):
        heu=0
        heu_group=[]
        for group in list(tabla.get_stone_groups(board,c)):
            heu=self.calcular_rodeado(c,board,group)/(self.espacios_vacios(board,group)+self.calcular_rodeado(c,board,group))
            heu_group.append(heu)
        return heu_group

    def algoritmo_minimax(self, e, p, t):
        if p == 0 or self.juego_terminado(e):
            e.set_heuristica(self.calcular_heuristica(e, t))
            self.estados_descubiertos += 1
            return e.get_heuristica()

        if t: #turno de max (jugador principal)
            hijos = []
            maximo = -math.inf
            e_max = None
            posiciones_hijos = self.ver_espacios_vacio(e)
            for posicion in posiciones_hijos:
                hijos.append(self.se_mueve_a(e, posicion, self.s_max))
            for hijo in hijos:
                eval = self.algoritmo_minimax(hijo, p - 1, False)
                if eval >= maximo:
                    maximo = eval
                    e_max = [filas[:] for filas in hijo.get_estado()]
            self.estado_solucion = [filas[:] for filas in e_max] # movimiento con mejor valor de evaluación
            return maximo

        else: #turno de min (adversario)
            hijos = []
            minimo = math.inf
            e_min = None
            posiciones_hijos = self.ver_espacios_vacio(e)
            for posicion in posiciones_hijos:
                hijos.append(self.se_mueve_a(e, posicion, self.s_min))
            for hijo in hijos:
                eval = self.algoritmo_minimax(hijo, p - 1, True)
                if eval <= minimo:
                    minimo = eval
                    e_min = [filas[:] for filas in hijo.get_estado()]
            self.estado_solucion = [filas[:] for filas in e_min]
            return minimo

    def inicia_busqueda():
        #algo hara aca tranquilo ekisdede
        return
