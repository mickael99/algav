#coding:utf-8

"""
    Renvoie une liste de bits représentant la décomposition en base 2 de l’entier x,
    telle que les bits de poids les plus faibles soient présentés en tête de liste
"""
def decomposition(n):
    if n <= 0:
        return []
    else:
        return [bool(n % 2)] + decomposition(n / 2)

"""
    Renvoie soit la liste tronquée ne contenant que ses n premiers éléments, soit la liste complétée à droite
    par des valeurs False, de taille n
"""
def completion(l, n):
    if n <= len(l):
        return l[0 : n]
    else:
        return l + ([False] * (n - len(l)))

"""
    Déecompose x en base 2 et complète la liste obtenue afin qu’elle soit de taille n
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

if __name__ == "__main__":
    test_decomposition()
    test_completion()
    test_table()