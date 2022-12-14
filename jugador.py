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
        col, row = tabla.xy_to_colrow(x, y, size)
        return col, row
    
    def put_stone_bot(self,board):
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
            s_max="black" if self.color=="black" else "white"
            s_min="white" if self.color=="black" else "black"

            '''
            if self.color=="black":
                s_max = "black"
                s_min = "white"
            else:
                s_max = "white"
                s_min = "black"
            '''
            
            bot = busqueda(board,s_max,s_min)
            new_board = bot.inicia_busqueda() #mejor solucion
            for i in range(board.shape[0]):
                for j in range(board.shape[0]):
                    if new_board[i,j]!= board[i,j]:
                        col, row = i, j

        return col,row