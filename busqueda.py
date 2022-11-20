from estado import *
from collections import deque
import sys, os, math
import tabla
class busqueda:
    #algoritmo minimax
    def __init__(self,EI, s_max, s_min):
        self.estado_inicial = estado(EI, None, "Origen", 0)
        self.estado_solucion = None
        self.s_max = s_max
        self.s_min = s_min
        self.estados_descubiertos = 0
    

    def contar_rodeado(self,c,board,group):
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

    def ver_espacios_vacios(self,e):
        m=e.get_estado()
        vacios=[]
        for i in range(m.shape[0]-1):
            for j in range(m.shape[0]-1):
                if m[i][j]==0:
                    vacios.append([i,j])
        return vacios
    
    def forzar_captura(self,e,group):
        m=e.get_estado()
        if tabla.has_not_liberties(e,group):
            return 100
        
    def juego_terminado(self,e):
        return len(self.ver_espacios_vacios(e))==0

    def calcular_heuristica(self,e,c):
        #aca calculara los espacios alrededor del grupo
        m=e.get_estado()
        if c=="black":
            return self.contar_rodeado(m,self.s_max)-self.contar_rodeado(m,self.s_min)
        else:
            return self.contar_rodeado(m,self.s_min)-self.contar_rodeado(m,self.s_max)

    def calcular_rodeado(self,board,c):
        heu=0
        heu_group=[]
        for group in list(tabla.get_stone_groups(board,c)):
            heu=self.contar_rodeado(c,board,group)
            heu_group.append(group)
        return heu_group

    def se_mueve_a(self, e, posicion, simbolo):
        nueva_matriz = [filas[:] for filas in e.get_estado()] # copia de matriz, valor por valor
        nueva_matriz[posicion[0]][posicion[1]] = simbolo
        return estado(nueva_matriz, e, " fila: " + str(posicion[0]) + ", columna: " + str(posicion[1]), e.get_nivel() + 1)

    def algoritmo_minimax(self, e, p, t):
        if p == 0 or self.juego_terminado(e):
            e.set_heuristica(self.calcular_heuristica(e, t))
            self.estados_descubiertos += 1
            return e.get_heuristica()

        if t: #turno de max (jugador principal)
            hijos = []
            maximo = -math.inf
            e_max = None
            posiciones_hijos = self.ver_espacios_vacios(e)
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
            posiciones_hijos = self.ver_espacios_vacios(e)
            for posicion in posiciones_hijos:
                hijos.append(self.se_mueve_a(e, posicion, self.s_min))
            for hijo in hijos:
                eval = self.algoritmo_minimax(hijo, p - 1, True)
                if eval <= minimo:
                    minimo = eval
                    e_min = [filas[:] for filas in hijo.get_estado()]
            self.estado_solucion = [filas[:] for filas in e_min]
            return minimo

    def inicia_busqueda(self):
        #algo hara aca tranquilo ekisdede
        self.algoritmo_minimax(self.estado_inicial, 2, True)
        mejor = -math.inf
        lista_solucion=[]
        for solucion in lista_solucion:
            if solucion[1] == mejor:
                self.estado_solucion = solucion[0]
        print("Estados Descubiertos: " + str(self.estados_descubiertos))
        return self.estado_solucion
