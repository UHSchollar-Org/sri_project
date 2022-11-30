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
    

def remove_puntuation(text : list, keep_parenthesis : bool = False):
    new_text = []
    for w in text:
        new_word = re.sub(r'[^\w\s]', '', w)
        if new_word != '':
            new_text.append(new_word)
        elif keep_parenthesis and (w == '(' or w == ')'):
            new_text.append(w)
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

def remove_stopwords(text, keep_logic_exp : bool = False):
    """Remove stop words from list of tokenized words"""
    new_text = []
    for w in text:
        if keep_logic_exp and w in ['and', 'or', 'not']:
            new_text.append(w)
        elif w not in stopwords.words('english'):
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

def normalize_text(text, is_boolean_text : bool = False):
    text = tokenize_text(text)
    text = remove_non_ascii(text)
    text = to_lower(text)
    text = remove_stopwords(text, is_boolean_text)
    text = remove_puntuation(text, is_boolean_text)
    text = replace_numbers(text)
    return text

"""def normalize_keep_logic_exp(text):
    text = tokenize_text(text)
    text = remove_non_ascii(text)
    text = to_lower(text)
    text = remove_stopwords(text, True)
    text = remove_puntuation(text, True)
    text = replace_numbers(text)
    return text"""

def is_balanced(text) -> bool:
    o_parenthesis = 0
    c_parenthesis = 0
    for i in range(len(text)):
        if text[i] == '(':
            o_parenthesis += 1
        elif text[i] == ')':
            c_parenthesis += 1
        
        if o_parenthesis < c_parenthesis:
            return False
    if o_parenthesis != c_parenthesis:
        return False
    return True

def get_boolean_text(text, steaming, lemmatizing) -> List[str]:
    text = clean_text(text, steaming, lemmatizing, True)
    exp = []
    if is_balanced(text):
        i = 0
        while i < len(text):
            match text[i]:
                case 'and':
                    if i+1 < len(text) and text[i+1] not in ['and', 'or', ')']:
                        exp.append('&')
                case 'or':
                    if i+1 < len(text) and text[i+1] not in ['and', 'or', ')']:
                        exp.append('|')
                case 'not':
                    if i+1 < len(text) and text[i+1] not in ['and', 'or', 'not', '(', ')']:
                        exp.append('~'+ text[i+1])
                        i+=1
                case '(':
                    exp.append('(')
                case ')':
                    exp.append(')')
                case _:
                    exp.append(text[i])
                    if i+1 < len(text) and text[i+1] not in ['and', 'or', 'not', '(', ')']:
                        exp.append('&')
            i+=1
    
        return exp
    else:
        raise SyntaxError()
    
def clean_text(text, steaming, lemmatizing, is_boolean_text : bool = False):
    text = normalize_text(text, is_boolean_text)
    return stem_lemm(text, steaming, lemmatizing)

    