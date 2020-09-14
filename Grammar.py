import re

from cmp.pycompiler import Grammar
from cmp.utils import Token, UnknownToken

from AST import ProgramNode,ClassDeclarationNode,AttrDeclarationNode,VarDeclarationNode,AssignNode,FuncDeclarationNode,BinaryNode
from AST import AtomicNode,CallNode,InstantiateNode, PlusNode, MinusNode, StarNode, DivNode, ConstantNumNode, VariableNode
from AST import LetDeclarationNode,CaseDeclarationNode, IfDeclarationNode, IsVoidDeclarationNode, BlockNode, HyphenNode
from AST import LesserNode, EqualNode, LesserEqualNode, NotNode, ConstantStringNode, WhileDeclarationNode, ConstantBoolNode
from AST import CaseVarNode

G = Grammar()
# non-terminals
program = G.NonTerminal('<program>', startSymbol=True)
class_list, def_class = G.NonTerminals('<class-list> <def-class>')
feature_list, def_attr, def_func = G.NonTerminals('<feature-list> <def-attr> <def-func>')
param_list, param, expr_list, let_var, let_var_list = G.NonTerminals('<param-list> <param> <expr-list> <let-var> <let-var-list>')
case_var_list, case_var = G.NonTerminals("<case-var-list> <case-var>")
expr, cond, arith, term, factor, atom = G.NonTerminals('<expr> <cond> <arith> <term> <factor> <atom>')
func_call, arg_list  = G.NonTerminals('<func-call> <arg-list>')
# terminals
classx, let, inx, comment = G.Terminals('class let in comment')  #Quite print de los terminales no se que pinta
semi, colon, comma, dot, opar, cpar, ocur, ccur = G.Terminals('; : , . ( ) { }')
equal, plus, minus, star, div = G.Terminals('= + - * /')
idx, num, string, new, hyphen = G.Terminals('id int string new ˜')
ifx, then, elsex, fi, case, of, esac, whilex, loop, pool = G.Terminals("if then else fi case of esac while loop pool")
lesser, greater, at, inherits, isVoid, notx, true, false, larrow, rarrow = G.Terminals("< > @ inherits isVoid not true false <- =>")


