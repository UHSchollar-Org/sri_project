import nltk as nl
import re
import unicodedata
import inflect as inf
from nltk.corpus import stopwords
import sympy as sy
from typing import List


def tokenize_text(text):
    return nl.word_tokenize(text)

def remove_non_ascii(text):
    new_text = []
    for w in text:
        new_word = unicodedata.normalize('NFKD', w).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_text.append(new_word)
    return new_text

def to_lower(text : list):
    return [w.lower() for w in text]
    

def remove_puntuation(text : list):
    new_text = []
    for w in text:
        new_word = re.sub(r'[^\w\s]', '', w)
        if new_word != '':
            new_text.append(new_word)
    return new_text

def replace_numbers(text : list):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inf.engine()
    new_text = []
    for w in text:
        if w.isdigit():
            new_text.append(p.number_to_words(w))
        else:
            new_text.append(w)
    return new_text

def remove_stopwords(text):
    """Remove stop words from list of tokenized words"""
    new_text = []
    for w in text:
        if w not in stopwords.words('english'):
            new_text.append(w)
    return new_text

def lemmatize_text(text):
    lemmatizer = nl.WordNetLemmatizer()
    lemmas = []
    for w in text:
        lemmas.append(lemmatizer.lemmatize(w, pos='v'))
    return lemmas

def stem_text(text):
    ps = nl.PorterStemmer()
    stems = []
    for w in text:
        stems.append(ps.stem(w))
    return stems

def stem_lemm(text, steaming, lemmatizing):
    return stem_text(lemmatize_text(text)) if steaming and lemmatizing \
        else stem_text(text) if steaming else lemmatize_text(text) if lemmatizing else text

def normalize_text(text):
    text = tokenize_text(text)
    text = remove_non_ascii(text)
    text = to_lower(text)
    text = remove_stopwords(text)
    text = remove_puntuation(text)
    text = replace_numbers(text)
    return text

def normalize_keep_stopwords(text):
    text = tokenize_text(text)
    text = remove_non_ascii(text)
    text = to_lower(text)
    text = remove_puntuation(text)
    text = replace_numbers(text)
    return text

def get_valid_boolean_expression(text : List[str]) -> List[str]:
    pass

def get_boolean_text(text, steaming, lemmatizing) -> List[str]:
    text = normalize_keep_stopwords(text)
    logic_operators = {'and': '&', 'or': '|', 'not': '~'}
    
    exp = []
     
    for i in range(len(text)):
        if text[i] in logic_operators.keys():
            exp.append(logic_operators[text[i]])
        else:
            exp.append(text[i])
            if i+1 < len(text) and text[i+1] not in ['and', 'or']:
                exp.append('&')
    
    exp = remove_stopwords(exp)
    exp = stem_lemm(exp, steaming, lemmatizing)
    
    return exp
    return get_valid_boolean_expression(exp)
    
def clean_text(text, steaming, lemmatizing):
    text = normalize_text(text)
    return stem_lemm(text, steaming, lemmatizing)

    