from juego import juego
from jugador import jugador
import pygame
import numpy as np
#5x5 = 25
if __name__ == "__main__":
    jugador1=jugador(color="black",tipo=False)
    jugador2=jugador(color="white",tipo=True)
    g = juego(size=5,jugador1=jugador1,jugador2=jugador2)
    g.init_pygame()
    g.clear_screen()
    g.draw()

    while True:
        g.update()
        pygame.time.wait(100)