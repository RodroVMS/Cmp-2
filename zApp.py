import streamlit as st
import os

def file_selector(folder_path="."):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox("Select a file", filenames)
    return os.path.join(folder_path, selected_filename), selected_filename

st.title("Cool Language")

sb = st.selectbox("Choose where the file is going to be loaded or written:", ["Import File", "Raw Input"],)
import_file = True if sb == "Import File" else False


local_name = ""

if import_file:
    st.write("Introduce File's FOLDER Location")
    ti = st.text_input("Introduce Folder's Adress")
    ti = "." if ti == "" else ti
    
    filename, local_name = file_selector(ti)
    st.text("You selected: " + filename,)

    file1 = open(filename, "r")
    program = file1.read()
    file1.close()
else:
    program = st.text_area("Write Program:")

if st.button("Submit"):
    st.write("Executing Program",local_name)
    st.text(program)
