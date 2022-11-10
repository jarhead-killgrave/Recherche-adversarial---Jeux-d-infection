import numpy as np

import move

import sys

GRILLE_INITIALE = np.full((7, 7), -1, dtype=np.int8)
GRILLE_INITIALE[[-1, 0], [0, -1]] = 0
GRILLE_INITIALE[[0, -1], [0, -1]] = 1
combinaison_action = np.array(np.meshgrid(["d", "g", "h", "b"], ["1", "2"])).T.reshape((-1, 2))
combinaison_action1 = list(map(tuple, combinaison_action))
deplacement = np.array(np.meshgrid([-1, 0, 1], [-1, 0, 1])).T.reshape(-1, 2)
deplacement  = np.delete(deplacement, 4, axis=0)





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

    def __str__(self) -> str:
        return str(self.grille) + "\nLe joueur actif est le joueur " + str(
            self.joueur)

    def update(self):
        return np.hstack((self.etats_precedent, self))

    def afficher(self) -> None:
        print("C'est le tour du joueur ", self.joueur)
        for ligne in self.grille:
            for colonne in ligne:
                if colonne in (1, 0):
                    print(f" {colonne} |", end="")
                else:
                    print(f"{colonne} |", end="")
            print("\n")

    def get_grille(self) -> np.ndarray:
        return self.grille

    def get_joueur(self):
        return self.joueur

    @staticmethod
    def adjacents1(x: int, y: int) -> np.ndarray:
        adjacent = deplacement + np.array((x, y))
        adjacent = np.delete(adjacent, (np.argwhere(adjacent < 0)[:, 0]), axis=0)
        adjacent = np.delete(adjacent, (np.argwhere(adjacent > 6)[:, 0]), axis=0)
        return adjacent

    @staticmethod
    def adjancents(pion: np.ndarray) -> np.ndarray:
        return Etat.adjacents1(pion[0], pion[1])

    @staticmethod
    def move_pion(x: int, y: int) -> np.ndarray:
        pion = np.array((x, y))
        t_a = list(map(move.Move, np.tile(pion, (10,1)), combinaison_action1))
        return t_a


    def select_pion(self, pion: np.ndarray) -> np.ndarray:
        mouvement_possible = Etat.move_pion(pion[0], pion[1])
        res = np.array([None], dtype=move.Move)
        for mvt in mouvement_possible:
            pion = mvt.do_move()
            if pion is not None and self.grille[tuple(pion)] == -1:
                res = np.hstack((res, mvt))
        return res

    def is_over(self):
        return (np.sum(self.grille == -1) == 0) or (np.sum(self.grille == 0) == 0) or (
                np.sum(self.grille == 1) == 0) or (np.sum(self.etats_precedent == self) >= 2)

    def get_moves(self, joueur: int = None) -> np.ndarray:
        if joueur is None:

            joueur = self.joueur

        all_pion = np.argwhere(self.grille == joueur)

        res = np.array([], dtype=move.Move)

        for pion in all_pion:

            all_move = self.select_pion(pion)

            res = np.hstack((res, all_move))

        return res


    def getScore(self, joueur=None):
        if joueur is None:
            joueur = self.joueur
        nj = np.sum(self.grille == joueur)
        nt = np.sum(self.grille == 0) + np.sum(self.grille == 1)
        return nj / nt


    def play(self, coup: move.Move):
        new_joueur = (self.joueur + 1) % 2
        new_grille = np.copy(self.grille)
        if coup is None or np.all(coup.do_move() == None):
            return Etat(new_grille, new_joueur, self.update())
        new_pion = coup.do_move()
        new_grille[tuple(new_pion)] = self.joueur
        if coup.get_type_mouvement() == "2":
            new_grille[tuple(coup.get_pion())] = -1
            
        for pion in Etat.adjancents(new_pion):
            if new_grille[tuple(pion)] != -1:
                new_grille[tuple(pion)] = self.joueur
        return Etat(new_grille, new_joueur, self.update())
    
    @staticmethod
    def minimax(si, d: int, maxi: bool):

        if d == 0 or si.is_over():
            return si.getScore(0)

        t = si.get_moves()
        c = np.array(list(map(si.play, t))).reshape(-1)
        m = list(map(Etat.minimax, c, np.full(len(c), d - 1), np.full(len(c), not maxi)))

        return np.max(m) if maxi else np.min(m)

    # @staticmethod
    # def alphabeta(si, alpha, beta, d, maxi: bool):

    #     if d == 0 or si.is_over():
    #         return si.getScore(0)
        
    #     if maxi == True:
    #         if alpha >= beta:
    #             return alpha
    #         t = si.get_moves()
    #         taille = len(t)
    #         a = np.min(list(map(Etat.alphabeta, t, np.full(taille, alpha), np.full(taille, beta), np.full(taille, d - 1), np.full(taille, False))))
    #         alpha = max(alpha, a)
    #         return alpha
        
    #     else:
    #         if alpha >= beta:
    #             return beta
    #         t = si.get_moves()
    #         taille = len(t)
    #         b = np.max(list(map(Etat.alphabeta, t, np.full(taille, alpha), np.full(taille, beta), np.full(taille, d - 1), np.full(taille, False))))
    #         beta = min(beta, b)
    #         return beta

            



    @staticmethod
    def alphabeta(si, alpha, beta, d, maxi: bool):
        
        if d == 0 or si.is_over():
            return si.getScore()
        
        else:
            
            if maxi:
                t = si.get_moves()
                next_state = np.array(list(map(si.play, t))).reshape(-1)
                for sj in next_state:
                    alpha = max(alpha, Etat.alphabeta(sj, alpha, beta, d - 1, False))
                    if alpha >= beta:
                        return alpha
                return alpha
            else:
                t = si.get_moves()
                next_state = np.array(list(map(si.play, t))).reshape(-1)
                for sj in next_state:
                    beta = min(beta, Etat.alphabeta(sj, alpha, beta, d-1, True))
                    if alpha >= beta:
                        return beta
                return beta
        

    def get_best_moves(self, d):
        t = self.get_moves()
        c = np.array(list(map(self.play, t))).reshape(-1)
        m = list(map(Etat.minimax, c, np.full(len(c), d - 1), np.full(len(c), True)))
        # m = list(map(Etat.alphabeta, c, np.full(len(c),float("-inf")), np.full(len(c),1), np.full(len(c), d - 1), np.full(len(c), True)))
        return t[np.argmax(m)]
    
    def get_best_moves1(self, d):
        best_move = np.array([], dtype=move.Move)
        best_value = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        t = self.get_moves(0)
        for action in t:
            next_state = self.play(action)
            value1= Etat.alphabeta(next_state, alpha, 1, d, True)
            alpha = max(alpha, value1)
            if alpha >= beta:
                return action
            
            if value1 >best_value:
                best_value = value1
                best_move = action
        
        return best_move

            
            
            



            

                

