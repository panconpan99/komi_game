import tabla
from random import choice
import numpy as np
import pygame
import itertools
import sys
from pygame import gfxdraw

BOARD_BROWN = (199, 105, 42)
BOARD_WIDTH = 1000
BOARD_BORDER = 75
STONE_RADIUS = 22
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURN_POS = (BOARD_BORDER, 20)
SCORE_POS = (BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER + 30)
WIN_POS=(500,500)
DOT_RADIUS = 4

class juego:
    def __init__(self,size,jugador1,jugador2):
        self.board = np.zeros((size, size))
        self.size = size
        self.jugador_1=jugador1
        self.jugador_2=jugador2
        self.turno=choice([True,False])
        self.ganador=False
        self.start_points, self.end_points = tabla.make_grid(self.size)
    
    def init_pygame(self):
        pygame.init()
        screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 30)

    def clear_screen(self):

        # fill board and add gridlines
        self.screen.fill(BOARD_BROWN)
        for start_point, end_point in zip(self.start_points, self.end_points):
            pygame.draw.line(self.screen, BLACK, start_point, end_point)

        # add guide dots
        guide_dots = [3, self.size // 2, self.size - 4]
        for col, row in itertools.product(guide_dots, guide_dots):
            x, y = tabla.colrow_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, DOT_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, DOT_RADIUS, BLACK)
    
    def turns(self):

        if self.turno:
            if not self.jugador_1.bot:
                col,row = self.jugador_1.put_stone_human(self.size)
            else:
                col,row =self.jugador_1.put_stone_bot(self.board)

            if not tabla.is_valid_move(col, row, self.board):
                return
            self.board[col, row] = 1
            self.jugador_1.turnos+=1
        else:
            if not self.jugador_2.bot:
                col,row = self.jugador_2.put_stone_human(self.size)
            else:
                col,row =self.jugador_2.put_stone_bot(self.board)

            if not tabla.is_valid_move(col, row, self.board):
                return
            self.board[col, row] = 2
            self.jugador_2.turnos+=1
            
        self_color = "black" if self.turno else "white"
        other_color = "white" if self.turno else "black"
        # handle captures
        capture_happened = False
        #despues se eliminia
        print(f""+ str(other_color) + " : "+ str(list(tabla.get_stone_groups(self.board,other_color)))) # aca se ve los grupos del oponente
        #print(list(bot.calcular_rodeado(self_color,self.board)))
        #print(list(bot.calcular_rodeado(other_color,self.board)))
        #hasta aca
        for group in list(tabla.get_stone_groups(self.board, other_color)):
            if tabla.has_no_liberties(self.board, group):
                capture_happened = True
                for i, j in group:
                    self.board[i, j] = 0
                if self.turno:
                    self.jugador_1.prisioneros[self_color] += len(group)
                else:
                    self.jugador_2.prisioneros[self_color] += len(group)

        # handle special case of invalid stone placement
        # this must be done separately because we need to know if capture resulted
        if not capture_happened:
            group = None
            for group in tabla.get_stone_groups(self.board, self_color):
                if (col, row) in group:
                    break
            if tabla.has_no_liberties(self.board, group):
                self.board[col, row] = 0
                return
        #if self.jugador_1.prisioneros[self_color]>=3 or self.jugador_2.prisioneros[self_color]>=3:
         #   self.ganador=True
          #  self.win(self_color)
        #else:
         #   self.pass_move()

        self.ganador=self.victory(self.jugador_1.prisioneros[self_color],self.jugador_2.prisioneros[self_color]) 
        if self.ganador:
            self.win(self_color)
        else:
            self.pass_move()
    
    def victory(self,jugador_1,jugador_2):
        if jugador_1>=3 or jugador_2>=3:
            return True
        else:
            return False

    def win(self,color):
        self.draw()
        if color=="black":
            msg=(
                f"Black wins!!! press X to close, done in {self.jugador_1.turnos} moves" 
            )
            txt = self.font.render(msg, True, BLACK)
            self.screen.blit(txt, SCORE_POS)
        elif color=="white":
            msg=(
                f"White wins!!! press X to close, done in {self.jugador_2.turnos} moves"
            )
            txt = self.font.render(msg, True, BLACK)
            self.screen.blit(txt, SCORE_POS)
        pygame.display.flip()
    
    def pass_move(self):
        self.turno = not self.turno
        self.draw()

    def draw(self):
        # draw stones - filled circle and antialiased ring
        self.clear_screen()
        for col, row in zip(*np.where(self.board == 1)):
            x, y = tabla.colrow_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, BLACK)
        for col, row in zip(*np.where(self.board == 2)):
            x, y = tabla.colrow_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, WHITE)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, WHITE)
        # text for score and turn info
        if not self.ganador:
            score_msg = (
                f"Black's Prisoners: {self.jugador_1.prisioneros['black']}"
                + f"     White's Prisoners: {self.jugador_2.prisioneros['white']}"
            )
            txt = self.font.render(score_msg, True, BLACK)
            self.screen.blit(txt, SCORE_POS)
            turn_msg = (
                f"{'Black' if self.turno else 'White'} to move. "
                + "Click to place stone, press P to pass."
            )
            txt = self.font.render(turn_msg, True, BLACK)
            self.screen.blit(txt, TURN_POS)
        pygame.display.flip()

    def update(self):
        # TODO: undo button
        events = pygame.event.get()
        for event in events:
            if not self.ganador:
                if self.turno:
                    if not self.jugador_1.bot:
                        if event.type==pygame.MOUSEBUTTONUP:
                            self.turns()
                    else:
                        self.turns()
                else:
                    if not self.jugador_2.bot:
                        if event.type==pygame.MOUSEBUTTONUP:
                            self.turns()
                    else:
                        self.turns()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.pass_move()
                if self.ganador:
                    if event.key==pygame.K_x:
                        sys.exit()


