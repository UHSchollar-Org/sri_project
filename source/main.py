import text_processing
import txt_corpus as txt
from models import vector_model


corp = txt.txt_corpus(True, False)

mri_vec = vector_model(corp)

idfs = mri_vec.idfs
weights = mri_vec.weights_in_docs

print(idfs)
print("*************************************************************************************")
print(weights)