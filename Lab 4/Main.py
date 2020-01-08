from LR0_steps.CanonicalCollection import canonical_collection
from LR0_steps.AnalysisTable import construct_analysis_table
from LR0_steps.Parser import parsing_algorithm, make_parsing_tree_as_table
from model.Grammar import Grammar
from model.Production import Production


def read_codification_table(filename):
    codification_table = {}  # table[token] = code
    file = open(filename, 'r')

    line = file.readline().strip()
    while line != "":
        line = line.split(" ")
        token, code = line[0].strip(), int(line[1])
        codification_table[token] = code
        line = file.readline().strip()

    file.close()
    return codification_table


def read_lab1_input_sequence(filename):
    """ A list of codes(ints) representing tokens that appear in a source code program """
    file = open(filename, 'r')
    input_sequence = []

    line = file.readline().strip()
    while line != "":
        input_sequence.append(int(line))
        line = file.readline().strip()

    file.close()
    return input_sequence


def replace_terminals_with_codes(productions, codif_table, terminals):
    productions_with_codes = []
    for prod_as_string in productions:
        prod_as_list = prod_as_string.split(" ")
        for i in range(0, len(prod_as_list)):
            symbol = prod_as_list[i]
            if symbol in terminals:
                code = codif_table[symbol]
                prod_as_list[i] = code
        productions_with_codes.append(prod_as_list)

    return productions_with_codes


def read_lab1_grammar_from_file(filename, codif_table):
    file = open(filename, "r")
    grammar = Grammar()

    s = file.readline().strip()
    grammar.start_symbol = s

    non_terms = file.readline().strip().split(" ")
    grammar.non_terminals = non_terms

    terms = file.readline().strip().split(" ")
    terms_replaced = terms.copy()
    for i in range(0, len(terms)):
        if terms[i] in codif_table.keys():
            terms_replaced[i] = codif_table[terms[i]]
    grammar.terminals = terms_replaced

    # replace terminals with their codes in productions
    # a constant = character or integer number will have code 1
    line = file.readline().strip()
    while line != "":
        production_rule = line.split("->")
        non_term = production_rule[0].strip()
        productions = production_rule[1].split("|")
        productions_with_codes = replace_terminals_with_codes(productions, codif_table, terms)

        if non_term in grammar.production_rules.keys():
            grammar.production_rules[non_term].extend(productions_with_codes)
        else:
            grammar.production_rules[non_term] = productions_with_codes

        # SS->S production will have number 0
        for production in productions_with_codes:
            i = grammar.no_productions
            grammar.production_rules_indexed[i] = Production(non_term, production)  # non_term + "->" + production
            grammar.no_productions += 1

        line = file.readline().strip()

    file.close()
    return grammar


def read_seminar_input_sequence(filename):
    file = open(filename, 'r')
    input_sequence = file.readline().strip()
    file.close()
    return input_sequence


def make_productions_as_lists(productions):
    productions_as_lists = []
    for prod_as_string in productions:
        prod = prod_as_string.split(" ")
        productions_as_lists.append(prod)
    return productions_as_lists


def read_seminar_grammar_from_file(filename):
    file = open(filename, "r")
    grammar = Grammar()

    s = file.readline().strip()
    grammar.start_symbol = s

    non_terms = file.readline().strip().split(" ")
    grammar.non_terminals = non_terms

    terms = file.readline().strip().split(" ")
    grammar.terminals = terms

    line = file.readline().strip()
    while line != "":
        production_rule = line.split("->")
        non_term = production_rule[0].strip()
        productions = production_rule[1].split("|")
        productions_as_lists = make_productions_as_lists(productions)

        if non_term in grammar.production_rules.keys():
            grammar.production_rules[non_term].extend(productions_as_lists)
        else:
            grammar.production_rules[non_term] = productions_as_lists

        # SS->S production will have number 0
        for production in productions_as_lists:
            i = grammar.no_productions
            grammar.production_rules_indexed[i] = Production(non_term, production)
            grammar.no_productions += 1

        line = file.readline().strip()

    file.close()
    return grammar


