import os
import cmp.visitor as visitor 
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
    return ast


filename = r".\CoolPrograms\Test131.txt"
print("Loading " + filename)
file1 = open(filename, "r")
program = file1.read()
file1.close()

ast = run_pipeline(G,program)