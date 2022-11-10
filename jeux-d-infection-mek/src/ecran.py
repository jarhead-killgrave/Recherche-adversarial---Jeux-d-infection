import copy
import os
import sys
import time
from typing import Union
import pygame
from pygame import Surface
from pygame.event import Event
from pygame.surface import SurfaceType
from etat import Etat
import image
import numpy as np

class Ecran:
    
    def __init__(self, screen: Union[Surface, SurfaceType]):
        self.screen = screen
        self.width, self.height = screen.get_size()

    def react_to(self, event: Event) -> None:
        if event.type == pygame.QUIT:
            sys.exit()

    def draw(self):
        self.screen.fill((255, 255, 255))
    

class Jeu(Ecran):
    def __init__(self, screen: Union[Surface, SurfaceType]):
        Ecran.__init__(self, screen)
        self.etat = Etat()
        self.image = image.Image()
        self.tour = 0


    

    def react_to(self, event: Event) -> None:
        Ecran.react_to(self, event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                a = self.etat.get_moves()
                mvt = None
                if self.etat.get_joueur() == 0 and len(a) > 0:
                    print("ok")
                    mvt = self.etat.get_best_moves(1)

                elif len(a) > 0:
                    mvt = np.random.choice(a)
                print(mvt)
                self.etat = self.etat.play(mvt)
                self.etat.afficher()
            if event.key == pygame.K_z:
                self.etat = self.etat.etats_precedent[-2]


    def draw(self):
        Ecran.draw(self)
        self.image.dessiner_grille(self.etat.grille, self.screen)


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    my_frame = Jeu(screen)
    horloge = pygame.time.Clock()
    my_frame.etat.afficher()
    while True:
        time = horloge.tick(60)
        for event in pygame.event.get():
            my_frame.react_to(event)
        
        my_frame.draw()
        if my_frame.etat.is_over():
            break
        pygame.display.flip()

    print(f"le score du joueur 0 est {my_frame.etat.getScore(0)} et le score du joueur 1 est {my_frame.etat.getScore(1)}")
        

