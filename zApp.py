import streamlit as st
import os
import cmp.visitor as visitor
from TypeCollectorBuilder import TypeBuilder, TypeCollector
from TypeChecker import TypeChecker

from Grammar import G, tokenize_text, ocur, ccur, semi
from Utils import FormatVisitor
from cmp.evaluation import evaluate_reverse_parse
from cmp.tools.LR1_Parser import LR1Parser


def file_selector(folder_path="."):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox("Select a file", filenames)
    return os.path.join(folder_path, selected_filename), selected_filename

def pprint_tokens(tokens):
    indent = 0
    pending = []
    s = ""
    for token in tokens:
        pending.append(token)
        if token.token_type in { ocur, ccur, semi }:
            if token.token_type == ccur:
                indent -= 1
            s += ('    '*indent + ' '.join(str(t.token_type) for t in pending))
            s += "\n"
            pending.clear()
            if token.token_type == ocur:
                indent += 1
    s += (' '.join([str(t.token_type) for t in pending]))
    return s

st.title("Cool Language")

sb = st.selectbox("Choose where the file is going to be loaded or written:", ["Import File", "Raw Input"],)
import_file = True if sb == "Import File" else False

st.sidebar.title("Options")
showProgram = st.sidebar.checkbox("Show Program", False)
showTokens = st.sidebar.checkbox("Show Tokenization", False)
showParsing = st.sidebar.checkbox("Show Parsing")
showAST = st.sidebar.checkbox("Show AST")
showTypesCollected = st.sidebar.checkbox("Show Types Collected")
showTypesBuilded = st.sidebar.checkbox("Show Types Builded")

local_name = ""

if import_file:
    st.write("Introduce File's FOLDER Location")
    ti = st.text_input(r"Introduce Folder's Adress (Default: .\CoolPrograms)")
    ti = r".\CoolPrograms" if ti == "" else ti
    
    filename, local_name = file_selector(ti)
    st.text("You selected: " + filename)

    file1 = open(filename, "r")
    program = file1.read()
    file1.close()
else:
    program = st.text_area("Write Program:")

###---------------RUN PIPELINE-----------------###
if st.button("Submit"):
    st.write("Executing Program", local_name)
    if showProgram:
        st.text(program)
    
    tokens = tokenize_text(program)
    if showTokens:
        st.write("Tokenizing")
        st.text(pprint_tokens(tokens))
    
    parser = LR1Parser(G)
    parse, operations = parser([t.token_type for t in tokens])
    if showParsing:
        st.write("Parsing")
        st.text("\n".join(repr(x) for x in parse))

    ast = evaluate_reverse_parse(parse, operations, tokens)
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    if showAST:
        st.write("Building AST")
        st.text(tree)
    
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    if errors == []:
        st.success("Collecting Types")
    else: 
        st.error("Collecting Types")
    if showTypesCollected:
        st.text("Context:")
        st.text(context)
    
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    if errors == []:
        st.success("Building Types")
    else:
        st.error("Building Types")
    if showTypesBuilded:
        st.text("Context")
        st.text(context)
    
    checker = TypeChecker(context, errors)
    scope = checker.visit(ast)
    if errors == []:
        st.success("Checking Types")
    else:
        st.error("Checking Types")
    
    st.text("Errors")
    st.text(errors)