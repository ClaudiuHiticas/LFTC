import os

#1. Closure function
def closure(I,nonT):
    J = I

    for item in J :
        # print(item)
        index = item[1].index('.')              #index = position of "."
        # print(index, item)
        if(index < (len(item[1]) - 1) and item[1][index+1] in nonT):    #if "." is not final and the next elem after '.' is nonT
            # print('item : ',item[1][index+1])
            for production in nonT[item[1][index+1]]:              
                if( [item[1][index+1], str('.') + str(production)] not in J):           #if "." is first
                    J.append([item[1][index+1], str('.') + str(production)])
                    # print([item[1][index+1], str('.') + str(production)])

    return J


# 2.  Set of Canonical Items 

state = []
I = []
def setOfItems(start,nonTer,ter):
    I.append(closure([['start','.'+start+'$']],nonTer))
    #print(I)
    ter += list(nonTer.keys())
    #print("list of inputs : " , ter)
    for conI in I:
        for grammar in ter:
            if(grammar == '$'):
                continue
            #print("grammar : ",grammar)
            goto = False
            goto1 = False
            shift = False
            shift1 = False
            reduce = False
            close = []
            for item in conI:
                #print("item  : ",item)
                if(item[1].index('.')<(len(item[1])-1) and item[1][item[1].index('.')+1] is grammar):
                    close.append([item[0],item[1][:item[1].index('.')]+grammar+'.'+item[1][item[1].index('.')+2:]])
                #else:
                #    print(item)
            #print("close : ",close)
            l = closure(close,nonTer)
            if(len(l) == 0):
                continue
            #print("closure : ", l)
            if(grammar in nonTer.keys()):
                goto1 = True
            else:
                shift1 = True
            if(l not in I):
                if(goto1):
                    state.append(['g',I.index(conI)+1,len(I)+1,grammar])
                    goto = True
                elif(shift1):
                    shift = True
                    state.append(['s',I.index(conI)+1,len(I)+1,grammar])
                I.append(l)

            else:
               if(goto1):
                    goto = True
                    state.append(['g',I.index(conI)+1,I.index(l)+1,grammar])
               elif(shift1):
                   shift = True
                   state.append(['s',I.index(conI)+1,I.index(l)+1,grammar])
                    



# 3. Create a Parse Table 

reduce = []
accept = -1
def toReduce(rule,accept,start):
    s = ['start',start+'.$']
    for parState in I:
        #print(s,parState)
        if(s in parState):
            #print("here;")
            accept = I.index(parState)
        for item in parState:
            if( item in rule):
                reduce[I.index(parState)].append(rule.index(item))

    return accept

            


# 4. To Parse
symbolMap = dict()
parseTable = []

def createParseTable(ter):
    for i in state:
        parseTable[i[1]-1][symbolMap[i[3]]] = i[0]+str(i[2]-1)

    # parseTable[accept][symbolMap['$']] = 'a'

    for i in reduce:
        if(len(i)>0):
            for j in ter:
                parseTable[reduce.index(i)][symbolMap[j]] = 'r'+str(i[0])
    print(symbolMap)


#  Driver Program

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
    terminals = []
    nonTerminals = dict()
    terminals = input("Enter Terminals (|) : ").split("|")
    n = int(input("No. of Non - Terminals  : "))

    for i in range(n):
        ch = input("NonTerminals : ").strip()
        rules = input("Productions (|) : ").split("|")
        nonTerminals[ch] = rules


terminals, nonTerminals, productions = readFromFile("RG.txt")

# terminals, nonTerminals = readFromConsole()

print("Terminals: ", terminals)
print("NonTerminals: ", nonTerminals)

# S = input("Start Symbol :  ")
S = "S" #Termporal
# terminals+=['$']
print("Productions : ")
for i in nonTerminals.keys():
    print(i,"-->",end=' ')
    for j in nonTerminals[i]:
        print(j,end= ' | ')
    print()

setOfItems(S,nonTerminals,terminals)
print("Step I. Set canonical collection of states")    
for count , i in enumerate(I):
    print(count+1, "{", end ="")
    for j in i:
        print("[", str(j[0]) + "->" + str(j[1]), "]", end ="")
    print("}")

# print("state Transitions : ")
# for count , i in enumerate(state):
#     print(count+1, i)

rule = []
accept = -1

for i in nonTerminals.keys():
    for j in nonTerminals[i]:
        rule.append([i,j+str('.')])

# print('rule :')
# for i in rule:
#     print(i)

# To find the reduction rules
reduce = [ [] for i in range(len(I)) ]
accept = toReduce(rule,accept,S)


#parse Table
symbols = []
symbols += terminals

for count , i in enumerate(symbols):
    symbolMap[i] = count
# print(symbols)

parseTable = [ ['-' for i in range(len(symbols))] for j in range(len(I)) ]

for i in nonTerminals.keys():
    terminals.remove(i)
    
createParseTable(terminals)

# Parse Table
print('Step II. Parse Table') 
print(" \t\t",end='')
for i in symbols:
    print(i,end= '\t')
print()
for count,j in enumerate(parseTable):
    print(count,end='\t\t')
    for i in j:
        print(i,end='\t')
    print()

