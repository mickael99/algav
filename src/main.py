#coding:utf-8

from decision_tree import *
from math import log2
import graphviz

"""
    Renvoie une liste de bits représentant la décomposition en base 2 de l’entier x,
    telle que les bits de poids les plus faibles soient présentés en tête de liste
    
    x(int) -> l'entier à décomposer
    
    return(list de boolean) -> la décomposition en base 2 
"""
def decomposition(x):
    if x <= 0:
        return []
    else:
        return [bool(x % 2)] + decomposition(x // 2)

"""
    Renvoie soit la liste tronquée ne contenant que les n premiers éléments de l, soit la liste complétée à droite
    par des valeurs False, de taille n
    
    l(liste) -> la liste 
    n -> la taille de la liste à la sortie
    
    return(liste de boolean) -> la nouvelle liste
"""
def completion(l, n):
    if n <= len(l):
        return l[0 : n]
    else:
        return l + ([False] * (n - len(l)))

"""
    Décompose x en base 2 et complète la liste obtenue afin qu’elle soit de taille n
    
    x(int) -> l'entier à décomposer
    n -> la taille de la liste à la sortie de la fonction
    
    return(liste de boolean) -> décomposition de l'entier x de taille n (complété avec des False)
"""
def table(x, n):
    return completion(decomposition(x), n)

"""
    Renvoie vrai si x est une puissance de 2, faux sinon
    
    x(entier) -> l'entier
    
    return(bool) -> Vrai si puissance de 2, faux sinon 
"""
def is_power_of_2(x):
    if x == 1:
        return True
    if x < 1:
        return False
    return is_power_of_2(x / 2)

"""
    Construit un arbre de décision à partir d'une liste (on suppose que cette liste n'a pas forcément une taille 
    qui est une puissance de 2, de ce fait, on corrige cette potentielle erreur)
    
    l(list de bool) -> la liste qui permet de construire l'arbre
    
    return(DecisionTree) -> l'arbre de décision résultant
"""
def build_tree(l):
    def rec_build_tree(l):
        log_binary = int(log2(len(l)))
        if len(l) == 2:
            return DecisionTree("x" + str(log_binary), DecisionTree(str(l[0])), DecisionTree(str(l[1])))
        slice_list = len(l) // 2
        return DecisionTree("x" + str(log_binary), rec_build_tree(l[:slice_list]), rec_build_tree(l[slice_list:]))
    while is_power_of_2(len(l)) == False:
        l += [False]
    return rec_build_tree(l)

"""
    Associe un mot Luka à chaque noeud de l'arbre de décision non compréssé
    
    t(DecisionTree) -> arbre de décision
    
    return(DecisionTree) -> l'arbre de décision tel que chaque noeud soit associé à son mot Luka
"""
def luka(t):
    if t == None:
        return
    if t.left != None:
        luka(t.left)
    if t.right != None:
        luka(t.right)
    if t.label != "False" and t.label != "True":
        t.luka_v = t.label + "(" + t.left.luka_v + ")" + "(" + t.right.luka_v + ")"
    else:
        t.luka_v = t.label
    return t

"""
    Compresse l'arbre de decision
    
    t(DecisionTree) -> l'arbre à comprésser
    
    return(DecisionTree) -> l'arbre compréssé
"""
def compression(t):
    """
        On utilise un dictionnaire pour pouvoir stocker les noeuds dans ce dernier et ainsi fusionner les noeuds
        avec un mot Luka similaire
    """
    def rec_compression(t, d):
        res_t = d.get(t.luka_v)
        #si le noeud n'est pas dans le dictionnaire, alors on l'ajoute
        if res_t == None:
            d[t.luka_v] = t
            #si c'est une feuille alors on renvoie cette dernière, sinon on continue à parcourir l'arbre
            if t.label != "False" and t.label != "True":
                t.left = rec_compression(t.left, d)
                t.right = rec_compression(t.right, d)
            return t
        else:
            return res_t

    return rec_compression(t, {})

"""
    Associe un identifiant unique à chaque noeud de l'arbre
    
    t(DecisionTree) -> arbre de décision
"""
def associate_id(t):
    """
        t(DecisionTree) -> l'arbre de décision
        i(int) -> l'identifiant
        l(liste int) -> contient les identifiants déjà utilisés
    """
    def rec_associate_id(t, i, l):
        while i in l:
            i += 1
        l += [i]
        t.id = i
        #t n'est pas une feuille
        if t.left and t.right:
            rec_associate_id(t.left, i + 1, l)
            rec_associate_id(t.right, i + 1, l)
    rec_associate_id(t, 0, [])

"""
    Créé un fichier dot à partir d'un arbre
    
    t(Decisiontree) -> l'arbre de décision
"""
#def create_dot(t):

"""

    FONCTIONS DE TEST
    
"""
def test_decomposition():
    try:
        assert [False, True, True, False, False, True] == decomposition(38)
        assert [] == decomposition(-7)
        assert [True, True, False, True, True] == decomposition(27)
    except AssertionError:
        print("Problème dans la fonction \"decomposition\"")

def test_completion():
    try:
        assert [False, True, True, False] == completion([False, True, True, False, False, True], 4)
        assert [False, True, True, False, False, True, False, False] == completion([False, True, True, False, False, True], 8)
    except AssertionError:
        print("Problème dans la fonction \"completion\"")

def test_table():
    try:
        assert [False, True, True, False] == table(38, 4)
        assert [False, True, True, False, False, True, False, False] == table(38, 8)
    except AssertionError:
        print("Problème dans la fonction \"table\"")

def test_power_of_2():
    try:
        assert True == is_power_of_2(64)
        assert True == is_power_of_2(128)
        assert True == is_power_of_2(4)
        assert False == is_power_of_2(60)
        assert False == is_power_of_2(100)
        assert False == is_power_of_2(70)
    except AssertionError:
        print("Problème dans la fonction puissance de 2")


def test_build_tree():
    try:
        assert build_tree(table(38, 8)).__str__() == "(x3, (x2, (x1, (False, None, None), (True, None, None)), (x1, (True, None, None), (False, None, None))), (x2, (x1, (False, None, None), (True, None, None)), (x1, (False, None, None), (False, None, None))))"
    except AssertionError:
        print("Problème dans la fonction qui construit un arbre de décision non compréssé à partir d'une liste")

def test_luka():
    try:
        t = luka(build_tree(table(38, 8)))
        assert t.luka_v == "x3(x2(x1(False)(True))(x1(True)(False)))(x2(x1(False)(True))(x1(False)(False)))"
    except:
        print("Problème dans la fonction qui construit un mot Luka")

if __name__ == "__main__":
    test_decomposition()
    test_completion()
    test_table()
    test_power_of_2()
    test_build_tree()
    test_luka()

