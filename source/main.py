from txt_corpus import txt_corpus
from cran_corpus import cran_corpus
from cisi_corpus import cisi_corpus
from med_corpus import med_corpus
from twenty_news_corpus import twenty_news_corpus
from models import vector_model, boolean_model, fuzzy_model
from document import query
import configparser
from eval import evaluate
import matplotlib as plt

# region Reading all settings

steamming = True
lemmatizing = False
corp = 'medline'
if corp not in ['txt', 'cisi', 'medline', '20news','cranfield']:
    raise Exception('Corpus not allowed. Only TXT, CISI, 20News and Cranfield corpora are allowed')

match corp:
    case 'txt':
        corp = txt_corpus(steamming, lemmatizing)
    case 'cranfield':
        corp = cran_corpus(steamming, lemmatizing)
    case '20news':
        corp = twenty_news_corpus(steamming, lemmatizing)
    case 'cisi':
        corp = cisi_corpus(steamming, lemmatizing)
    case 'medline':
        corp = med_corpus(steamming, lemmatizing)

model = 'vector'
if model not in ['boolean', 'vector', 'fuzzy']:
    raise Exception('Model not allowed. Only Boolean and Vector models are allowed')

match model:
    case 'boolean':
        model = boolean_model(corp)
    case 'vector':
        model = vector_model(corp)
    case 'fuzzy':
        model = fuzzy_model(corp)
#endregion

"""q = query(0,"shock wave")
r= model.exec_query(q)
for t in r:
    print(t[0], t[1])"""
evaluate(corp, model)