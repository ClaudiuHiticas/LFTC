# Scanner
from os import sys, path
from random import randint
import re

#parameter: fileName - the source of the toy language source
class Scanner:
    def __init__(self, fileName):
        #toy language source
        self.fileName = fileName 
        #file to store the program internal form (PIF)
        self.outputFileName = path.splitext(path.basename(fileName))[0] + "_pif.txt"
        #clear file if already exist
        open(self.outputFileName, 'w').close()
        #file to store the identifiers table
        self.outputIdentifiersTable = path.splitext(path.basename(fileName))[0] + "_id_table.txt"
        #file to store the constant table
        self.outputConstantTable = path.splitext(path.basename(fileName))[0] + "_const_table.txt"

        #hashtable for all the program symbols (if, for, while, int, else, float...)
        self.symbolsTable = {}
        #hashtable for sorting the identifiers, as a pair identifier -> integer id
        self.identifiersTable = {}
        # hashtable for storing the identifiers, as a pair constant -> integer id
        self.constantsTable = {}

        #load all the toy language symbols
        self.populateSymbolTable()

        #define regex patterns
        self.identifierPattern = re.compile('^[a-zA-Z][a-zA-Z0-9]{0,8}$')
        self.intPattern = re.compile('^0$|^([-+]?[1-9][0-9]*)$')
        self.charPattern = re.compile('^\'[0-9a-zA-Z]\'$')
        

    #the method to loads all the symbol table in memory from disk
    def populateSymbolTable(self):
        try:
            #open the file
            f = open("symbols.dat")
            #iterate through its lines
            for line in f.readlines():
                #get the symbol and the symbol id from each line from file
                (symbol, sid) = line.split()
                #add the data in symbols table
                self.symbolsTable[symbol] = sid
        except IOError:
            #in case there is no file, print an error
            print("Error: Symbol file not found!")
            sys.exit()
        

    # method returns a random integer that is not in the values array
    def randomNotIn(self, values):
        #get a random number beteen 1 and 100000
        r = randint(1, 100000)
        #if exist
        while r in values:
            #generate another one
            r = randint(1, 100000)
        #return it
        return r
    
    #method append buff to the file <outputFileName>
    def appendToOutput(self, buff):
        #open file
        with open(self.outputFileName, "a") as f:
            #write the string buff as a new line
            f.write(buff)
    
    #sorting the tables based on key
    def sortTable(self, tableToSort):
        dictValues = list(tableToSort.keys())
        dictValuesSorted = sorted(dictValues)
        newDict = {}
        for key in tableToSort:
            for i in range(0, len(dictValuesSorted) - 1):
                if dictValuesSorted[i] == key:
                    newDict[key] = [tableToSort[key], tableToSort[dictValuesSorted[i+1]]]
            if key == dictValuesSorted[len(dictValuesSorted) - 1]:
                newDict[key] = [tableToSort[key], - 1]
        return newDict

    #method writes the identifiers and constant table
    def writeTables(self):
        self.constantsTable = self.sortTable(self.constantsTable)
        self.identifiersTable = self.sortTable(self.identifiersTable)

        #open file for identifiers table
        with open(self.outputIdentifiersTable, "w") as f:
            #iterate throught the identifiers table
            for key in self.identifiersTable:
                #write the pair on a new line
                f.write("%s %s\n" % (key, self.identifiersTable[key]))
        
        #open file for constants table
        with open(self.outputConstantTable, "w") as f:
            #iterate throught the constant table
            for key in self.constantsTable:
                #write the pair on a new line
                f.write("%s %s\n" % (key, self.constantsTable[key]))

    #method decides if _token is a symbol or an identifiers
    def addToken(self, _token):
        #if the _token is in symbols table, then it's a symbol
        if _token in self.symbolsTable:
            return self.addSymbol(_token)
        #else must be an identifier
        else:
            return self.addIdentifier(_token)
    
    #method prints the symbol to the program internal form (PIF)
    def addSymbol(self, _symbol):
        #if the symbol is in the symbol table
        if _symbol in self.symbolsTable:
            #print it
            self.appendToOutput(str(self.symbolsTable[_symbol] + " 0\n"))
            return True
        else:
            #return false because _symbol is not a valid symbol, and then throw an error
            return False
    
    #method prints identifier and it's id to the output file
    def addIdentifier(self, _id):
        #assign a new unused integer id for the current identifier
        if _id not in self.identifiersTable:
            self.identifiersTable[_id] = self.randomNotIn(self.identifiersTable.values())
            #print to program internal form output file
            self.appendToOutput(self.symbolsTable["identifier"] + " " + str(self.identifiersTable[_id]) + "\n")
        return True

    #method add a constant to the table and prints it to the output file
    def addConstant(self, _val):
        #assign a new unused integer id for the current constant
        if _val not in self.constantsTable:
            self.constantsTable[_val] = self.randomNotIn(self.constantsTable.values())
            # print to the program internl form output file
            self.appendToOutput(self.symbolsTable["constant"] + " " + str(self.constantsTable[_val]) + "\n")
        return True

    #generator method returns all the characters line by line
    def getNextChar(self):
        try:
            #open the file for reading
            f = open(self.fileName, "r")
            #read all the lines
            lines = f.readlines()
            #iterate through lines
            for lineIndex, line in enumerate(lines):
                #iterete through columns
                for columnIndex, ch in enumerate(line):
                    #yield the line, column, and the current character
                    yield [lineIndex, columnIndex, ch]
        #if the file was not found, print error
        except IOError:
            print("Error! Source file not found!")
            sys.exit()
    
    #check if s is a list
    def isList(self, s):
        if s[0] != "[" and s[len(s) - 1] != "]":
            return False
        for i in range(1, len(s) - 1):
            if s not in self.constantsTable and s not in self.identifiersTable:
                return False
        return True

    #method to tokenize the source file
    def tokenize(self):
        #get the generator
        charIterator = self.getNextChar()
        try:
            #get the next value from the generator
            (i, j, ch) = next(charIterator)
            #we iterate while we get a stopIteration exception
            while True:
                #in case we have an alphabet character
                if ch.isalpha():
                    #variable to store the current identifier
                    _id = ""
                    #we iterete with the iterator while we have valid identifier characters
                    while ch.isalpha() or ch.isdigit():
                        #append the current character to id
                        _id += ch
                        #get the next character
                        (i, j, ch) = next(charIterator)
                    # at the end, if the lenght of the iterator is more than the max allowed lenght
                    # throw an error
                    if not self.identifierPattern.match(_id):
                        print("Error: entifier has too many characters. (line, col) = (%d, %d)" % (i, j))
                        sys.exit()
                    # add the token to the interal hashmaps
                    self.addToken(_id)
                    _id = ""
                # in case we have a digit (0-9) or a char in '' or a sign (+, -)
                elif ch.isdigit() or ch == '\'' or ch == '+' or ch == '-':
                    # variable stores the current constant
                    _val = ""
                    # while there is a digit (0-9) or a char in '' or a sign (+, -)
                    while ch.isdigit() or ch == '\'' or ch.isalpha() or ch == '+' or ch == '-':
                        # append the character to the constant
                        _val += ch
                        # get next character
                        (i, j, ch) = next(charIterator)
                    # add the constant to the program internal form and to the internal hashmaps
                    # if the last ch is a ' we add it to the val
                    if ch == "\'":
                        _val += ch
                    if self.charPattern.match(_val) or self.intPattern.match(_val):
                        self.addConstant(_val)
                    else:
                        print(
                            "ERROR: Constant is not a char or int. (line, col) = (%d, %d)" % (i, j))
                        sys.exit()
                # ignore whitespace characters
                elif ch.isspace():
                    # get the next character
                    (i, j, ch) = next(charIterator)
                # else, we may have a symbol or an invalid identifier
                else:
                    # get the first character and store it in the _id variable
                    _id = ch
                    # try to get the second one for cases like >=, <=, == and !=
                    try:
                        # store last character
                        last = ch
                        # get the next cahracter
                        (i, j, ch) = next(charIterator)
                        # if we are in one of the cases >=, <=, == or !=, we update the variable
                        if (last == '>' or last == '<' or last == '=' or last == '!') and ch == '=':
                                _id = _id + ch
                    except StopIteration:
                        # no other character left to get, we simply pass cause we may have }
                        pass
                    # if we couldn't add the symobl, we throw an error because it is an unexpected
                    # symbol identifier
                    if not self.addSymbol(_id):
                        print(
                            "ERROR: Syntax Error detected at (line, col) = (%d, %d)" % (i, j))
                        print("ERROR: Unexpected token '%s'" % _id)
                        sys.exit()
        # in case we reached the end of the iteration
        except StopIteration:
            self.writeTables()
            print("> finish")
            return

# method scans and tokenize the filename source code
def scan(filename):
    # create the scaner
    s = Scanner(filename)
    # call the tokenize method
    s.tokenize()

# if name is main
if __name__ == '__main__':
    # get the first argument of the args
    # log it
    print("> scanning " + str(sys.argv[1]) + "...")
    # scan that filename
    scan(sys.argv[1])


