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
    
    def calcular_rodeado(self,board,c_a):
        #calcula cuanto a rodeado al enemigo
        heu=0
        if c_a == "black":
            c_e="white"
        else:
            c_e="black"
        if len(list(tabla.get_stone_groups(board,c_e)))==0:
            return 0
        else:
            for groups in list(tabla.get_stone_groups(board,c_e)):
                up, down = self.contar_rodeado(c_a,board,groups)
                heu_prov=(up/down)*100
                heu+=heu_prov
            return heu

    def contar_rodeado(self,c,m,group):
        #e es estado
        #c color
        cant_up = 0
        cant_down=0
        if c=="black":
            c_l=1
        else:
            c_l=2   
        for x,y in group:
            #up
            if m[x-1,y] in [c_l,""]:
                cant_up+=1
            if m[x,y-1] in [c_l,""]:
                cant_up+=1 
            if y<m.shape[0] - 1 and m[x,y+1] in [c_l,""]:
                cant_up+=1
            if x<m.shape[0] - 1 and m[x+1,y] in [c_l,""]:
                cant_up+=1
            #down
            if x+1<m.shape[0]:
                cant_down+=1
            if x-1>=0:
                cant_down+=1 
            if y-1>=0:
                cant_down+=1
            if y+1<m.shape[1]:
                cant_down+=1
        return cant_up,cant_down
    
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
                    posibles.append([x-1,y])
                if m[x,y-1] == 0:
                    posibles.append([x,y-1])
                if y<m.shape[0] - 1 and m[x,y+1] == 0:
                    posibles.append([x,y+1])
                if x<m.shape[0] - 1 and m[x+1,y] == 0:
                    posibles.append([x+1,y])
        return posibles
    
    
    def forzar_captura(self,e,color):
        m=e.get_estado()
        for groups in list(tabla.get_stone_groups(m,color)):
                if tabla.has_no_liberties(m,groups):
                    return 100
        return 0
    
    def juego_terminado(self,e):
        #no mas espacios vacios y si hubo captura
        flag=False
        m=e.get_estado()
        print(m)
        for c in ["black","white"]:
            for groups in list(tabla.get_stone_groups(m,c)):
                if tabla.has_no_liberties(m,groups):
                    flag=True
        return len(self.ver_espacios_vacios(e))==0 or flag==True

    def calcular_heuristica(self,e,c):
        #se espera calcular cantidad de fichas rodeadas - cantidad de fichas enemigas posiblemente perjudiciales + forzar capturra
        m=e.get_estado()
        if c=="black":
            return self.calcular_rodeado(m,self.s_max)-self.calcular_rodeado(m,self.s_min)+self.forzar_captura(e,self.s_max)
        else:
            return self.calcular_rodeado(m,self.s_min)-self.calcular_rodeado(m,self.s_max)+self.forzar_captura(e,self.s_min)
    

    def se_mueve_a(self, e, posicion, simbolo):
        #nueva_matriz=np.zeros((5,5))
        x,y = posicion
        #nueva_matriz = [filas[:] for filas in e.get_estado()]
        nueva_matriz = np.copy(e.get_estado())
        if simbolo=="black":
            number=1
        else:
            number=2
        nueva_matriz[x,y] = number
        return estado(nueva_matriz, e, " fila: " + str(posicion[0]) + ", columna: " + str(posicion[1]), e.get_nivel() + 1)

    def algoritmo_minimax(self, e, p, t):
        if p == 0 or self.juego_terminado(e):
            e.set_heu(self.calcular_heuristica(e, t))
            self.estados_descubiertos += 1
            return e.get_heu()

        if t: #turno de max (jugador principal)
            hijos = []
            maximo = -math.inf
            e_max = None
            posiciones_hijos = self.ver_espacios_posibles(e,self.s_min)
            for posicion in posiciones_hijos:
                hijos.append(self.se_mueve_a(e, posicion, self.s_max))
            for hijo in hijos:
                eval = self.algoritmo_minimax(hijo, p - 1, False)
                if eval >= maximo:
                    maximo = eval
                    #e_max = [filas[:] for filas in hijo.get_estado()]
                    e_max = np.copy(hijo.get_estado())
            #self.estado_solucion = [filas[:] for filas in e_max]
            self.estado_solucion=e_max
            return maximo

        else: #turno de min (adversario)
            hijos = []
            minimo = math.inf
            e_min = None
            posiciones_hijos = self.ver_espacios_posibles(e,self.s_max)
            for posicion in posiciones_hijos:
                hijos.append(self.se_mueve_a(e, posicion, self.s_min))
            for hijo in hijos:
                eval = self.algoritmo_minimax(hijo, p - 1, True)
                if eval <= minimo:
                    minimo = eval
                    #e_min = [filas[:] for filas in hijo.get_estado()]
                    e_min = np.copy(hijo.get_estado())
            #self.estado_solucion = [filas[:] for filas in e_min]
            self.estado_solucion=e_min
            return minimo

    def inicia_busqueda(self):
        self.algoritmo_minimax(self.estado_inicial, 4, True)
        mejor = -math.inf
        lista_solucion=[]
        for solucion in lista_solucion:
            if solucion[1] == mejor:
                self.estado_solucion = solucion[0]
        print("Estados Descubiertos: " + str(self.estados_descubiertos))
        return self.estado_solucion
