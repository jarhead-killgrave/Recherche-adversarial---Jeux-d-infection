import numpy as np
from move import Move

#Une grille sera representer par un grille forme de 3 chiffre
#1 qui represente les cases appartenant au joueur 1
#2 qui represente les cases appartenant au joueur 2
#0 les case libres de placement

#une grille a une taille 7 * 7 par defaut
GRILLE_INITIALE = np.full((7,7),-1, dtype=np.int8)
GRILLE_INITIALE[[-1,0], [0, -1]] = 0
GRILLE_INITIALE[[0,-1], [0, -1]] = 1

# mouvementsimple = {"d": np.array(0, 1), "g": np.array(0, -1), "b": np.array(1, 0), "h": np.array(-1, 0)}

# mouvementdouble = {"d": np.array(0, 2), "g": np.array(0, -2), "b": np.array(2, 0), "h": np.array(-2, 0)}

# def mouvements(x):
#     return {"d": np.array(0, x), "g": np.array(0, -x), "b": np.array(x, 0), "h": np.array(-x, 0)}

class State:

    def __init__(self,
                grille = GRILLE_INITIALE,
                pions = np.array([[]]),
                joueur_actif = 0) -> None:
        
        self.grille = grille
        self.pions = pions
        self.joueur_actif = joueur_actif
    
    def __str__(self) -> str:
        return str(self.grille) + "\nLe joueur actif est le joueur " + str(self.joueur_actif) + "\nLes pions du joueur se trouve au position\n" + str(self.pions) 
    
    def afficher(self) -> None:
        print("C'est le tour du joueur ", self.joueur_actif)
        for ligne in self.grille:
            for colonne in ligne:
                if colonne in (1, 0):
                    print(f" {colonne} |", end="")
                else:
                    print(f"{colonne} |", end="")
            print("\n")
    
    # def mouvementAutorise(self, arrive):
    #     """
    #         Verifie si le movement d'arrive est possible
    #     """
    #     return np.array((0,0)) <= arrive < np.array((7,7)) and self.grille[arrive] == 0

    def isOver(self) -> bool:
        return np.all(self.grille != -1) or (not np.any(self.grille == 0)) or (not np.any(self.grille == 1))
    
    # def getMoves(self, joueur):
    #     result = np.array([[]])
    #     for pion in self.pions:
    #         for mouvement in mouvementsimple, mouvementdouble:

    def getMoves(self, joueur= None):
        if joueur is None:
            joueur = self.joueur_actif
        allpion = np.argwhere(self.grille == joueur)
        res = np.array([], dtype=Move)
        combinaison_action = np.array(np.meshgrid(["d", "g", "h", "b"], ["1", "2"])).T.reshape((-1,2))
        for pion in allpion:
            for action in combinaison_action:
                mouvement = Move(pion, tuple(action))
                res = np.append(res, mouvement) if mouvement.do_move()[1] else np.append(res, None)
        return res
        

    def getScore(self, joueur):
        nj = np.sum(self.grille == joueur)
        nt = np.sum(self.grille == 0) + np.sum(self.grille == 1)
        return nj / nt
    
    def get_joueur(self):
        return self.joueur_actif
    
    
    def play(self, coup:Move):
        new_joueur = (self.joueur_actif + 1) % 2
        new_grille = np.copy(self.grille)
        if coup != None:
            new_pion = coup.do_move()[0]
            new_grille[tuple(new_pion)] = self.joueur_actif
            if coup.get_type_mouvement() == "2":
                new_grille[tuple(coup.get_pion())] = -1
            for pion in Move.cases_adjacente(new_pion):
                if new_grille[tuple(pion)] != -1:
                    new_grille[tuple(pion)] = self.joueur_actif
        new_pions = np.argwhere(new_grille == new_joueur)

        return State(new_grille, new_pions, new_joueur)



    

