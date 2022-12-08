#coding:utf-8

from decision_tree import *
from experimentation import *
from copy import deepcopy
from math import log2
import os
import sys
import subprocess
import time
from random import randint

sys.setrecursionlimit(10**6)

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
    if t.luka_v == "":
        luka(t)
    t = rec_compression(t, {})
    associate_id(t)
    return t

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
    Créé une liste contenant toutes les adresses des noeuds d'un arbre de décision
    
    t(DecisionTree) -> arbre de décision 
    
    return(liste liste) -> la listes contenant les noeuds
"""
def create_list_from_decision_tree(t):
    def rec_create_list_from_decision_tree(t, l):
        if t == None:
            return None
        if [t, t.left, t.right] not in l:
            l.append([t, t.left, t.right])
        rec_create_list_from_decision_tree(t.left, l)
        rec_create_list_from_decision_tree(t.right, l)
    l = []
    rec_create_list_from_decision_tree(t, l)
    return l

"""
    Créé un fichier dot et un fichier png à partir d'un arbre 
    
    t(Decisiontree) -> l'arbre de décision
    file_name(string) -> le nom du fichier
"""
def create_dot(t, file_name):
    if t.id == -1:
        associate_id(t)

    #création du dossier dot où sera stocké le fichier de sortie
    if not os.path.exists("../dot"):
        os.mkdir("../dot")

    #récupération de la liste des noeuds de l'arbre
    l = create_list_from_decision_tree(t)

    #écriture dans le fichier
    f = open("../dot/" + file_name + ".dot","w")
    f.write("graph {\n")

    for node in l:
        if node[0].label != "False" and node[0].label != "True":
            f.write("\t" + str(node[0].id) + "[label = \"" + str(node[0].label) + "\"];\n")
            f.write("\t" + str(node[1].id) + "[label = \"" + str(node[1].label) + "\";]\n")
            f.write("\t" + str(node[2].id) + "[label = \"" + str(node[2].label) + "\";]\n")
            f.write("\t" + str(node[0].id) + " -- " + str(node[1].id) + "[ style=dashed  ];\n")
            f.write("\t" + str(node[0].id) + " -- " + str(node[2].id) + "[ style=solid  ];\n")
    f.write("}")

    f.close()

    #créer le fichier "tree.png" qui affiche l'arbre
    subprocess.run("dot -Tpng ../dot/" + file_name + ".dot" + " -o ../dot/" + file_name + ".png")

"""
    Compresse un arbre en robdd unique 
    
    t(DecisionTree) -> l'arbre à comprésser
    
    return(DecisionTree) -> l'arbre Robdd résultant
"""
def compress_bdd(t):
    def rec_compress_bdd(t):
        #si t est une feuille
        if t.label == "True" or t.label == "False":
            return t
        #si t n'est pas une feuille
        t.left = rec_compress_bdd(t.left)
        t.right = rec_compress_bdd(t.right)
        if t.left.id == t.right.id:
            return t.right
        return t
    if t.luka_v == "":
        luka(t)
    t = compression(t)
    return rec_compress_bdd(t)



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

def test_size():
    try:
        t = build_tree(table(38, 8))
        t2 = compress_bdd(deepcopy(t))
        assert t.size() == 15
        assert t2.size() == 7
    except:
        print("Problème dans la fonction size")

"""
    FONCTIONS DE DESSINS D'ARBRE
"""

def create_classic_tree_png():
    t = build_tree(table(38, 8))
    create_dot(t, "classic_tree")
    print("le fichier dot/classic_tree.png a bien ete cree, vous pouvez des a present l'ouvir")

def create_compress_tree_png():
    t = build_tree(table(38, 8))
    t = compression(t)
    create_dot(t, "compress_tree")
    print("le fichier dot/compress_tree.png a bien ete cree, vous pouvez des a present l'ouvir")

def create_compress_bdd_tree_png():
    t = build_tree(table(38, 8))
    t = compress_bdd(t)
    create_dot(t, "compress_bdd_tree")
    print("le fichier dot/compress_bdd_tree.png a bien ete cree, vous pouvez des a présent l'ouvir")

"""

    FONCTION DE DESSINS DES GRAPHIQUES

"""

"""
    Trie un dictionnaire en fonction de la valeur des clés 
    
    d(dict) -> le dictionnaire à trier
    
    return(dict) -> le dictionnaire trié
"""
def sorted_dic(d):
    keys = list(d.keys())
    keys = sorted(keys)
    sorted_d = {}

    for key in keys:
        sorted_d[key] = d[key]

    return sorted_d

"""
     Créer un dictionnaire qui contient (point abscice: point ordonné)
     
     n(int) -> nombre de variables
     
     return(int, int) -> (valeurs de l'axe des absices, valeurs de l'axe des ordonnés)
