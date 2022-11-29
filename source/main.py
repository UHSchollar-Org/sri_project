import txt_corpus as txt
from models import vector_model, boolean_model
from document import query
from nltk.corpus import stopwords
import text_processing as tp
from sympy import sympify, to_dnf

corp = txt.txt_corpus(True, False)

"""mri_vec = vector_model(corp)

q1 : query = query("harry potter and the school")

r = mri_vec.exec_query(q1)"""

"""a = tp.get_boolean_text("harry or potter or magic not school", True, True)
a = " ".join(a)
b = sympify(a)
c = to_dnf(b)
print(c)
a = tp.get_boolean_text("(harry and and or not not ron) and (fred and george or malfoy) and not lucius", True, True)
b = sympify(" ".join(a))
c = to_dnf(b)
print(b)"""

mri_bool = boolean_model(corp)

q1 : query = query("(harry and and or not not ron) and (fred and george or malfoy) and not lucius")

r = mri_bool.exec_query(q1)