def print_codification_table(codif_table):
    print("\n\n CODIFICATION TABLE:")
    print("token\t\t| code")
    print('_' * 30)
    for key in codif_table.keys():
        print(key + "\t\t| " + str(codif_table[key]))


def print_canonical_collection(can_col):
    print("\n\n CANONICAL COLLECTION OF STATES:\n")
    for k in can_col.keys():
        print('s' + str(k), can_col[k])


def print_analysis_table(table, grammar, can_col):
    print("\n\n ANALYSIS TABLE:\n")
    print(table)

    NUE = grammar.non_terminals + grammar.terminals
    header = "\n   action| "
    for X in NUE:
        if X != grammar.start_symbol:
            header += str(X) + " | "
    print(header)
    print('_' * 30)
    for i in range(0, len(can_col.keys())):
        row = str(i) + "| " + table[(str(i), "action")] + " | "
        for X in NUE:
            if X != grammar.start_symbol:
                row += table[(str(i), str(X))] + " | "
        print(row)
    print("\n")


def print_production_string(prod_string):
    print("\n\n PRODUCTION STRING:\n")
    print(prod_string)


def print_parsing_tree_as_table(pt_table):
    print("\nposition | symbol | father_position | left_brother")
    print("_" * 30)
    for i in range(0, len(pt_table)):
        print("\t", pt_table[i]["pos"], "\t | ", pt_table[i]["symbol"], "\t| ", pt_table[i]["father"], "\t| ", pt_table[i]["left_brother"])


def seminar_example_main():
    input_sequence = read_seminar_input_sequence("data/seminar_example/input_sequence.txt")
    input_sequence = input_sequence.split(' ')
    # print(input_sequence)

    grammar = read_seminar_grammar_from_file("data/seminar_example/grammar.txt")
    # each non_term has a list of productions, and each production is a list of symbols(terminals or non terminals)
    # for k in grammar.production_rules.keys():
    #     print(k, grammar.production_rules[k])
    # for k in grammar.production_rules_indexed.keys():
    #     print(k, grammar.production_rules_indexed[k])

    col, goto = canonical_collection(grammar)
    print_canonical_collection(col)
    for k in goto.keys():
        print(k, goto[k])

    table = construct_analysis_table(grammar, col, goto)
    print_analysis_table(table, grammar, col)

    prod_string = parsing_algorithm(grammar, input_sequence, table)
    print_production_string(prod_string)

    pt_table = make_parsing_tree_as_table(grammar, prod_string)
    print_parsing_tree_as_table(pt_table)


def lab1_example_main():
    cod_table = read_codification_table("data/lab1/codification_table.txt")
    # print_codification_table(cod_table)

    input_sequence = read_lab1_input_sequence("data/lab1/PIF_input_sequence.txt")
    print(input_sequence)

    grammar = read_lab1_grammar_from_file("data/lab1/grammar.txt", cod_table)
    # each non_term has a list of productions, and each production is a list of symbols(terminals or non terminals)
    # for k in grammar.production_rules.keys():
    #     print(k, grammar.production_rules[k])
    for k in grammar.production_rules_indexed.keys():
        print(k, grammar.production_rules_indexed[k])

    col, goto = canonical_collection(grammar)
    print_canonical_collection(col)
    for k in goto.keys():
        print("goto", k, "=", goto[k])

    table = construct_analysis_table(grammar, col, goto)
    print_analysis_table(table, grammar, col)

    prod_string = parsing_algorithm(grammar, input_sequence, table)
    print_production_string(prod_string)

    pt_table = make_parsing_tree_as_table(grammar, prod_string)
    print_parsing_tree_as_table(pt_table)


def main():
    """
    SS is the new start symbol for the enriched grammar, it should be included in the nonterminals list, and
    SS->S must be the first production rule in the file, so it will correspond to the number 0 (because the rules are numbered)
    In the grammar files, write the productions like this: B-> b C|B C ,meaning that you have to manually separate the symbols by space,
because it would be harder to know which are the symbols from something like this: prog->declstmt;returnstmt
    """
    seminar_example_main()
    # lab1_example_main()


main()
