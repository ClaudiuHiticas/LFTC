
import os

#1. Closure function
def closure(I,nonT):
    J = I
    for item in J :
        # print(item)
        index = item[1].index('.')
        if(index<(len(item[1])-1) and item[1][index+1] in nonT):
            # print('item : ',item[1][index+1])
            for production in nonT[item[1][index+1]]:
                if( [item[1][index+1],str('.')+str(production)] not in J):
                    J.append([item[1][index+1],str('.')+str(production)])
                    # print([item[1][index+1],str('.')+str(production)])
    return J


#2. Set of Canonical Colection
state = []
I = []
def setOfItems(start,nonTer,ter):
    I.append(closure([['start','.'+start+'$']],nonTer))
    # print("I:", I)
    ter += list(nonTer.keys())
    # print("list of inputs : " , ter)
    for conI in I:
        for grammar in ter:
            if(grammar == '$'):
                continue
            # print("grammar : ",grammar)
            goto = False
            goto1 = False
            shift = False
            shift1 = False
            reduce = False
            close = []
            for item in conI:
                #print("item  : ",item)
                if(item[1].index('.') < (len(item[1])-1) and item[1][item[1].index('.')+1] is grammar):
                    close.append([item[0], item[1][:item[1].index('.')] + grammar + '.' + item[1][item[1].index('.') + 2:]])
                #else:
                #    print(item)
            #print("close : ",close)
            l = closure(close, nonTer)
            if(len(l) == 0):
                continue
            #print("closure : ", l)
            if(grammar in nonTer.keys()):
                goto1 = True
            else:
                shift1 = True
            if(l not in I):
                if(goto1):
                    state.append(['g', I.index(conI)+1, len(I)+1, grammar])
                    goto = True
                elif(shift1):
                    shift = True
                    state.append(['s', I.index(conI)+1, len(I)+1, grammar])
                I.append(l)

            else:
               if(goto1):
                    goto = True
                    state.append(['g', I.index(conI)+1, I.index(l)+1, grammar])
               elif(shift1):
                   shift = True
                   state.append(['s', I.index(conI)+1, I.index(l)+1, grammar])


terminals = []
nonTerminals = dict()


def getTerminals(gr):
    return list(set(gr[1].split(",")))


#read terminals and nonterminals from file
fullPath = os.path.dirname(os.path.abspath(__file__))
def readFromFile(filename):
    regularGrammar = []
    filename = fullPath + "/" + filename
    with open(filename) as f:
        for line in f:
            regularGrammar.append(line.strip())

    nonTerminals = list(set(regularGrammar[0].split(",")))
    terminals = getTerminals(regularGrammar)
    productions = regularGrammar[2:]
    
    nonT = dict()
    for i in range(0, len(nonTerminals)):
        a,b= productions[i].split('->')
        nonT[a] = b.split("|")
    
    nonTerminals = nonT
    return terminals, nonTerminals,productions



def readFromConsole():
    terminals = input("Enter Terminals (|) : ").split("|")
    n = int(input("No. of Non - Terminals  : "))

    for i in range(n):
        ch = input("NonTerminals : ").strip()
        rules = input("Productions (|) : ").split("|")
        nonTerminals[ch] = rules
    return terminals, nonTerminals


def main():
    
    terminals, nonTerminals, productions = readFromFile("RG.txt")

    # terminals, nonTerminals = readFromConsole()

    print("Terminals: ", terminals)
    print("NonTerminals: ", nonTerminals)

    S = input("Start Symbol :  ")
    terminals+=['$']
    print("Productions : ")
    for i in nonTerminals.keys():
        print(i,"-->",end=' ')
        for j in nonTerminals[i]:
            print(j,end= ' | ')
        print()
    setOfItems(S,nonTerminals,terminals)
    for count , i in enumerate(I):
        print(count+1 , i)

    rule = []
    accept = -1

    for i in nonTerminals.keys():
        for j in nonTerminals[i]:
            rule.append([i,j+str('.')])

    print('rule :')
    for i in rule:
        print(i)


main()
print(state)
