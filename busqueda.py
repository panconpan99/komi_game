from estado import *
from collections import deque
import sys, os, math
import tabla
import numpy as np
class busqueda:
    #algoritmo minimax
    def __init__(self,EI, s_max, s_min):
        self.estado_inicial = estado(EI, None, "Origen", 0)
        self.estado_solucion = None
        self.s_max = s_max
        self.s_min = s_min
        self.estados_descubiertos = 0
    

    def contar_rodeado(self,m,c,group):
        #e es estado
        #c color
        if c == 1:
            c_l=2
        else:
            c_l=1
        cant = 0

        for x,y in group:
            if m[x-1,y] in [c_l,""]:
                cant+=1
            if m[x,y-1] in [c_l,""]:
                cant+=1 
            if y<m.shape[0] - 1 and m[x,y+1] in [c_l,""]:
                cant+=1
            if x<m.shape[0] - 1 and m[x+1,y] in [c_l,""]:
                cant+=1
        return cant

    def ver_espacios_vacios(self,e):
        m=e.get_estado()
        vacios=[]
        for i in range(4):
            for j in range(4):
                if m[i,j]==0:
                    vacios.append([i,j])
        return vacios

    def ver_espacios_posibles(self,e,c):
        m=e.get_estado()
        posibles=[]
        for group in list(tabla.get_stone_groups(m,c)):
            for x,y in group:
                if m[x-1,y] == 0:
                    posibles.append([x,y])
                if m[x,y-1] == 0:
                    posibles.append([x,y])
                if y<m.shape[0] - 1 and m[x,y+1] == 0:
                    posibles.append([x,y])
                if x<m.shape[0] - 1 and m[x+1,y] == 0:
                    posibles.append([x,y])
        return posibles
    

    def forzar_captura(self,e,group):
        m=e.get_estado()
        if tabla.has_not_liberties(m,group):
            return 100
        
    def juego_terminado(self,e):
        return len(self.ver_espacios_vacios(e))==0

    def calcular_heuristica(self,e,c):
        #aca calculara los espacios alrededor del grupo
        m=e.get_estado()
        if c==1:
            return self.calcular_rodeado(m,self.s_max)-self.calcular_rodeado(m,self.s_min)
        else:
            return self.calcular_rodeado(m,self.s_min)-self.calcular_rodeado(m,self.s_max)

    def calcular_rodeado(self,board,c):
        heu=0
        for group in list(tabla.get_stone_groups(board,c)):
            heu=self.contar_rodeado(c,board,group)
        return heu

    def se_mueve_a(self, e, posicion, simbolo):
        new_simbolo=simbolo
        nueva_matriz=np.zeros((5,5))
        x,y = posicion
        #nueva_matriz = [filas[:] for filas in e.get_estado()] copia de matriz, valor por valor
        nueva_matriz = e.get_estado()
        nueva_matriz[x,y] = new_simbolo
        return estado(nueva_matriz, e, " fila: " + str(posicion[0]) + ", columna: " + str(posicion[1]), e.get_nivel() + 1)

    def algoritmo_minimax(self, e, p, t):
        if p == 0 or self.juego_terminado(e):
            e.set_heu(self.calcular_heuristica(e, t))
            self.estados_descubiertos += 1
            return e.get_heu()

        if t: #turno de max (jugador principal)
            hijos = []
            maximo = -math.inf
            e_max = np.zeros((5,5))
            posiciones_hijos = self.ver_espacios_posibles(e,self.s_max)
            for posicion in posiciones_hijos:
                hijos.append(self.se_mueve_a(e, posicion, self.s_max))
            for hijo in hijos:
                eval = self.algoritmo_minimax(hijo, p - 1, False)
                if eval >= maximo:
                    maximo = eval
                    e_max = e.get_estado()
            self.estado_solucion =e_max
            return maximo

        else: #turno de min (adversario)
            hijos = []
            minimo = math.inf
            e_min = np.zeros((5,5))
            posiciones_hijos = self.ver_espacios_posibles(e,self.s_min)
            for posicion in posiciones_hijos:
                hijos.append(self.se_mueve_a(e, posicion, self.s_min))
            for hijo in hijos:
                eval = self.algoritmo_minimax(hijo, p - 1, True)
                if eval <= minimo:
                    minimo = eval
                    e_min = e.get_estado()
            self.estado_solucion =e_min
            return minimo

    def inicia_busqueda(self):
        #algo hara aca tranquilo ekisdede
        self.algoritmo_minimax(self.estado_inicial, 4, True)
        mejor = -math.inf
        lista_solucion=[]
        for solucion in lista_solucion:
            if solucion[1] == mejor:
                self.estado_solucion = solucion[0]
        print("Estados Descubiertos: " + str(self.estados_descubiertos))
        return self.estado_solucion
