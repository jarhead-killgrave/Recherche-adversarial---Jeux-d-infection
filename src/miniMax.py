from algo import Algorithm

import numpy as np

class MiniMax(Algorithm):

    def __init__(self, joueur: int, profondeur: int):
        super().__init__(joueur, profondeur)
    
    def minimax(self, si, profondeur: int) -> float:
        super().incremente_noeud()
        if profondeur == 0 or si.is_over():
            return si.getScore(self.joueur)
        
        else:
            if self.joueur == si.joueur:
                t = si.get_moves()
                sj = np.vectorize(si.play)(t)
                liste_mini_max = np.vectorize(self.minimax)(sj, profondeur -1)
                b = max(liste_mini_max)

            else:
                t = si.get_moves()
                sj = list(map(si.play, t))
                liste_mini_max = np.vectorize(self.minimax)(sj, profondeur -1)
                b = min(liste_mini_max)    
            return b
        
    

    def get_best_moves(self, s):

        best_moves = None
        best_value = float("-inf")
        all_move = s.get_moves()
        all_move = all_move[np.random.permutation(len(all_move))]
        print(all_move)
        for m in all_move:
            etat = s.play(m)
            value = self.minimax(etat, self.profondeur)
            if value > best_value:
                best_value = value
                best_moves = m
        return best_moves

