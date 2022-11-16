import pygame
import tabla
import collections
import random as r
import busqueda
class jugador:
    def __init__(self,color,tipo):
        self.color=color
        self.prisioneros=collections.defaultdict(int)
        self.turnos=0
        self.bot=tipo
    
    def put_stone_human(self,size):
        x, y = pygame.mouse.get_pos()
        col, row = tabla.xy_to_colrow(x, y,size)
        return col,row
    
    def put_stone_bot(self,board):
        #experimento no sera final
        #x = r.randrange(1000)
        #y = r.randrange(1000)

        #col, row = tabla.xy_to_colrow(x, y,size)
        if self.color=="Black":
            s_max = "Black"
            s_min = "White"
        else:
            s_max = "White"
            s_min = "Black"
        bot = busqueda(board,s_max,s_min)
        col, row = bot.inicia_busqueda()
        
        return col,row
