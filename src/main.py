#coding:utf-8

from decision_tree import *
from math import log2

"""
    Renvoie une liste de bits représentant la décomposition en base 2 de l’entier x,
    telle que les bits de poids les plus faibles soient présentés en tête de liste
"""
def decomposition(x):
    if x <= 0:
        return []
    else:
        return [bool(x % 2)] + decomposition(x // 2)

"""
    Renvoie soit la liste tronquée ne contenant que les n premiers éléments de l, soit la liste complétée à droite
    par des valeurs False, de taille n
"""
def completion(l, n):
    if n <= len(l):
        return l[0 : n]
    else:
        return l + ([False] * (n - len(l)))

"""
    Décompose x en base 2 et complète la liste obtenue afin qu’elle soit de taille n
"""
def table(x, n):
    return completion(decomposition(x), n)

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

def is_power_of_2(x):
    if x == 1:
        return True
    if x < 1:
        return False
    return is_power_of_2(x / 2)

index_build_tree = 0

def rec_build_tree(l, t, level_max, current_level):
    global index_build_tree
    if current_level < level_max - 1:
        t.insert_left("x" + str(level_max - current_level - 1))
        t.insert_right("x" + str(level_max - current_level - 1))
        rec_build_tree(l, t.left, level_max, current_level + 1)
        rec_build_tree(l, t.right, level_max, current_level + 1)
    else:
        t.insert_left(str(l[index_build_tree]))
        t.insert_right(str(l[index_build_tree + 1]))
        index_build_tree += 2

def build_tree(l):
    while is_power_of_2(len(l)) == False:
        l += [False]
    logarithm_binary = int(log2(len(l)))
    t = DecisionTree("x" + str(logarithm_binary))
    index_build_tree = 0
    rec_build_tree(l, t, logarithm_binary, 0)
    return t

#en developpement
def luka(t):
    return "(" + t.label + luka(t.left) + luka(t.right) + ")"

if __name__ == "__main__":
    test_decomposition()
    test_completion()
    test_table()
    test_power_of_2()

print(build_tree(table(38, 8)))