"""
def create_graphic_point(n):
    #Création de tous les arbre possibles pour 1 seul variable -> x1
    #le nombre de noeud dans un arbre compréssé BDD vaut le nombre de fonction booléennes possibles
    trees = []
    graphic_point = {}
    n = pow(2, n)
    nb_possibility = pow(2, n)

    if n >= pow(2, 5):
        for i in range(pow(2, 16)):
            rand_number = randint(0, nb_possibility)
            trees.append(build_tree(table(rand_number, n)))
            trees[i] = compress_bdd(trees[i])
            size_tree = trees[i].size()
            if size_tree in graphic_point:
                graphic_point[size_tree] += 1
            else:
                graphic_point[size_tree] = 1
        graphic_point = sorted_dic(graphic_point)
    else:
        for i in range(0, nb_possibility):
            trees.append(build_tree(table(i, n)))
            trees[i] = compress_bdd(trees[i])
            size_tree = trees[i].size()
            if size_tree in graphic_point:
                graphic_point[size_tree] += 1
            else:
                graphic_point[size_tree] = 1
        graphic_point = sorted_dic(graphic_point)

    print(graphic_point)
    return graphic_point.keys(), graphic_point.values()

"""
   Créer un graphique pour 1 variable
"""
def create_graphic_for_1_var():
    keys, values = create_graphic_point(1)

    plt.plot(list(keys), list(values), "b-o")
    plt.xlabel("ROBDD node count for 1 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 4, 0, 4])
    plt.show()

"""
   Créer un graphique pour 2 variable
"""
def create_graphic_for_2_var():
    keys, values = create_graphic_point(2)

    plt.plot(list(keys), list(values), "b-o")
    plt.xlabel("ROBDD node count for 2 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 6, 0, 9])
    plt.show()

"""
   Créer un graphique pour 3 variable
"""
def create_graphic_for_3_var():
    keys, values = create_graphic_point(3)

    plt.plot(list(keys), list(values), "b-o")
    plt.xlabel("ROBDD node count for 3 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 8, 0, 100])
    plt.show()

"""
   Créer un graphique pour 4 variable
"""
def create_graphic_for_4_var():
    keys, values = create_graphic_point(4)

    plt.plot(list(keys), list(values), "b-o")
    plt.xlabel("ROBDD node count for 4 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 13, -500, 2.5 * pow(10, 4)])
    plt.show()

"""
   Créer un graphique pour 5 variable
"""
def create_graphic_for_5_var():
    keys, values = create_graphic_point(5)

    plt.plot(list(keys), list(values), "b-o")
    plt.xlabel("ROBDD node count for 5 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 25, -500, 20000])
    plt.show()


"""
   Créer un graphique pour 6 variable
"""
def create_graphic_for_6_var():
    keys, values = create_graphic_point(6)

    plt.plot(list(keys), list(values), "b-o")
    plt.xlabel("ROBDD node count for 6 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([15, 35, -500, 20000])
    plt.show()

"""
   Créer un graphique pour 7 variable
"""
def create_graphic_for_7_var():
    keys, values = create_graphic_point(7)

    plt.plot(list(keys), list(values), "b-o")
    plt.xlabel("ROBDD node count for 7 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 50, -500, 20000])
    plt.show()

"""
   Créer un graphique pour 8 variable
"""
def create_graphic_for_8_var():
    keys, values = create_graphic_point(8)

    plt.plot(list(keys), list(values), "b-o")
    plt.xlabel("ROBDD node count for 8 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 90, -500, 20000])
    plt.show()

"""
   Créer un graphique pour 9 variable
"""
def create_graphic_for_9_var():
    keys, values = create_graphic_point(9)

    plt.plot(list(keys), list(values), "b-o")
    plt.xlabel("ROBDD node count for 9 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 150, -500, 20000])
    plt.show()

"""
   Créer un graphique pour 10 variable
"""
def create_graphic_for_10_var():
    keys, values = create_graphic_point(10)

    plt.plot(list(keys), list(values), "b-o")
    plt.xlabel("ROBDD node count for 10 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 300, -500, 20000])
    plt.show()

if __name__ == "__main__":
    begin = time.process_time()
    test_decomposition()
    test_completion()
    test_table()
    test_power_of_2()
    test_build_tree()
    test_luka()
    test_size()

    #create_graphic_for_1_var()
    #create_graphic_for_2_var()
    #create_graphic_for_3_var()
    #create_graphic_for_4_var()
    #create_graphic_for_5_var()
    #create_graphic_for_6_var()
    #create_graphic_for_7_var()
    #create_graphic_for_8_var()
    #create_graphic_for_9_var()
    #create_graphic_for_10_var()
    end = time.process_time()
    complete_time = end - begin
    if complete_time < 60:
        print("temps d'execution -> " + str(complete_time) + " seconde(s)")
    else:
        print("temps d'execution -> " + str(int(complete_time // 60)) + " minute(s) et " + str(int(complete_time % 60)) + " seconde(s)")


