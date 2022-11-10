from state import State
import numpy as np
from etat import Etat

def numero_case(x,y):
    return x * 7 + y

if __name__ == '__main__':

    #etat = State()
    etat = Etat()
    print(etat.get_moves())
    etat.afficher()
    for _ in range(1000):
        #a = etat.getMoves()
        a = etat.get_moves()
        mvt = None

        if etat.get_joueur() == 1 and len(a) > 0:
            #mvt = np.random.choice(a)
            mvt = None
        else:
            dico = {k: v for k, v in zip(range(len(a)), a)}
            print(dico)
            choix = int(input("veuillez selectionner le mouvement souhaité: "))
            if choix in dico:
                mvt = dico[choix]
        etat = etat.play(mvt)
        print(mvt)
        etat.afficher()
        if etat.is_over():
            break
    print(f"le score du joueur 0 est {etat.getScore(0)} et le score du joueur 1 est {etat.getScore(1)}")
