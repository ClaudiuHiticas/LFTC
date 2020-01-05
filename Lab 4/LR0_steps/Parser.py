def algorithm_iteration(grammar, table, alpha, beta, phi, state, end):
    prev_state = state

    if table[(state, 'action')] == "Shift":
        a, beta = str(beta[0]), beta[1:]  # pop the front a from beta
        state = table[(state, a)]  # e.g: state = '0'
        if state == " ":
            raise Exception("Error while parsing table[" + str(prev_state) + ", " + a + "].\n Work stack= " + str(alpha) + ", input stack= " + str(beta) + ", output= " + str(phi))
        alpha.append(a)
        alpha.append(state)

    elif table[(state, 'action')][0] == "R":
        prod_no = table[(state, "action")][1:]
        prod_no = prod_no.strip()
        prod = grammar.production_rules_indexed[int(prod_no)]
        lhs, rhs = prod.lhs, prod.rhs

        # parse alpha and rhs of production, to find the starting position for reducing
        i = len(alpha) - 2
        rhs_pos = len(rhs) - 1
        reduce_start_pos = -1
        done = False

        while i >= 2 and rhs_pos >= 0 and done is False:
            if str(alpha[i]) == str(rhs[rhs_pos]):
                reduce_start_pos = i
                rhs_pos -= 1
                i -= 2
            else:
                done = True

        alpha = alpha[0:reduce_start_pos]  # keep only what was not reduced
        last_state = alpha[reduce_start_pos - 1]
        state = table[(last_state, lhs)]
        if state == " ":
            raise Exception("Error while parsing table[" + str(prev_state) + ", "  + "].\n Work stack= " + str(alpha) + ", input stack= " + str(beta) + ", output= " + str(phi))
        alpha += [lhs, state]  # lhs + state
        phi.append(prod_no.strip())  # add production number to result string

    elif table[(state, "action")] == "acc  " and len(beta) == 1:
        print("success")
        end = True
    else:
        raise Exception("Error while parsing table[" + str(prev_state) + "].\n Work stack= " + str(alpha) + ", input stack= " + str(beta) + ", output= " + str(phi))
    return alpha, beta, phi, state, end


def parsing_algorithm(grammar, input_sequence, table):
    state = '0'
    alpha = ['$', '0']  # "$0"  # work stack
    beta = input_sequence  # input stack
    beta.append('$')
    phi = []  # output band
    end = False

    alpha, beta, phi, state, end = algorithm_iteration(grammar, table, alpha, beta, phi, state, end)
    while end is False:
        alpha, beta, phi, state, end = algorithm_iteration(grammar, table, alpha, beta, phi, state, end)

    phi.reverse()
    return phi


def make_parsing_tree_as_table(grammar, production_string):
    pt_table = []  # table: position, symbol, father, left_brother
    current_pos = 0
    father_pos = -1
    left_brother_pos = -1

    for prod_no in production_string:
        prod = grammar.production_rules_indexed[int(prod_no)]
        print(prod)
        lhs, rhs = prod.lhs, prod.rhs

        # if table is empty, first symbol(lhs) does not have a father
        if len(pt_table) == 0:
            current_pos += 1
            row = {"pos": current_pos, "symbol": lhs, "father": father_pos, "left_brother": left_brother_pos}
            pt_table.append(row)
            father_pos = current_pos

        # add the children(rhs) of the lhs, having lhs as father
        for elem in rhs:
            current_pos += 1
            row = {"pos": current_pos, "symbol": elem, "father": father_pos, "left_brother": left_brother_pos}
            pt_table.append(row)
            left_brother_pos = current_pos
        left_brother_pos = -1

        # find which element from the current rhs is the father for the next production
        if int(prod_no) + 1 in grammar.production_rules_indexed.keys():

            next_prod = grammar.production_rules_indexed[int(prod_no) + 1]
            next_lhs = next_prod.lhs

            for i in range(current_pos - 1, 0, -1):
                symbol = pt_table[i]["symbol"]
                if symbol == next_lhs:
                    father_pos = pt_table[i]["pos"]
                    break
    return pt_table
