import re

PATTERN = r'\n\.T(.*)\n\.A(.*)\n\.B(.*)\n\.W(.*)'
pattern = re.compile(PATTERN,re.DOTALL)

path = 'C:\\Users\\karel\\OneDrive\\Escritorio\\Personal Folder\\Tercero\\Segundo Semestre\\Sistemas de Recuperacion de Informacion\\Proyecto Final\\sri_project\\corpus\\cran_corpus\\cran.all.1400'

with open(path, 'r') as f:
    texts = f.read().split('\n.I')
    text = texts[470]
    aux = pattern.search(text)
    doc_tittle = aux.group(1)
    doc_author = aux.group(2)
    doc_bibliography = aux.group(3)
    doc_text = aux.group(4)
    print('ok')
    