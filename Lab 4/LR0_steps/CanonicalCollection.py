from model.Item import Item
from model.State import State


# def convert_production_to_list(production):
#     return ['.'] + list(production)


def closure_iteration(grammar, closure_set):
    """ for each item, find the first non terminal B after '.' and add its productions in the closure """
    for item in closure_set:  # item = [A, [alpha,.,B,beta] ] meaning [A -> alpha.Bbeta]
        lhs = item.lhs
        rhs = item.rhs  # alpha.Bbeta

        point_pos = rhs.index('.')
        alpha = rhs[0:point_pos]
        Bbeta = rhs[point_pos + 1:]

        if len(Bbeta) != 0:
            B = Bbeta[0]
            if B in grammar.non_terminals:
                productions = grammar.production_rules[B]

                # add the productions of B in the closure set
                for production in productions:  # production is a list of symbols (terms and non terms)
                    rhs = ['.'] + production  # convert_production_to_list(production)
                    prod_item = Item(B, rhs)  # B -> .production
                    if prod_item not in closure_set:
                        closure_set.append(prod_item)
    return closure_set


def closure(grammar, initial_item):
    """ initial_item = (A, [alpha,.,B,beta]) meaning [A -> alpha.Bbeta]  """

    closure_set = [initial_item]
    prev_closure_set = closure_set.copy()
    closure_set = closure_iteration(grammar, closure_set)

    while closure_set != prev_closure_set:  # stop when closure was not modified
        prev_closure_set = closure_set.copy()
        closure_set = closure_iteration(grammar, closure_set)
    return closure_set


"""###############################################################################################################"""


def make_production_as_list(alpha, X, point, beta):
    production = alpha.copy()  # alpha is a list
    production.append(X)
    production.append(point)
    production.extend(beta)  # beta is a list
    return production


def goto_LR0(grammar, can_col, state, givenX):
    """  new_state = goto(state, X) = closure( [A -> alphaX.beta] ) """

    # if an item from the state contains '.X' in a production, move the point after X and
    # compute:   new state = closure( [A -> alphaX.beta] )
    new_state = State()
    for item in state:  # item [A -> alpha.Xbeta]

        lhs, rhs = item.lhs, item.rhs  # A, alpha.Xbeta
        point_pos = rhs.index('.')
        alpha = rhs[0:point_pos]
        Xbeta = rhs[point_pos + 1:]

        if len(Xbeta) != 0:
            X = Xbeta[0]
            beta = Xbeta[1:]

            if X == givenX:
                production = make_production_as_list(alpha, X, ".", beta)
                initial_item = Item(lhs, production)  # [A -> alphaX.beta]
                new_state.items = closure(grammar, initial_item)
    return new_state


"""###############################################################################################################"""


def state_in_can_col(new_state, can_col):
    for i in can_col.keys():
        s = can_col[i]
        if s == new_state:
            return i
    return -1


def canonical_collection_iteration(grammar, can_col, no_states, goto):
    new_can_col = can_col.copy()

    for index in can_col.keys():
        state = can_col[index]
        NUE = grammar.non_terminals + grammar.terminals
        for X in NUE:
            new_state = goto_LR0(grammar, can_col, state, X)
            if len(new_state) != 0:
                i = state_in_can_col(new_state, can_col)
                if i == -1:
                    new_can_col[no_states] = new_state
                    goto[('s' + str(index), X)] = 's' + str(no_states)
                    no_states += 1
                else:
                    # this state equals some other state
                    goto[('s' + str(index), X)] = 's' + str(i)

    return new_can_col, no_states, goto


def canonical_collection(grammar):
    can_col = {}  # can_col[index] = state
    goto = {}  # goto[ (s0,S) ] = s1

    first_production = grammar.production_rules_indexed[0]  # prod:  SS -> S
    lhs, rhs = first_production.lhs, first_production.rhs
    initial_item = Item(lhs, ['.']+rhs)  # item: [SS -> .S] as Item('SS', ['.', 'S'])

    state0 = State()
    state0.items = closure(grammar, initial_item)
    can_col[0] = state0
    no_states = 1

    prev_can_col = can_col.copy()
    can_col, no_states, goto = canonical_collection_iteration(grammar, can_col, no_states, goto)

    while can_col != prev_can_col:  # stop when can_col was not modified
        prev_can_col = can_col.copy()
        can_col, no_states, goto = canonical_collection_iteration(grammar, can_col, no_states, goto)

    return can_col, goto
