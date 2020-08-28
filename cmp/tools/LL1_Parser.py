from grammar import compute_firsts, compute_follows
from  pycompiler import Grammar
from utils import pprint, list_to_string

class LL1Parser:
    def __init__(self, G, firsts = None, follows = None):
        self.G = G
        
        if firsts == None:
            self.firsts = compute_firsts(G)
        else: self.firsts = firsts

        if follows == None:
            self.follows = compute_follows(G, self.firsts)
        else: self.follows = follows
        
        self.conflictType = dict()
        self.M = self.build_parsing_table(self.G, self.firsts, self.follows)
        self.parser = self.predictive_non_recursive_method(self.G, self.M)
        
        
        self.conflictChain = ""
        if self.conflictType != {}:
            conflicts, typ = self.conflict_chain(self.G, self.M)
            conflicts = list_to_string(conflicts)
            typ = list_to_string(typ)
            if typ[0] == "":
                typ = (typ[1],)
            if typ[1] == "":
                typ = (typ[0],)
            self.conflictChain = "Conflict String: " + list_to_string(conflicts) + "\nType: " + list_to_string(typ, " and ")

        

    def predictive_non_recursive_method(self, G, M):
        def parser(w):
            stack = [G.startSymbol]
            cursor = 0
            output= []

            while len(stack) > 0:
                top = stack.pop()
                a = w[cursor]

                if top.IsTerminal:
                    if top != a:
                        return f"String {w} does not belong to grammatic's generated language: It was expected {top} in position {cursor}, instead there is {a}", False
                    cursor += 1
                else:
                    try:
                        production = M[top,a][0]
                    except KeyError:
                        s = f"Error! There is no [{top} --> {a}] production", False
                        return s
                    alpha = production.Right
                    output.append(production)
                    for i in range(len(alpha) - 1, -1, -1):
                        stack.append(alpha[i])
            if len(w) > cursor + 1:
                return f'Error! String was not parsed entirely. String has length {len(w) - 1} and it was parsed until position {cursor}', False

            return output, True

        return parser 
    
    def build_parsing_table(self, G, firsts, follows):
        # init parsing table
        M = {}

        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            for t in firsts[alpha]:
                try:
                    M[X, t].append(production)
                    self.conflictType[X, t] = ("First-First", "")
                except KeyError:
                    M[X, t] = [production]

            if firsts[alpha].contains_epsilon:
                for t in follows[X]:
                    try:
                        M[X, t].append(production)
                        try:
                            self.conflictType[X, t] = (self.conflictType[X, t][0], "First-Follow")
                        except KeyError:
                            self.conflictType[X, t] = ("", "First-Follow")
                    except KeyError:
                        M[X, t] = [production]

        # for item in M.items():
        #     if(len(item[1]) > 1):
        #         return(f"Error! Table in position {item[0]} contains more than one productions {item[1]}. Therefore there is ambiguity and can't be parsed by LL(1)")            
        # parsing table is ready!!!
        return M


    def conflict_chain(self, G, M):
        analized = dict()
        #l = set()
        s = [([G.startSymbol], False, None, None)]
        while(len(s) > 0):
            cur_prod, isConflcit, g_sym, g_t  = s.pop()

            prev = []
            for sym in cur_prod:
                if sym.IsNonTerminal:
                    for t in G.terminals + [G.EOF]:
                        try:
                            n_body = M[(sym, t)]
                            try:
                                analized[(sym, t, isConflcit)]
                            except KeyError:
                                analized[(sym, t, isConflcit)] = True
                                conflict = len(n_body) > 1 or isConflcit
                                for i in range(len(n_body)):
                                    if n_body[i].IsEpsilon:
                                        s.append((prev + cur_prod[len(prev) + 1:], conflict, sym, t))
                                        if conflict:
                                            #l.add(tuple(prev))self.conflictType[X, t][0]
                                            return prev, self.conflictType[sym, t]
                                    else:
                                        a_sym = g_sym if (conflict and g_t != None) else sym
                                        a_t = g_t if (conflict and g_t != None) else t
                                        s.append((prev + list(n_body[i].Right._symbols) + cur_prod[len(prev) + 1:], conflict, a_sym, a_t))
                                    #prev += s[-1][0]
                        except KeyError:
                            pass
                    #prev += s[-1][0]
                    break
                else: prev.append(sym)
            if isConflcit and prev != []:
                #l.add(tuple(prev))
                return prev, self.conflictType[g_sym, g_t]
                
        return 0, 0


def build_parsing_table2(G, firsts, follows):
    # init parsing table
    M = {}

    # P: X -> alpha
    for production in G.Productions:
        X = production.Left
        alpha = production.Right

        for t in firsts[alpha]:
            try:
                M[X, t].append(production)
            except KeyError:
                M[X, t] = [production]

        if firsts[alpha].contains_epsilon:
            for t in follows[X]:
                try:
                    M[X, t].append(production)
                except KeyError:
                    M[X, t] = [production]

    # for item in M.items():
    #     if(len(item[1]) > 1):
    #         return(f"Error! Table in position {item[0]} contains more than one productions {item[1]}. Therefore there is ambiguity and can't be parsed by LL(1)")            
    # parsing table is ready!!!
    return M

 




## TESTS ##

G = Grammar()
A = G.NonTerminal('A', True)
B = G.NonTerminal('B')
d, c = G.Terminals('d c')

A %= c
A %= B 
B %= c
    
ll1 = LL1Parser(G)
M = ll1.M
pprint(M)

print(ll1.conflictChain)

# parser = predictive_non_recursive_method(G, M, firsts, follows)
# left_parse = parser([c, c, c, G.EOF])
# pprint(left_parse)





