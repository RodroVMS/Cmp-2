import re
from Grammar import G, num, idx, string

keywords = r"\bclass\b|\blet\b|\bin\b|\bnew\b|\bif\b|\bthen\b|\belse\b|\bfi\b|\bcase\b|\bof\b|\besac\b|\bwhile\b|\bloop\b|\bpool\b|\binherits\b|isVoid\b|not\b|true\b|false\b|"
nums = r"\d+\.\d+|\d+|"
string=r"\".*?\"|"
#string = r"\".*?(?=(?:\\\\)+?\"|[^\\]\").*?\"(?<![^\\]\\\")"
#|\".*?[^\\]*?(?:\\\\)+\""
idex = r"[a-zA-Z]\w*|"
comments = r"\(\*.*?\*\)|--.*?\n" #
#comments = r"\(\*(.+?)\*\)"
symbols = r",|;|:|\{|\}|\(|\)|<-|=>|\.|=|\+|-|\*|/|<|>|@"



#regex = re.compile(keywords + nums + string + idex +  symbols,re.DOTALL)


filename = r".\CoolPrograms\7u.txt"
#filename = r".\CoolPrograms\0Simple.txt"
print("Loading " + filename)
file1 = open(filename, "r")
program = file1.read()
file1.close()

regex = re.compile(comments, re.DOTALL)
program = regex.sub("",program)

print(program)

program = re.compile(r"\\\\").sub("§bb§", program)
program = re.compile(r"\\\"").sub("§bc§", program)

print(program)

program = re.compile("§bb§").sub(r"\\\\", program)
program = re.compile("§bc§").sub(r"\"", program)

print(program)
regex = re.compile(keywords + nums + string + idex +  symbols,re.DOTALL)
#regex = re.compile(string, re.DOTALL)

text = regex.findall(program)
print(text)

print("   FT\n".join(child for child in text))
print("cantidad de tokens", len(text))

#s = ""
#for i in tokens:
#    i = str(i)
#    if i.isspace() or i == "\n":
#        assert False, "Bad Tokenization"
#    s += i + " "
#print(s)

#def comparer(s, text):
#    j = 0
#    stesti = ""
#    stestj = ""
#    for i in range(len(text)):
#        if text[i].isspace() or text[i] == "\n":
#            continue
#        while s[j].isspace() or s[j] == "\n":
#            j += 1
#        stesti += text[i]
#        stestj += s[j]
#        if s[j] != text[i]:
#            print("i:",stesti, "### text en i:", text[i])
#            print("j:",stestj, "### s en j:", s[j])
#            return False
#        j += 1
#    return True

#print(comparer(s, program))