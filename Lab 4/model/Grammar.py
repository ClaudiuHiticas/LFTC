class Grammar:
    def __init__(self):
        self.start_symbol = None    # S
        self.non_terminals = []     # N
        self.terminals = []         # Σ
        self.no_productions = 0

        #  production_rules['S'] = ['B', 'aA']
        self.production_rules = {}  # P

        #  production_rules_indexed[1] = 'S->B',
        #  production_rules_indexed[2] = 'S->aA'
        self.production_rules_indexed = {}
