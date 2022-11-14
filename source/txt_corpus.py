import pickle as pk
from collections import Counter

from document import corpus, document
from text_processing import *


class txt_corpus(corpus):
    def __init__(self, steamming, lemmatizing):
        return super().__init__("txt", steamming, lemmatizing)
    
    def proccess_corpus(self):
        data_path = self.path / 'corpus/txt_corpus/'
        path_list = data_path.glob('*.txt')
        
        id = 0
        for file in path_list:
            with open(file, 'r') as f:
                doc = document(id, file.name, file.name, f.read())
            id+=1
            
            clean_doc = clean_text(doc.text, self.stemming, self.lemmatizing)
            
            for word in set(clean_doc):
                self.all_words_counter[word] = self.all_words_counter.get(word, 0) + 1
                
            self.documents_words_counter[doc] = Counter(clean_doc)
    
    def check_content(self):
        path = self.path / f'corpus/indexed_corpus/{self.name}_index/'
        stemm = '' if not self.stemming else '_st'
        lemm = '' if not self.lemmatizing else '_le'
        
        
        
        f = open(path / f'documents{stemm}{lemm}.bak','rb')
        doc = pk.load(f)
        f.close()
        
        r = open(path / f'all_words{stemm}{lemm}.bak','rb')
        words = pk.load(r)
        r.close()
        print(doc)
        print("************************************************************************")
        print(words)