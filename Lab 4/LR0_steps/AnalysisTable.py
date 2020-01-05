from model.Item import Item


def find_production_number(grammar, item):
    lhs = item.lhs
    rhs = ""
    for elem in item.rhs:
        if elem != '.':
            rhs += str(elem)
    searched_production = lhs + " -> " + rhs

    productions = grammar.production_rules_indexed
    for number, prod in productions.items():
        if str(prod) == searched_production:
            return number
    return -1


def decide_action_type(grammar, state, key):
    action = ""

    """ if [SS -> S.] in state, then action(state) = accept, goto columns are empty """

    first_production = grammar.production_rules_indexed[0]  # prod:  SS -> S
    lhs, rhs = first_production.lhs, first_production.rhs
    initial_item = Item(lhs, rhs + ['.'])  # item: [SS -> S.] as Item('SS', ['S', '.'])

    if initial_item in state.items:
        action = "acc  "
    else:
        """ - if item [A -> alpha.beta] in state, then action(state) = shift
            - if item [A -> alpha.]     in state, then action(state) = reduce I,
                    I = nr of prod A -> alpha, goto columns are empty   """
        is_shift = False
        is_reduce = False
        I = -1

        for item in state.items:
            point_pos = item.rhs.index('.')
            alpha, beta = item.rhs[0:point_pos], item.rhs[point_pos + 1:]
            if len(beta) != 0:
                is_shift = True
            else:
                if is_reduce is True:
                    II = find_production_number(grammar, item)
                    if I != II:
                        # CONFLICT when a state contains items [A -> alphabeta.] and [B -> gama.],
                        # in which the action is reduce, but with distinct productions
                        raise Exception("   Reduce-reduce conflict in state" + str(key) + ": " + str(state))
                is_reduce = True
                I = find_production_number(grammar, item)

        if is_shift and is_reduce:
            # CONFLICT when a state contains items [A -> alpha.beta] and [B -> gama.], yielding to 2 distinct actions
            raise Exception("   Shift-reduce conflict in state" + str(key) + ": " + str(state))
        if is_shift:
            action = "Shift"
        elif is_reduce:
            action = "R" + str(I) + "   "
        else:
            raise Exception("   Error: no suitable action found for state" + str(key) + ": " + str(state))
    return action


def construct_analysis_table(grammar, can_col, goto, ):
    """ one row for each state in can_col
        'action' column = shift or reduce or accept,
        'goto' columns for each symbol X in N U E  (don't include start symbol SS)
    """
    table = {}
    # for every state complete a row in the table
    for key in can_col.keys():
        state = can_col[key]
        action = decide_action_type(grammar, state, key)
        table[(str(key), 'action')] = action

        NUE = grammar.non_terminals + grammar.terminals
        if action == "acc  " or action[0] == "R":
            # 'goto' columns are empty for each symbol X in N U E
            for X in NUE:
                if X != grammar.start_symbol:
                    table[(str(key), str(X))] = " "
        else:
            # action is shift: for each X in NUE, goto(state, X) = state_j, complete column with j
            for X in NUE:
                if X != grammar.start_symbol:
                    if ('s' + str(key), X) in goto.keys():
                        sj = goto[('s' + str(key), X)]
                        j = sj[1:]
                        table[(str(key), str(X))] = j
                    else:
                        table[(str(key), str(X))] = " "

    return table