## PRODUCTIONS ##
program %= class_list, lambda h,s: ProgramNode(s[1])
# <class-list>
class_list %= def_class + semi, lambda h,s: [s[1]]
class_list %= def_class + semi + class_list, lambda h,s: [s[1]] + s[3]
# <def-class> 
def_class %= classx + idx + ocur + feature_list + ccur, lambda h,s: ClassDeclarationNode(s[2], s[4])              #Clase sin herencia simple
def_class %= classx + idx + inherits + idx + ocur + feature_list + ccur, lambda h,s: ClassDeclarationNode(s[2], s[6], s[4])
# <feature-list>
feature_list %= def_attr + semi + feature_list, lambda h,s: [s[1]] + s[3]
feature_list %= def_func + semi + feature_list, lambda h,s: [s[1]] + s[3]
feature_list %= G.Epsilon, lambda h,s: []
# <def-attr>
def_attr %= idx + colon + idx, lambda h,s: AttrDeclarationNode(s[1], s[3])
def_attr %= idx + colon + idx + larrow + expr, lambda h,s: AttrDeclarationNode(s[1], s[3], s[5])
# <def-func>
def_func %= idx + opar + param_list + cpar + colon + idx + ocur + expr + ccur, lambda h,s: FuncDeclarationNode(s[1], s[3], s[6], s[8])
# <param-list>
param_list %= G.Epsilon, lambda h,s: []
param_list %= param, lambda h,s: [ s[1] ]
param_list %= param + comma + param_list, lambda h,s: [ s[1] ] + s[3]
# <param>  
param %= idx + colon + idx, lambda h,s: (s[1], s[3])
# <expr-list>
expr_list %= expr + semi, lambda h,s: [s[1]]
expr_list %= expr + semi + expr_list, lambda h,s: [s[1]] + s[3]
# <expr>
expr %= idx + larrow + expr, lambda h,s: AssignNode(s[1], s[3])
expr %= ocur + expr_list + ccur, lambda h,s: BlockNode(s[2])
expr %= let + let_var_list + inx + expr, lambda h,s: LetDeclarationNode(s[2], s[4])
expr %= case + expr + of + case_var_list + esac, lambda h,s: CaseDeclarationNode(s[2], s[4])#
#expr %= ifx + expr + then + expr + elsex + expr + fi, lambda h,s: IfDeclarationNode(s[2], s[4], s[6])#
expr %= whilex + expr + loop + expr + pool, lambda h,s: WhileDeclarationNode(s[2], s[4])#
#expr %= idx + opar + arg_list + cpar, lambda h,s: CallNode(s[3][0], s[1], s[3])
#expr %= expr + dot + idx + opar + arg_list + cpar, lambda h,s: CallNode(s[1], s[3], s[5])
#expr %= expr + at + idx + dot + idx + opar + arg_list + cpar, lambda h,s: CallNode((s[1], s[3]), s[5], s[7])#Verificar s[3] sea subclase de s[1]
#expr %= new + idx, lambda h,s: InstantiateNode(s[2])
expr %= isVoid + expr, lambda h,s: IsVoidDeclarationNode(s[2])
expr %= hyphen + expr, lambda h,s: HyphenNode(s[2])
#expr %= expr + plus + expr, lambda h,s: PlusNode(s[1], s[3])#
#expr %= expr + minus + expr, lambda h,s: MinusNode(s[1], s[3])#
#expr %= expr + star + expr, lambda h,s: StarNode(s[1], s[3])#
#expr %= expr + div + expr, lambda h,s: DivNode(s[1], s[3])#
#expr %= expr + lesser + expr, lambda h,s: LesserNode(s[1], s[3])#
#expr %= expr + equal + expr, lambda h,s: EqualNode(s[1], s[3])#
#expr %= expr + lesser + equal + expr, lambda h,s: LesserEqualNode(s[1], s[4])#
expr %= notx + expr, lambda h,s: NotNode(s[2])
#expr %= opar + expr + cpar, lambda h,s: s[2]
#expr %= idx, lambda h,s: VariableNode(s[2])
#expr %= num, lambda h, s: ConstantNumNode(s[1])
expr %= cond, lambda h,s: s[1]
# <let-var-list>
let_var_list %= let_var + comma + let_var_list, lambda h,s: [s[1]] + s[3]
let_var_list %= let_var, lambda h,s: [s[1]]
# <let-var>
let_var %= idx + colon + idx, lambda h,s: VarDeclarationNode(s[1], s[3], None)
let_var %= idx + colon + idx + larrow + expr, lambda h,s: VarDeclarationNode(s[1], s[3], s[5])
# <case-var-list>
case_var_list %= case_var + semi + case_var_list, lambda h,s: [s[1]] + s[3]
case_var_list %= case_var + semi, lambda h,s: [s[1]]
# <case_var>
case_var %= idx + colon + idx + rarrow + expr, lambda h,s: CaseVarNode(s[1], s[3], s[5])
# <arg-list>
arg_list %= G.Epsilon, lambda h,s: []
arg_list %= expr, lambda h,s: [ s[1] ]
arg_list %= expr + comma + arg_list, lambda h,s: [ s[1] ] + s[3]
# <arith>       
arith %= arith + plus + term, lambda h,s: PlusNode(s[1], s[3])
arith %= arith + minus + term, lambda h,s: MinusNode(s[1], s[3])
arith %= term, lambda h,s: s[1]
# <term>     
term %= term + star + factor, lambda h, s: StarNode(s[1], s[3])
term %= term + div + factor, lambda h, s: DivNode(s[1], s[3])
term %= factor, lambda h, s: s[1]
# <cond>
cond %= cond + equal + arith, lambda h,s: EqualNode(s[1], s[3]) 
cond %= cond + lesser + arith, lambda h,s: LesserNode(s[1], s[3])
cond %= cond + lesser + equal + arith, lambda h,s: LesserEqualNode(s[1],s[4])
cond %= arith, lambda h,s: s[1]
# <factor>      
factor %= atom, lambda h, s: s[1]
factor %= opar + expr + cpar, lambda h, s: s[2]
factor %= ifx + expr + then + expr + elsex + expr + fi, lambda h,s: IfDeclarationNode(s[2], s[4], s[6])
factor %= idx + opar + arg_list + cpar, lambda h,s: CallNode(None, s[1], s[3])
factor %= factor + dot + idx + opar + arg_list + cpar, lambda h,s: CallNode(s[1], s[3], s[5])
factor %= factor + at + idx + dot + idx + opar + arg_list + cpar, lambda h,s: CallNode((s[1], s[3]), s[5], s[7])#Verificar s[3] sea subclase de s[1]
#factor %= factor + func_call, lambda h,s: CallNode(s[1], s[2][0], s[2][1])
# <atom>
atom %= true, lambda h,s: ConstantBoolNode(True)
atom %= false, lambda h,s: ConstantBoolNode(False) 
atom %= string, lambda h, s: ConstantStringNode(s[1])
atom %= num, lambda h, s: ConstantNumNode(s[1])
atom %= idx, lambda h, s: VariableNode(s[1])
atom %= new + idx, lambda h,s: InstantiateNode(s[2])

