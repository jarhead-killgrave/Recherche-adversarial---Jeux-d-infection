import numpy as np

taille_max = 6
taille_min = 0
tab_direction = np.array([[[-1, -1],
                           [-2, -2]],

                          [[-1,  0],
                           [-2,  0]],

                          [[-1,  1],
                           [-2,  2]],

                          [[0, -1],
                           [0, -2]],

                          [[0,  1],
                           [0,  2]],

                          [[1, -1],
                           [2, -2]],

                          [[1,  0],
                           [2,  0]],

                          [[1,  1],
                           [2,  2]]])


class Move:

    def __init__(self, pion: np.ndarray, direction: np.ndarray = np.array([])):
        """
            Initialise un nouvelle instance de deplacement d'un pion

            :param pion: un pion est un couple de (x, y) stocké dans un tableau
            :param direction: c'est la direction dans laquelle le pion doit se deplacer
                une direction est representé par 2 valeur:\n
                    - la direction de deplacement {0: haut-gauche, 1: haut, 2: haut-droit, 3: gauche, 4: droite, 5: bas-gauche, 6: bas, 7: bas-droit}
                    - le type de deplacement {0: clonage, 1: saut}
        """

        self.pion = pion
        self.direction = direction

    def __repr__(self) -> str:
        return f"Move(pion={self.pion}, direction={self.direction})"

    def __str__(self) -> str:
        return f"Le pion {self.pion} tente le deplacement {self.direction}"

    def __eq__(self, __o: object) -> bool:
        return (self.direction[1] == 0 and __o.direction[1] == 0) and np.all(self.prochaine_case()[0] == __o.prochaine_case()[0]) if isinstance(__o, Move) else False

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __lt__(self, __o: object) -> bool:
        if self == None or __o == None:
            return False
        return (np.all(self.pion < __o.pion) and np.all(self.direction < __o.direction)) if isinstance(__o, Move) else False

    def __le__(self, __o: object) -> bool:
        return self.__lt__(__o) or self.__eq__(__o)

    def __gt__(self, __o: object) -> bool:
        return not self.__lt__(__o)

    def __ge__(self, __o: object) -> bool:
        return self.__lt__(__o) or self.__eq__(__o)

    def prochaine_case(self, direction=None) -> tuple:
        """
            Renvoie la prochaine case dû au deplacement avec direction et verifie si le mouvement est logiquement possible

            :param direction: la direction de deplacement(par défaut elle est égale à la direction initiale)
        """
        if direction is None:
            direction = self.direction
        new_pion = self.pion + tab_direction[direction[0], direction[1]]
        return self.pion + tab_direction[direction[0], direction[1]], np.all(new_pion >= taille_min) and np.all(new_pion <= taille_max)

    @staticmethod
    def cases_adjacentes(pion: np.ndarray) -> np.ndarray:
        """
            Renvoie la liste de toutes les cases adjancentes possibles
        """
        tmp = np.array(np.meshgrid([-1, 0, 1], [-1, 0, 1])).T.reshape(-1, 2)
        tmp = np.delete(tmp, 4, axis=0)
        res = tmp + pion
        res = np.delete(res, (np.argwhere(res < taille_min)[:, 0]), axis=0)
        res = np.delete(res, (np.argwhere(res > taille_max)[:, 0]), axis=0)
        return res


if __name__ == '__main__':

    a = Move(np.array([0, 0]), np.array([2, 0]))
    action = np.array(np.meshgrid(np.arange(8), [0, 1])).T.reshape(-1, 2)
    tmp = np.array(list(map(a.prochaine_case, action)))
    test = np.arange(49).reshape(7, 7)
    # l = list(map(tuple, tmp[:,0][:]))
    print(tmp)
    print(len(action))
    print(len(tmp))
    indice = np.argwhere(tmp[:, 1] == True)[:, 0]

    print(tmp[indice][:, 0])
    print(list(map(lambda x: test[tuple(x)] % 2 == 0, tmp[indice, 0])))
    print(test)
    # print(test[(2, 0), (1, 1), (2, 2)])
    print(action[(tmp[:, 1] == True)])
    a = list(map(Move, np.tile(np.array([0, 0]), (6, 1)), action))
    print(a)
