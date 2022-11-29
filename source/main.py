import txt_corpus as txt
import cran_corpus as cran
import twenty_news_corpus as news
from models import vector_model, boolean_model
from document import query
from nltk.corpus import stopwords
import text_processing as tp
from sympy import sympify, to_dnf
corp = txt.txt_corpus(True, False)


q1 : query = query("what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft")

r = mri_vec.exec_query(q1)

for tuple in r:
    print(tuple[0])