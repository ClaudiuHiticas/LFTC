class Item:
    def __init__(self, lhs='', rhs=None):
        # e.g: [A -> alpha.Xbeta]
        self.lhs = lhs  # A
        self.rhs = rhs  # list of items in rhs
        if rhs is None:
            rhs = []

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __str__(self):
        production = ''
        for elem in self.rhs:
            production += str(elem)
        return self.lhs + ' -> ' + production
