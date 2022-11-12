from abc import ABC, abstractmethod
from typing import *

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
    
class corpus(ABC):
    
    def __init__(self, path, name, language, stemming, lemmatizing) -> None:
        self.path = path
        self.name = name
        self.language = language
        self.stemmer = stemming
        self.lemmatizing = lemmatizing
        
        try:
            self.load_indexed_corpus()
        except FileNotFoundError:
            self.documents_words_counter : Dict[document, Counter[str, int]] = {}
            self.proccess_corpus()
            self.save_indexed_corpus()
    
    def load_indexed_corpus(self):
        pass
    
    def proccess_corpus(self):
        pass
    
    def save_indexed_corpus(self):
        pass
        
        
    
    