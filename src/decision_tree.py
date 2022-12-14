from main import *
from copy import deepcopy

"""
    Exception qui se lance lorsqu'il est impossible d'insérer un noeud dans un arbre de décision ou autre problèmes
"""
class DecisionTreeError(Exception):
    """
        Constructeur:
            s(string) -> l'argument passé en paramètre de la fonction
            f(string) -> la fonction dans laquelle l'exception a été levée
    """
    def __init__(self, s, f = ""):
        Exception.__init__(self, s)
        self.s = s
        self.f = f

    """
        Fonction d'affichage
    """
    def __str__(self):
        return "exception \"DecisionTreeError\" lancée depuis la fonction \" " + self.f + \
                "\" avec le paramètre " + self.s

"""
    Arbre de décision
"""
class DecisionTree:
    """
        Constructeur:
            label(string) -> l'étiquette du noeud
            left(DecisionTree) -> fils gauche du noeud
            right(DecisionTree) -> fils droit du noeud
    """
    def __init__(self, label, left = None, right = None):
        self.label = label
        self.left = left
        self.right = right
        self.luka_v = ""
        self.id = -1

    """
        Insère un nouveau noeud qui sera le fils gauche de l'arbre
        
        value(string) -> étiquette du fils gauche
    """
    def insert_left(self, value):
        if self.left == None:
            self.left = DecisionTree(value)
        else:
            raise DecisionTreeError(value, "insert_left")

    """
        Insère un nouveau noeud qui sera le fils droit de l'arbre
        
        value(string) -> étiquette du fils droit
    """
    def insert_right(self, value):
        if self.right == None:
            self.right = DecisionTree(value)
        else:
            raise DecisionTreeError(value, "insert_right")

    """
        Compte le nombre de noeud différent dans l'arbre
        
        return(int) -> nombre de noeud différent
    """
    def size(self):
        def rec_size(t, l):
            if t == None:
                return 0
            if t.id not in l:
                l += [t.id]
                return 1 + rec_size(t.left, l) + rec_size(t.right, l)
            return rec_size(t.left, l) + rec_size(t.right, l)
        if self.id == -1:
            associate_id(self)
        return rec_size(self, [])

    """
        Fonction d'affichage
    """
    def __str__(self):
        return "(" + self.label + ", " + self.left.__str__() + ", " + self.right.__str__() +")"


def test_constructor():
    try:
        t1 = DecisionTree("x1")
        t2 = DecisionTree("x1", DecisionTree("x2"), DecisionTree("x3"))
        assert t1.__str__() == "(x1, None, None)"
        assert t2.__str__() == "(x1, (x2, None, None), (x3, None, None))"
    except AssertionError:
        print("Problème au niveau du constructeur de l'arbre")

def test_insertion():
    try:
        t = DecisionTree("x1")
        t.insert_left("x2")
        t.insert_right("x3")
        assert t.__str__() == "(x1, (x2, None, None), (x3, None, None))"
    except AssertionError:
        print("Problème au niveau des méthodes d'insertions")

if __name__ == "__main__":
    test_constructor()
    test_insertion()
