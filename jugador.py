import pygame
import tabla
import collections
import random as r

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
    
    def put_stone_bot(self,size):
        #experimento no sera final
        x = r.randrange(1000)
        y = r.randrange(1000)
        col, row = tabla.xy_to_colrow(x, y,size)
        return col,row
