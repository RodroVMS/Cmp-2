import os
import cmp.visitor as visitor
import re

from TypeCollectorBuilder import TypeBuilder, TypeCollector
from TypeChecker import TypeChecker

from Grammar import G, pprint_tokens,  lexer
from Utils import FormatVisitor
from cmp.evaluation import evaluate_reverse_parse
from cmp.tools.LR1_Parser import LR1Parser
#from cmp.tools.parsing import LR1Parser

#def file_selector(folder_path="."):
    #filenames = os.listdir(folder_path)
    #selected_filename = st.selectbox("Select a file", filenames)
    #return os.path.join(folder_path, selected_filename), selected_filename

def run_pipeline(G, program):
    print("Executing Program")
    #print(program)
    
    #toks = regex.findall(program)

    tokens = lexer(program)
    #tokens = tokenize_text(toks)
    print("Tokens")
    pprint_tokens(tokens)
    
    parser = LR1Parser(G)
    #parse, operations = parser([t.token_type for t in tokens])
    parse, operations, result = parser(tokens)
    #print("\n".join(repr(x) for x in parse))
    print(parse)

    if not result:
        return

    ast = evaluate_reverse_parse(parse, operations, tokens)
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    print(tree)
    
    errors = []
    errors.append("TypeCollector Errors:")
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    print("Context\n", context)
    

    errors.append("TypeBuilder Errors:")
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    print("Context\n", context)
    
    
    errors.append("TypeChecker Errors:")
    checker = TypeChecker(context, errors)
    scope = checker.visit(ast)

    for err in errors:
        print(err)
    print(len(errors) - 3)

filename = r".\CoolPrograms\life.cl"
#filename = r".\CoolPrograms\0Simple.txt"
print("Loading " + filename)
file1 = open(filename, "r")
program = file1.read()
file1.close()

run_pipeline(G, program)

from cmp.pycompiler import Grammar
H = Grammar()
A = H.NonTerminal("A", True)
B, C, D = H.NonTerminals("B C D")
x, y, z = H.Terminals("x y z")

#A %= y + A + x + A + z + A
#A %= y + A + x + A + z 
A %= B
B %= y + B + z + B + x + B

#parser = LR1Parser(G)
#print("Done!")