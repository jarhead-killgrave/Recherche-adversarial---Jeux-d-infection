from typing import Union
import pygame
from pygame import Surface
from pygame.surface import SurfaceType
import numpy as np
import etat


pygame.init()

class Image:
    def __init__(self):
        super().__init__()
        self.representation = {
            -1: pygame.image.load("./images/case-noire.jpg"),
            0: pygame.image.load("./images/case-bleu.jpg"),
            1: pygame.image.load("./images/case-rouge.png"),
        }
        self.taille = self.representation[-1].get_width()
        

    def dessiner_grille(self, plateau: np.ndarray, ecran: Union[Surface, SurfaceType]):
        coords = np.array(np.meshgrid(np.arange(7), np.arange(7))).T.reshape(-1, 2)
        for coord in coords:
            val = plateau[tuple(coord)]
            if val in self.representation:
                ecran.blit(self.representation[val], (coord[1] * self.taille, coord[0] * self.taille))