# <func-call>
#func_call %= dot + idx + opar + arg_list + cpar, lambda h, s: (s[2], s[4])

def lexer(program):
    program = remove_comments(program)
    program = from_strsym_to_code(program)

    keywords = r"\bclass\b|\blet\b|\bin\b|\bnew\b|\bif\b|\bthen\b|\belse\b|\bfi\b|\bcase\b|\bof\b|\besac\b|\bwhile\b|\bloop\b|\bpool\b|\binherits\b|isVoid\b|not\b|true\b|false\b|"
    nums = r"\d+\.\d+|\d+|"
    string=r"\".*?\"|"
    idex = r"[a-zA-Z]\w*|"
    symbols = r",|;|:|\{|\}|\(|\)|<-|=>|\.|=|\+|-|\*|/|<|>|@|˜"
    #special = r"|\n"

    regex = re.compile(keywords + nums + string + idex + symbols,re.DOTALL)
    text = regex.findall(program)
    return tokenizer(text)



def tokenizer(text):
    fixed_tokens = { t.Name: Token(t.Name, t) for t in G.terminals if t not in { idx, num, string }}
    tokens = []
    for lex in text:
        try:
            token = fixed_tokens[lex]
        except KeyError:
            token = UnknownToken(lex)
            try:
                token = analize_token(token)
            except TypeError:
                pass
        tokens.append(token)

    tokens.append(Token('$', G.EOF))
    return tokens


def analize_token(token):
    lex = token.lex
    if token.lex[0] == token.lex[-1] == "\"":
        token.lex = from_code_to_strsym(lex)
        return token.transform_to(string)
    try:
        float(lex)
        return token.transform_to(num)
    except ValueError:
         return token.transform_to(idx)

def remove_comments(text):
    inside_str = False
    mod = ""
    i = 0
    while i < len(text):
        char = text[i]
        if char == "\\":
            mod += char
            escaping = True
            j = i + 1
            while text[j] == "\\":
                mod += text[j]
                escaping = not escaping
                j += 1
            mod += text[j]
            i = j
            if not escaping and text[i] == "\"":
                inside_str = False
        elif char == "\"":
            mod += char
            inside_str = not inside_str
        elif not inside_str and i + 1 < len(text) and (char == "(" and text[i + 1] == "*"):
            j = i + 2
            balance = 1
            while j + 1 < len(text) and balance!=0:
                if text[j] == "(" and text[j + 1] == "*":
                    balance += 1
                if text[j] == "*" and text[j + 1] == ")":
                    balance -= 1
                j += 1
            i = j
        elif not inside_str and i + 1 < len(text) and char == text[i + 1] == "-":
            j = i + 2
            while j < len(text) and text[j] != "\n":
                j += 1
            i = j
        else:
            mod += char  
        i += 1
    return mod
   
def from_strsym_to_code(program):
    program = re.compile(r"\\\\").sub("§bb§", program)
    program = re.compile(r"\\\"").sub("§bc§", program)
    return program

def from_code_to_strsym(program):
    program = re.compile("§bb§").sub(r"\\\\", program)
    program = re.compile("§bc§").sub(r"\"", program)
    return program

def pprint_tokens(tokens):
    indent = 0
    pending = []
    for token in tokens:
        pending.append(token)
        if token.token_type in { ocur, ccur, semi, of, inx, esac, loop, let }:
            if token.token_type in {ccur, esac, pool, inx}:
                indent -= 1
            print('    '*indent + ' '.join(str(t.token_type) for t in pending))
            pending.clear()
            if token.token_type in {of, ocur, loop, let}:
                indent += 1
    print(' '.join([str(t.token_type) for t in pending]))

def reform_text(tokens):
    indent = 0
    text = []
    line = ""
    i = 0
    while i < len(tokens):
        token = tokens[i]
        line += token.lex + " "
        if token.lex in {"{", ";", "}"}:
            text.append(line)
            if token.lex in {"{"}:
                indent += 1
            if token.lex in {"}"}:
                indent -= 1
            line = "     "*indent
        
