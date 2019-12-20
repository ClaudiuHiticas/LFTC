import string
import os


listOfUpperCase = []
for letter in string.ascii_uppercase:
    listOfUpperCase.append(letter)

listOfLowerCase = []
for letter in string.ascii_lowercase:
    listOfLowerCase.append(letter)

listOfDigits = []
for i in range(0, 10):
    listOfDigits.append(i)

def firstMenu():
    str = "Press 1 for regular grammar\n"
    str += "Press 2 for finite automata\n"
    str += "Press 0 to exit\n"
    print(str)

def secondMenu():
    str = "Press 1 for read from file\n"
    str += "Press 2 for read from keyboard\n"
    str += "Press -1 to go back\n"
    str += "Press 0 to exit\n"
    print(str)

def regularGrammarOptions():
    d = " display "
    str = "Press 1 for" + d + "set of non terminals\n"
    str += "Press 2 for" + d + "set of terminals\n"
    str += "Press 3 for" + d + "set of productions\n"
    str += "Press 4 for" + d + "the productions of a given non-terminal symbol\n"
    str += "Press 5 for checking if the grammar is regular or not\n"
    str += "Press 6 to turn into finite automata\n"
    str += "Press -1 to go back\n"
    str += "Press 0 to exit\n"
    print(str)

def finiteAutomataOptions():
    d = " display "
    str = "Press 1 for" + d + "the set of states\n"
    str += "Press 2 for" + d + "the alphabet\n"
    str += "Press 3 for" + d + "all the transition\n"
    str += "Press 4 for" + d + "the set of final state\n"
    str += "Press 5 to turn into regular grammar\n"
    str += "Press -1 to go back\n"
    str += "Press 0 to exit\n"
    print(str)


def createDictFromList(theList):
    dict = {}
    for i in range(0, len(theList)):
        if theList[i] in listOfLowerCase or theList[i] in listOfUpperCase or theList[i] in listOfDigits:
            dict[theList[i]] = i + 1
    return dict

#1a) Read RG from file
#filename - string
fullPath = os.path.dirname(os.path.abspath(__file__))
def readRGFromFile(filename):
    regularGrammar = []
    filename = fullPath + "/" + filename
    with open(filename) as f:
        for line in f:
            regularGrammar.append(line.strip())
    return regularGrammar

#1b) Read RG from keyboard
def readRGFromKeyboard():
    regularGrammar = []
    userInput = ""
    print("Input the regular grammar rules. Write 'done' when you're done.")
    while userInput != "done":
        userInput = input()
        regularGrammar.append(userInput.strip())
    regularGrammar = regularGrammar[:len(regularGrammar)-1]
    return regularGrammar

#2a) Set of non-terminals
#str - regular grammar - string
def getNonTerminals(str):
    nonTerminals = []
    for st in str:
        for s in st:
            if s in listOfUpperCase:
                nonTerminals.append(s)
    return list(set(nonTerminals))

#2b) Set of terminals
#str - regular grammar - string
def getTerminals(str):
    terminals = []
    for st in str:
        st = st.replace("|epsilon", "")
        st = st.replace("epsilon|", "")
        st = st.replace("epsilon", "")
        for s in st:
            if s in listOfLowerCase:
                terminals.append(s)
    return list(set(terminals))

#2c) Set of productions
#str - regular grammar - string
def getProductions(str):
    return str

#2d) Productions of a given non terminal
#str - regular grammar - string
#nonTerminal - Character 
def getProductionsOfNonTerminal(str, nonTerminal):
    prodsOfNonTerminal = []
    for prod in str:
        if prod.find(nonTerminal) != -1:
            prodsOfNonTerminal.append(prod)
    return prodsOfNonTerminal

