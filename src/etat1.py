import numpy as np
from deplacement import Move
import deplacement
import ia
import itertools as it

GRILLE_INITIALE = np.full((7, 7), -1, dtype=np.int8)
GRILLE_INITIALE[[-1, 0], [0, -1]] = 0
GRILLE_INITIALE[[0, -1], [0, -1]] = 1


action = np.array(np.meshgrid(np.arange(8), [0, 1])).T.reshape(-1, 2)


class Etat:

    def __init__(self,
                 grille: np.ndarray = GRILLE_INITIALE,
                 joueur: int = 0,
                 etats_precedent: np.ndarray = np.array([])) -> None:
        self.grille = grille
        self.joueur = joueur
        self.etats_precedent = etats_precedent

    def __eq__(self, other):

        return (np.all(self.grille == other.grille) and (self.joueur == other.joueur)) if isinstance(other, type(
            self)) else False

    def __ne__(self, other):
        return not self.__eq__(other)

    def update(self) -> np.ndarray:
        """
            Rajoute l'etat courant dans la liste des etat precedents
        """
        return np.hstack((self.etats_precedent, self))

    def afficher(self) -> None:
        """
            Affiche l'etat de la grille courante
        """
        print("C'est le tour du joueur ", self.joueur)
        for ligne in self.grille:
            for colonne in ligne:
                if colonne in (1, 0):
                    print(f" {colonne} |", end="")
                else:
                    print(f"{colonne} |", end="")
            print("\n")

    def get_grille(self) -> np.ndarray:
        """
            Renvoie la grille actuelle
        """
        return self.grille

    def get_joueur(self):
        """
            Renvoie le joueur actuelle
        """
        return self.joueur

    def is_over(self):
        """
            Renvoie Vrai si la partie est terminé
        """
        return (np.sum(self.grille == -1) == 0) or (np.sum(self.grille == 0) == 0) or (
            np.sum(self.grille == 1) == 0) or (np.sum(self.etats_precedent == self) >= 2)

    def select_pion(self, pion):
        """
            renvoie l'ensemble des mouvements possibles d'un pion
        """

        tmp = Move(pion)
        res = np.array(list(map(tmp.prochaine_case, action)))
        indices = np.argwhere(res[:, 1] == True)[:, 0]
        t = list(map(lambda x: self.grille[tuple(x)] == -1, res[indices, 0]))
        u = indices[t]
        return action[u]

    def get_moves(self, joueur=None):
        if joueur is None:
            joueur = self.joueur

        all_pion = np.argwhere(self.grille == joueur)
        
        res = np.array([None], dtype=deplacement.Move)
        
        for pion in all_pion:
            t = self.select_pion(pion)
            tmp = list(map(Move, it.repeat(pion), t))
            res = np.append(res, tmp)
        res = np.unique(res)
        return res

    def getScore(self, joueur=None):
        if joueur is None:
            joueur = self.joueur
        nj = np.sum(self.grille == joueur)
        nt = np.sum(self.grille == 0) + np.sum(self.grille == 1)
        return nj / nt
    
    def evaluate(self, joueur=None):
        if joueur is None:
            joueur = self.joueur
        
        if len(self.etats_precedent) == 0:
            return 1
        
        a = np.sum(self.grille == joueur)
        b = np.sum(self.etats_precedent[-1].grille == joueur)
        
        if a > b:
            return 1 + self.etats_precedent[-1].evaluate(joueur)
        elif a < b:
            return -1 + self.etats_precedent[-1].evaluate(joueur)
        return 0 + self.etats_precedent[-1].evaluate(joueur)

    def play(self, coup: deplacement.Move):
        new_joueur = (self.joueur + 1) % 2
        new_grille = np.copy(self.grille)
        if coup is not None:
            new_pion, _ = coup.prochaine_case()
            new_grille[tuple(new_pion)] = self.joueur

            if coup.direction[1] == 1:
                new_grille[tuple(coup.pion)] = -1

            for pion in Move.cases_adjacentes(new_pion):
                if new_grille[tuple(pion)] != -1:
                    new_grille[tuple(pion)] = self.joueur
            
        return Etat(new_grille, new_joueur, self.update())

    def get_best_moves(self, d, joueur: int = None):
        if joueur is None:
            joueur = self.joueur

        ordi = ia.IA(joueur)
        t = self.get_moves(joueur)
        c = np.array(list(map(self.play, t)))

        m = list(map(ordi.minimax, c, np.full(
            len(c), d - 1), np.full(len(c), True)))
        # m = list(map(Etat.alphabeta, c, np.full(len(c),float("-inf")), np.full(len(c),1), np.full(len(c), d - 1), np.full(len(c), True)))
        print(m)
        print(np.argmax(m))
        print(t)
        return t[np.argmax(m)]

    def get_best_moves1(self, d):
        best_move = np.array([], dtype=deplacement.Move)
        best_value = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        ass = ia.IA(self.joueur)
        t = self.get_moves()
        for action in t:
            next_state = self.play(action)
            value1 = ass.alphabeta(next_state, alpha, 1, d, True)
            alpha = max(alpha, value1)
            if alpha >= beta:
                return action
            else:
                beta = min(beta, 1 - alpha)

            if value1 > best_value:
                best_value = value1
                best_move = action

        return best_move


if __name__ == '__main__':
    et = Etat()
    et.afficher()
    # o = np.array([[0,0], [6, 6]])
    # y = np.array(list(map(et.select_pion, o))).reshape((-1, 2))
    
    t = et.select_pion([0,6])
    m = np.tile([0,6], (len(t), 1))
    print(m)
    res = list(map(Move, m, t))
    print(res)

    # ou = list(map(et.select_pion, o))
    print(et.get_moves(0))
    # print(Etat.minimax(et, 3, True))
