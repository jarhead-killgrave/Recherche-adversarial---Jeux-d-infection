from algo import Algorithm

import numpy as np

class AlphaBeta(Algorithm):

    def __init__(self, joueur, profondeur):
        super().__init__(joueur, profondeur)
    
    def alphaBeta(self, si, alpha, beta, profondeur):
        super().incremente_noeud()
        if profondeur == 0 or si.is_over():
            return si.getScore(self.joueur)

        else:

            if self.joueur == si.joueur:
                t = si.get_moves()
                next_state = list(map(si.play, t))
                for sj in next_state:
                    alpha = max(alpha, self.alphaBeta(
                        sj, alpha, beta, profondeur - 1))
                    if alpha >= beta:
                        return alpha
                return alpha
            else:
                t = si.get_moves()
                next_state = list(map(si.play, t))
                for sj in next_state:
                    beta = min(beta, self.alphaBeta(
                        sj, alpha, beta, profondeur-1))
                    if alpha >= beta:
                        return beta
                return beta
    

    def get_best_moves(self, etat):
        best_moves = None
        alpha = float("-inf")
        beta = 1
        all_move = etat.get_moves()
        all_move = all_move[np.random.permutation(len(all_move))]
        print(all_move)
        for m in all_move:
            next_etat = etat.play(m)
            value = max(alpha, self.alphaBeta(next_etat, alpha, beta, self.profondeur))
            if  value > alpha:
                alpha = value
                best_moves = m
            
            if alpha > beta:
                break
        return best_moves