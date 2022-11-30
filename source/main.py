import txt_corpus as txt
import cran_corpus as cran
import twenty_news_corpus as news
from models import vector_model, boolean_model
from document import query
from nltk.corpus import stopwords
import text_processing as tp
from sympy import sympify, to_dnf
import configparser

# region Reading all settings
config = configparser.ConfigParser()
config.read('source/config.ini')

steamming = config.getboolean('DEFAULT','STEAMMING')
lemmatizing = config.getboolean('DEFAULT','LEMMATIZING')
corp = config['DEFAULT']['CORPUS']
if corp not in ['txt', '20news','cranfield']:
    raise Exception('Corpus not allowed. Only TXT, 20News and Cranfield corpora are allowed')

match corp:
    case 'txt':
        corp = txt.txt_corpus(steamming, lemmatizing)
    case 'cranfield':
        corp = cran.cran_corpus(steamming,lemmatizing)
    case '20news':
        corp = news.twenty_news_corpus(steamming,lemmatizing)

model = config['DEFAULT']['MODEL']
if model not in ['boolean', 'vector']:
    raise Exception('Model not allowed. Only Boolean and Vector models are allowed')

match model:
    case 'boolean':
        model = boolean_model(corp)
    case 'vector':
        model = vector_model(corp)
#endregion



q1 : query = query("what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft")
q2 : query = query("(aeroelastic and models) and (heated or high and (speed or aircraft)) and not speed")
q3 : query = query("experimental")

r = model.exec_query(q2)
    
for tuple in r:
    print(tuple[0])