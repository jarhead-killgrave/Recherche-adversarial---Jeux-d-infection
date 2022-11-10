from abc import ABC, abstractmethod



class Algorithm(ABC):

    def __init__(self, joueur: int, profondeur: int):
        self.joueur = joueur
        self.profondeur = profondeur
        self.noeud_visite = 0
    
    @abstractmethod
    def get_best_moves(self, state):
        pass

    def incremente_noeud(self):
        self.noeud_visite += 1
