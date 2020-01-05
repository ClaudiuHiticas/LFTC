class State:
    def __init__(self):
        self.items = []

    def __eq__(self, other):
        return self.items == other.items

    def __str__(self):
        string = "{ "
        for i in self.items:
            string += '['+str(i) + "], "
        string += '}'
        return string

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)
