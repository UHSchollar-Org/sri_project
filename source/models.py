from abc import ABC, abstractmethod
from document import document, corpus
from typing import *
from pathlib import Path
import pickle as pk
from math import log10

class generic_mri_model(ABC):
    def __init__(self, _corpus) -> None:
        self._corpus : corpus = _corpus
    
    @abstractmethod
    def exec_query(self, query) -> List[int]:
        pass
        
class vector_model(generic_mri_model):
    def __init__(self, corpus) -> None:
        super().__init__(corpus)
        self.path = Path.cwd() / 'models_info/vector_model/'
        
        try:
            self.load_model_data()
        except FileNotFoundError:
            self.idfs : Dict[str, float] = self.calc_idfs()
            self.tfs : Dict[document, Dict[str, float]] = self.calc_tfs()
            self.weights_in_docs : Dict[document, Dict[str, float]] = self.calc_weights()
            self.save_model_data()
    
    def calc_idfs(self) -> Dict[str, float]:
        idfs : Dict[str, float] = {} 
        N = self._corpus.documents_words_counter.keys().__len__()
        
        for word in self._corpus.all_words_counter:
            idfs[word] = log10(N/self._corpus.all_words_counter[word])
        return idfs
    
    def calc_tfs(self) -> Dict[document, Dict[str, float]]:
        tfs : Dict[document, Dict[str, float]]= {}
        
        for doc in self._corpus.documents_words_counter.keys():
            counter = self._corpus.documents_words_counter[doc]
            doc_dict : Dict[str, float] = {}
            for word in counter.keys():
                doc_dict[word] = self._corpus.token_frequency_in_doc(word, doc) / self._corpus.most_common_token_in_doc(doc)[1]
            tfs[doc] = doc_dict
        return tfs
            
    
    def calc_weights(self) -> Dict[document, Dict[str, float]]:
        weight : Dict[document, Dict[str, float]] = {}
        
        for doc in self._corpus.documents_words_counter.keys():
            counter = self._corpus.documents_words_counter[doc]
            doc_dict : Dict[str, float] = {}
            for word in counter.keys():
                doc_dict[word] = self.tfs[doc][word] * self.idfs[word]
            weight[doc] = doc_dict
        
        return weight     
    
    def load_model_data(self):        
        with open(self.path / f'idfs.bak','rb') as f:
            self.idfs = pk.load(f)
        
        with open(self.path / f'weights.bak','rb') as f:
            self.weights_in_docs = pk.load(f)
    
    def save_model_data(self):
        
        self.path.mkdir(parents=True, exist_ok= True)
        
        with open(self.path / f'idfs.bak','wb') as f:
            pk.dump(self.idfs, f)
        
        with open(self.path / f'weights.bak','wb') as f:
            pk.dump(self.weights_in_docs, f)
    
    def calc_query_tf(self, clean_query) -> Dict[str, float]:
        pass
        
    
    def calc_query_weight(self, clean_query) -> Dict[str, float]:
        pass
    
    def exec_query(self, clean_query) -> List[int]:
        pass
    
    

class boolean_model(generic_mri_model):
    pass