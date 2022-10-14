import pygame
import numpy as np
import itertools
import networkx as nx
import collections
from pygame import gfxdraw


# Game constants
BOARD_BROWN = (199, 105, 42)
BOARD_WIDTH = 1000
BOARD_BORDER = 75
STONE_RADIUS = 22
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURN_POS = (BOARD_BORDER, 20)
SCORE_POS = (BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER + 30)
DOT_RADIUS = 4
