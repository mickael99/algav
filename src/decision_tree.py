"""
    Exception qui se lance lorsqu'il est impossible d'insérer un noeud dans un arbre de décision
"""
class InsertionDecisionTreeError(Exception):
    """
        Constructeur:
            s -> l'argument passé en paramètre de la fonction
            f -> la fonction dans laquelle l'exception a été levée
    """
    def __init__(self, s, f = ""):
        Exception.__init__(self, s)
        self.s = s
        self.f = f

    """
        Fonction d'affichage
    """
    def __str__(self):
        return "exception \"InsertionDecisionTreeError\" lancée depuis la fonction \" " + self.f + \
                "\" avec le paramètre " + self.s

"""
    Arbre de décision
"""
class DecisionTree:
    """
        Constructeur:
            label -> l'étiquette du noeud
            left -> fils gauche du noeud
            right -> fils droit du noeud
    """
    def __init__(self, label, left = None, right = None):
        self.label = label
        self.left = left
        self.right = right

    """
        Insère un nouveau noeud qui sera le fils gauche de l'arbre
            value -> étiquette du fils gauche
    """
    def insert_left(self, value):
        if self.left == None:
            self.left = DecisionTree(value)
        else:
            raise InsertionDecisionTreeError(value, "insert_left")

    """
        Insère un nouveau noeud qui sera le fils droit de l'arbre
            value -> étiquette du fils droit
    """
    def insert_right(self, value):
        if self.right == None:
            self.right = DecisionTree(value)
        else:
            raise InsertionDecisionTreeError(value, "insert_right")

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



