from juego import juego
from jugador import jugador
import pygame
import numpy as np
#5x5 = 25
if __name__ == "__main__":
    print("-"*23)
    print("bienvenidos al juego del Komi")
    print("-"*23)
    typer1=int(input("jugador Black: 0 si es humano o 1 si es bot "))
    typer2=int(input("jugador White: 0 si es humano o 1 si es bot "))
    jugador1=jugador(color="black",tipo= True if typer1==1 else False)
    jugador2=jugador(color="white",tipo= True if typer2==1 else False)
    g = juego(size=5,jugador1=jugador1,jugador2=jugador2)
    g.init_pygame()
    g.clear_screen()
    g.draw()

    while True:
        g.update()
        pygame.time.wait(100)