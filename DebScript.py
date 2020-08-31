import os
import cmp.visitor as visitor

from TypeCollectorBuilder import TypeBuilder, TypeCollector
from TypeChecker import TypeChecker

from Grammar import G, tokenize_text, pprint_tokens
from Utils import FormatVisitor
from cmp.evaluation import evaluate_reverse_parse
from cmp.tools.LR1_Parser import LR1Parser
#from cmp.tools.parsingM import LR1Parser

#def file_selector(folder_path="."):
    #filenames = os.listdir(folder_path)
    #selected_filename = st.selectbox("Select a file", filenames)
    #return os.path.join(folder_path, selected_filename), selected_filename

def run_pipeline(G, program):
    print("Executing Program")
    print(program)
    
    
    tokens = tokenize_text(program)
    pprint_tokens(tokens)
    
    parser = LR1Parser(G)
    parse, operations = parser([t.token_type for t in tokens])
    print("\n".join(repr(x) for x in parse))

    ast = evaluate_reverse_parse(parse, operations, tokens)
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    print(tree)
    
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    print("Context\n", context)
    print(errors)

    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    print("Context\n", context)
    print(errors)

    checker = TypeChecker(context, errors)
    scope = checker.visit(ast)

    print(errors)

filename = r".\CoolPrograms\Test131.txt"
print("Loading " + filename)
file1 = open(filename, "r")
program = file1.read()
file1.close()

run_pipeline(G, program)