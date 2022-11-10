import numpy as np


class Move:

    def __init__(self, pion: np.ndarray, action: tuple) -> None:
        self.pion = pion
        self.action = action

    def __eq__(self, other):
        return (other.pion == self.pion and other.action == self.action) if isinstance(other, Move) else False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self == None and other == None:
            return True
        return (other.action > self.action and np.all(other.pion > self.pion)) if isinstance(other, Move) else False

    def __gt__(self, other):
        return not self.__lt__(other)

    def cloner_a_droite(self):
        return self.pion + np.array((0, 1)), self.pion[1] != 6

    def cloner_a_gauche(self):
        return self.pion + np.array((0, -1)), self.pion[1] != 0

    def cloner_en_haut(self):
        return self.pion + np.array((-1, 0)), self.pion[0] != 0

    def cloner_en_bas(self):
        return self.pion + np.array((1, 0)), self.pion[0] != 6

    def sauter_a_droite(self):
        return self.pion + np.array((0, 2)), self.pion[1] < 5

    def sauter_a_gauche(self):
        return self.pion + np.array((0, -2)), self.pion[1] > 1

    def sauter_en_haut(self):
        return self.pion + np.array((-2, 0)), self.pion[0] > 1

    def sauter_en_bas(self):
        return self.pion + np.array((2, 0)), self.pion[0] < 5

    def do_move(self):
        dico = {("d", "1"): self.cloner_a_droite(), ("g", "1"): self.cloner_a_gauche(),
                ("h", "1"): self.cloner_en_haut(),
                ("b", "1"): self.cloner_en_bas(), ("d", "2"): self.sauter_a_droite(),
                ("g", "2"): self.sauter_a_gauche(),
                ("h", "2"): self.sauter_en_haut(), ("b", "2"): self.sauter_en_bas()
                }
        return dico[self.action][0] if dico[self.action][1] else None

    def __repr__(self):
        return f"[{self.pion}, {self.action}]"

    # def __str__(self):
      #   return f"[{self.pion}, {self.action}]"

    def get_type_mouvement(self):
        return self.action[1]

    def get_pion(self):
        return self.pion

    def __str__(self) -> str:
        res = f"Le pion situé à la position: {self.pion} effectue le mouvement: {self.action}. "
        res += "Le mouvement est possible" if self.do_move() is not None else " Le mouvement n'est pas possible"
        return res

    @staticmethod
    def cases_adjacente(pion: np.ndarray) -> np.ndarray:
        deplacement = np.array(np.meshgrid(
            [-1, 0, 1], [-1, 0, 1])).T.reshape(-1, 2)
        deplacement = np.delete(deplacement, (4), axis=0)
        adjacent = deplacement + pion
        adjacent = np.delete(
            adjacent, (np.argwhere(adjacent < 0)[:, 0]), axis=0)
        adjacent = np.delete(
            adjacent, (np.argwhere(adjacent > 6)[:, 0]), axis=0)
        return adjacent


if __name__ == "__main__":
    mouvement = Move([1, 0], ("d", "1"))
    print(mouvement)
    print(mouvement.do_move())
