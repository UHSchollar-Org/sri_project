import txt_corpus as txt
import cran_corpus as cran
import twenty_news_corpus as news
from models import vector_model, boolean_model, fuzzy_model
from document import query
import configparser
from eval import evaluate
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



q1 : query = query(0,"what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft")
q2 : query = query(1,"(aeroelastic and models) and (heated or high and (speed or aircraft)) and not speed")
q3 : query = query(2,"how do interference-free longitudinal stability measurements (made using free-flight models) compare with similar measurements made in a low-blockage wind tunnel")

evaluate(corp, model)
"""r = model.exec_query(q1)
q1 : query = query("what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft")
q2 : query = query("(aeroelastic and models) and (heated or high and (speed or aircraft)) and not speed")
q3 : query = query("experimental")
q4 : query = query("models and (speed or not heated)")

r = model.exec_query(q4)
    
for tuple in r:
    print(tuple[0])"""
"""print('***************')
print(x)
print('***************')
print(y)
print('***************')
print(z)
print('***************')"""