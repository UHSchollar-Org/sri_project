from abc import ABC, abstractmethod
from typing import *
from pathlib import Path
import pickle as pk
import nltk as nl
from text_processing import clean_text, get_boolean_text
from collections import Counter

class document:
    
    def __init__(self, id, title, author, text):
        self.id = id
        self.title = title
        self.text = text
        self.author = author
        
    def __eq__(self, other):
        return isinstance(other, document) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
    def __str__(self) -> str:
        return str(self.id)

class query:
    def __init__(self, id, text) -> None:
        self.id = id
        self.text = text
        self.boolean_text = get_boolean_text(text, True, False)
        self.clean_text = clean_text(text, True, False)  ##Cambiar aqui los booleanos por parametros
        self.counter = Counter(self.clean_text)
        
    def __iter__(self):
        return iter(self.clean_text)
    
    def __eq__(self, __o: object) -> bool:
        return set(self.clean_text) == set(__o.clean_text)
  
class corpus(ABC):
    
    def __init__(self, name, stemming : bool, lemmatizing : bool) -> None:
        self.path = Path.cwd()
        self.name = name
        self.stemming = stemming
        self.lemmatizing = lemmatizing
        
        
        try:
            self.load_indexed_corpus()
        except FileNotFoundError:
            self.documents_words_counter : Dict[document, Counter[str, int]] = {}
            self.all_words_counter : Dict[str, int] = {}
            self.proccess_corpus()
            self.save_indexed_corpus()
            
        self.docs_count = len(self.documents_words_counter.keys())
    
    def load_indexed_corpus(self):
        ind_corpus_path = self.path / f'corpus/indexed_corpus/{self.name}_index/'
        stemm = '' if not self.stemming else '_st'
        lemm = '' if not self.lemmatizing else '_le'
        
        with open(ind_corpus_path / f'documents{stemm}{lemm}.bak','rb') as f:
            self.documents_words_counter = pk.load(f)
        
        with open(ind_corpus_path / f'all_words{stemm}{lemm}.bak','rb') as f:
            self.all_words_counter = pk.load(f)
   
    
    def save_indexed_corpus(self):
        ind_corpus_path = self.path / f'corpus/indexed_corpus/{self.name}_index/'
        ind_corpus_path.mkdir(parents=True, exist_ok= True)
        stemm = '' if not self.stemming else '_st'
        lemm = '' if not self.lemmatizing else '_le'
        
        with open(ind_corpus_path / f'documents{stemm}{lemm}.bak','wb') as f:
            pk.dump(self.documents_words_counter, f)
        
        with open(ind_corpus_path / f'all_words{stemm}{lemm}.bak','wb') as f:
            pk.dump(self.all_words_counter, f)
        
    @abstractmethod
    def proccess_corpus(self):
        pass
    
    def token_frequency_in_doc(self, token : str, document : document):
        return self.documents_words_counter[document][token]
    
    def most_common_token_in_doc(self, document : document):
        return self.documents_words_counter[document].most_common(1)[0]
        
        
    
    