#3) Check if a grammar is regular
def checkIfRegularGrammar(regularGrammar):
    ok = False
    okEpsilon = False
    okInitial = True
    okTerminalAfterNonTerminal = True
    okMaxTwo = True
    setOfProductions = getProductions(regularGrammar)

    
    for production in setOfProductions:  
        #Verify if S->epsilon and nobody else do it   
        if "epsilon" in production: 
            if "S" in production:   
                okEpsilon = True
                production = production.replace("|epsilon", "")
                production = production.replace("epsilon|", "")
                production = production.replace("epsilon", "")
            if "epsilon" in production:
                okEpsilon = False
                print("Must be just an epsilon, for S")

        #must to don't exist S after arrow
        if production.split("->")[0] != "S":    
            if "S" in production:   
                okInitial = False
                print("No S after arrow")
        
            
        newProduction = production.split("->")[1]
        #print(newProduction)

        #maximum 2 symbols
        initial = 0
        final = len(newProduction)-1
        for i in range(0, len(newProduction)-1):
            if newProduction[i+1] != "|":
                if i - initial > 2:
                    okMaxTwo = False
                    print("Maximum 2 symbols")
                    break
                else:
                    initial = i + 1

        #right linear
        for i in range(0, len(newProduction)-1):
            if newProduction[i+1] != "|":
                if newProduction[i].isupper() and newProduction[i+1].islower():
                    okTerminalAfterNonTerminal = False
            else:
                if newProduction[i].isupper() and not newProduction[i-1].islower():
                    okTerminalAfterNonTerminal = False
        
        if(len(newProduction) == 1):
            if newProduction.isupper():
                okTerminalAfterNonTerminal = False
        
            
            
    #final check
    if okEpsilon and okInitial and okTerminalAfterNonTerminal and okMaxTwo:
        ok = True
    return "Is regular grammar" if ok else "Is not regular grammar"

#4a) Read FA from file
#filename - string
def readFAFromFile(filename):
    finiteAutomata = []
    q = ""
    F = []
    filename = fullPath + "/" + filename
    with open(filename) as f:
        q = f.readline().strip().strip("q=")
        F = f.readline().strip().strip("F={").strip("}").split(",")
        for line in f:
            finiteAutomata.append(line.strip().split("|"))
    return q, F, finiteAutomata

#4b) Read FA from keyboard
def readFAFromKeyboard():
    finiteAutomata = []
    q = input("Input the initial state: ")
    F = input("Input the final state(s): ")
    F = F.split(",")
    userInput = ""
    print("Input the transition table. Write 'done' when you're done.")
    while userInput != "done":
        userInput = input()
        finiteAutomata.append(userInput.strip().split("|"))
    finiteAutomata = finiteAutomata[:len(finiteAutomata) - 1]
    return q, F, finiteAutomata

#5a) set of states
def getSetOfStates(str):
    states = []
    for st in str:
        states.append(st[0])
    return states[1:]

#5b) display the alphabet
def getAlphabet(str):
    alphabet = []
    for s in str[0]:
        alphabet.append(s.strip(" "))
    return alphabet[1:]

#5c) display transition
def getTransitions(str):
    transitions = "  "
    for st in str:
        for i in range(0, len(st)):
            transitions += st[i]
            if i != len(st) - 1:
                transitions += "|"
        transitions += "\n"
    return transitions

#5d) Get final state
def getSetOfFinalStates(str, F):
    return F

#6 RG -> FA
def fromRegularGrammarToFiniteAutomata(str):
    finiteAutomata = []
    terminals = [""] + getTerminals(str)
    terminals_Dict = createDictFromList(getTerminals(str))
    nonTerminals = getNonTerminals(str)  
    nonTerminals_Dict = createDictFromList(nonTerminals)
    #Add terminals
    finiteAutomata.append(terminals)
    #Add nonTerminals
    for nonTerminal in nonTerminals:
        finiteAutomata.append([nonTerminal] + ([""] * (len(terminals) - 1)))
    
    productions = getProductions(str)
    initStates = ["S"]
    finalStates = ["K"]
    #Find more final states, if has epsilon
    for production in productions:
        if any(x == "epsilon" for x in production.split("->")[1].split("|")):
            finalStates.append(production.split("->")[0])
    
    productions = getProductions(str)
    for production in productions:
        for i in range(3, len(production) - 1):
            if production[i] in terminals:
                if production[i + 1] in nonTerminals:
                    finiteAutomata[nonTerminals_Dict[production[0]]
                    ][terminals_Dict[production[i]]] += production[i + 1]
                
                elif production[i + 1] == '|':
                    finiteAutomata[nonTerminals_Dict[production[0]]
                                   ][terminals_Dict[production[i]]] += 'K'
        
        if production[len(production) - 1] in terminals:
            finiteAutomata[nonTerminals_Dict[production[0]]
                           ][terminals_Dict[production[len(production) - 1]]] += 'K'
        

    
    finiteAutomata = getTransitions(finiteAutomata)
    return initStates, finalStates, finiteAutomata

