import pygame
import tabla
import collections
import random as r
from busqueda import *
class jugador:
    def __init__(self,color,tipo):
        self.color=color
        self.prisioneros=collections.defaultdict(int)
        self.turnos=0
        self.bot=tipo
    
    def put_stone_human(self,size):
        x, y = pygame.mouse.get_pos()
        #y = pygame.mouse.get_pos()
        col, row = tabla.xy_to_colrow(x, y, size)
        matriz = [col,row]
        print(matriz)
        #print(tabla.xy_to_colrow(tabla.xy_to_colrow(x, y, size)))
        return col, row
    
    def put_stone_bot(self,board):
        #experimento no sera final
        flag=False
        for i in range(board.shape[0]):
            for j in range(board.shape[0]):
                if board[i,j]!=0:
                    flag=True
        if flag==False:
            x = r.randrange(1000)
            y = r.randrange(1000)
            col, row = tabla.xy_to_colrow(x, y, board.shape[0])
        else:
            if self.color=="Black":
                s_max = 1
                s_min = 2
            else:
                s_max = 2
                s_min = 1
            bot = busqueda(board,s_max,s_min)
            new_board = bot.inicia_busqueda() #mejor solucion
            for i in range(board.shape[0]):
                for j in range(board.shape[0]):
                    if new_board[i,j] == board[i,j]: #antes era !=
                        print("entre ")
                        #col, row = i, j
                        col,row = r.randrange(5),r.randrange(5)
        return col,row