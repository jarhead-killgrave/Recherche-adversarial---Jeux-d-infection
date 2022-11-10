import numpy as np
import time
import itertools as it

class IA:

    def __init__(self, joueur: int) -> None:
        self.joueur = joueur
        self.noeud_visite = 0

    def minimax(self, si, d: int, maxi: bool):

        if d == 0 or si.is_over():
            return si.getScore(self.joueur)

        t = si.get_moves()
        sj = np.vectorize(si.play)(t)
        # sj = list(map(si.play, t))
        # m = list(map(self.minimax, sj, it.repeat(d-1), it.repeat(not maxi)))
        m = np.vectorize(self.minimax)(sj, d-1, not maxi)

        return np.max(m) if maxi else np.min(m)

    # def minimax(self, si, d: int, maxi: bool):

    #     if d == 0 or si.is_over():
    #         return si.getScore(self.joueur)
        
    #     else:
    #         if maxi:
    #             t = si.get_moves()
    #             sj = np.array(list(map(si.play, t))).reshape(-1)
    #             b = float("-inf")
    #             for s in sj:
    #                 m = self.minimax(s, d-1, False)
    #                 b = max(b, m)
    #         else:
    #             b = float("+inf")
    #             t = si.get_moves()
    #             sj = np.array(list(map(si.play, t))).reshape(-1)
    #             for s in sj:
    #                 m = self.minimax(s, d-1, True)
    #                 b = min(b, m)
            
    #         return b




    def alphabeta(self, si, alpha, beta, d, maxi: bool):

        if d == 0 or si.is_over():
            return si.getScore(self.joueur)

        else:

            if maxi:
                t = si.get_moves()
                next_state = np.array(list(map(si.play, t)))
                for sj in next_state:
                    alpha = max(alpha, self.alphabeta(
                        sj, alpha, beta, d - 1, False))
                    if alpha >= beta:
                        return alpha
                return alpha
            else:
                t = si.get_moves()
                next_state = np.array(list(map(si.play, t))).reshape(-1)
                for sj in next_state:
                    beta = min(beta, self.alphabeta(
                        sj, alpha, beta, d-1, True))
                    if alpha >= beta:
                        return beta
                return beta
    
    def get_best_moves(self, s, d: int):

        t = s.get_moves(self.joueur)
        c = list(map(s.play, t))

        m = np.vectorize(self.minimax)(c, d, True)
        # m = func(c, d, True)
        # m = list(map(self.minimax, c, it.repeat(d), it.repeat(True)))
        # m = list(map(Etat.alphabeta, c, np.full(len(c),float("-inf")), np.full(len(c),1), np.full(len(c), d - 1), np.full(len(c), True)))
        print(m)
        print(np.argmax(m))
        print(t)
        return t[np.argmax(m)]
    
    def get_best_moves1(self, s, d: int):

        t = s.get_moves(self.joueur)
        c = list(map(s.play, t))

        # m = np.vectorize(self.minimax)(c, d, True)
        # m = func(c, d, True)
        # m = list(map(self.minimax, c, it.repeat(d), it.repeat(True)))
        m = list(map(self.alphabeta, c, it.repeat(float("-inf")), it.repeat(1), it.repeat(d), it.repeat(True)))
        print(m)
        print(np.argmax(m))
        print(t)
        return t[np.argmax(m)]