#7. FA -> RG
def fromFiniteAutomataToRegularGrammar(finiteAutomata, setOfFinalStates):
    regularGrammar = []
    alphabet = getAlphabet(finiteAutomata)
    setOfStates = getSetOfStates(finiteAutomata)
    setOfFinalStates = setOfFinalStates[0].split(",")

    
    for i in range(0, len(setOfStates)):
        production = setOfStates[i] + "->"
        for j in range(0, len(alphabet)):
            listOfState = finiteAutomata[i+1][j+1].split(",")
            for state in listOfState:
                if state in setOfFinalStates and state == setOfStates[i]:
                    production += alphabet[j] + "|"
                elif state in setOfFinalStates:
                    production += alphabet[j] + "|" + alphabet[j] + state + "|"
                else:
                    production += alphabet[j] + state + "|"
                
        if production[len(production)-1] == '|':
            production = production[:-1]
        
        regularGrammar.append(production)
    for i in range(0, len(regularGrammar)):
        if regularGrammar[i].split("->")[0] in setOfFinalStates:
            regularGrammar[i] += "|epsilon"
    return regularGrammar


def runRegularGrammarLogistics(regularGrammar):
    while True:
        regularGrammarOptions()
        y = input("Your choice: ")
        if y == "1":
            print(getNonTerminals(regularGrammar))
        elif y == "2":
            print(getTerminals(regularGrammar))
        elif y == "3":
            print(getProductions(regularGrammar))
        elif y == "4":
            z = input("Enter the non-terminal whose productions you'd like: ")
            if z not in listOfUpperCase:
                print("What you've entered isn't a non-terminal.")
            else:
                print(getProductionsOfNonTerminal(regularGrammar, z))
        elif y == "5":
            print(checkIfRegularGrammar(regularGrammar))
        elif y == "6":
            initStates, finalStates, finiteAutomata = fromRegularGrammarToFiniteAutomata(
                regularGrammar)
            print("Init States: " + str(initStates))
            print("Final States: " + str(finalStates))
            print("Productions: \n" + str(finiteAutomata)) 
        elif y == "-1":
            break
        elif y == "0":
            exit()
        else:
            print("Invalid option")

def runRegularGrammar():
    while True:
        regularGrammar = []
        secondMenu()
        x = input("Your choice: ")
        if x == "1":
            regularGrammar = readRGFromFile("rg.txt")
        elif x == "2":
            regularGrammar = readRGFromKeyboard()
        elif x == "-1":
            break
        elif x == "0":
            exit()
        else:
            print("Invalid option")
        runRegularGrammarLogistics(regularGrammar)

def runfiniteAutomataLogistic(q, F, finiteAutomata):
    while True:
        finiteAutomataOptions()
        y = input("Your input: ")
        if y == "1":
            print(getSetOfStates(finiteAutomata))
        elif y == "2":
            print(getAlphabet(finiteAutomata))
        elif y == "3":
            print(getTransitions(finiteAutomata))
        elif y == "4":
            print(getSetOfFinalStates(finiteAutomata, F))
        elif y == "5":
            print(fromFiniteAutomataToRegularGrammar(finiteAutomata, F))
        elif y == "-1":
            break
        elif y == "0":
            exit()
        else:
            print("Invalid Input!")



def runFiniteAutomata():
    while True:
        q, F, finiteAutomata = [], [], []
        secondMenu()
        x = input("Your choice: ")
        if x == "1":
            q, F, finiteAutomata = readFAFromFile("fa.txt")
            #print(finiteAutomata)
        elif x == "2":
            q, F, finiteAutomata = readFAFromKeyboard()
        elif x == "0":
            exit()
        else:
            print("Invalid option")
        runfiniteAutomataLogistic(q, F, finiteAutomata)



def runProgram():
    while True:
        firstMenu()
        x = input("Your choice: ")
        if x == "1":
            runRegularGrammar()
        elif x == "2":
            runFiniteAutomata()
        elif x == "0":
            exit()
        else:
            print("Invalid option")


runProgram()

#print(checkIfRegularGrammar(readRGFromFile("rg.txt")))

# print(fromRegularGrammarToFiniteAutomata(readRGFromFile("rg.txt")))