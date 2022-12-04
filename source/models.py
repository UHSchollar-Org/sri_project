from abc import ABC, abstractmethod
from document import document, corpus, query
from typing import *
from pathlib import Path
import pickle as pk
from math import log10
from collections import Counter
import math
from sympy import to_dnf, sympify

class generic_mri_model(ABC):
    def __init__(self, _corpus) -> None:
        self._corpus : corpus = _corpus
        self.path = Path.cwd() / f'models_info/{type(self).__name__}/{_corpus.name}'
        
    @abstractmethod
    def exec_query(self, query) -> List[Tuple[document, float]]:
        pass
    
        
class vector_model(generic_mri_model):
    def __init__(self, corpus) -> None:
        super().__init__(corpus)

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
    
    def calc_query_tfs(self, q : query) -> Dict[str, float]:
        
        tfs_query : Dict[str, float] = {}
        
        for word in q.counter.keys():
            tfs_query[word] = q.counter[word] / q.counter.most_common(1)[0][1]
        return tfs_query
    
    def calc_query_weights(self, q : query, a = 0.5) -> Dict[str, float]:
        weights_query : Dict[str, float] = {}
        tfs_query = self.calc_query_tfs(q)
        
        for word in q.clean_text:
            weights_query[word] = (a + (1 - a) * tfs_query[word]) * self.idfs[word]
        
        return weights_query
    
    """def docs_weights_to_vector(self, doc : document) -> List[float]:
        return [0 if w not in self._corpus.documents_words_counter[doc] else self.weights_in_docs[doc][w]
                for w in self._corpus.all_words_counter.keys()]
        
    def query_weight_to_vector(self, q : query) -> List[float]:
        weights_query = self.calc_query_weights(q)
        
        return [0 if w not in q.counter else weights_query[w]
                for w in self._corpus.all_words_counter.keys()]"""
    
    def exec_query(self, q : query) -> List[Tuple[document, float]]:
        reduced_q = [w for w in q.clean_text if w in self._corpus.all_words_counter]
        ranking : List[Tuple[document, float]] = []
        weight_q = self.calc_query_weights(q)
        
        for doc in self._corpus.documents_words_counter.keys():
            doc_x_q = 0
            doc_norm = math.sqrt(sum([i**2 for i in self.weights_in_docs[doc].values()]))
            query_norm = math.sqrt(sum(weight_q.values()))
            for word in set(reduced_q):
                try:
                    doc_x_q += self.weights_in_docs[doc][word] * weight_q[word]
                except KeyError:
                    pass
            
            try:
                sim = doc_x_q / (doc_norm * query_norm)
            except ZeroDivisionError:
                sim = 0
            
            if sim > 0:
                ranking.append((doc, sim))
        
        ranking.sort(reverse = True, key= lambda x: x[1])
        
        return ranking
        
class boolean_model(generic_mri_model):
    def __init__(self, _corpus) -> None:
        super().__init__(_corpus)
        
        try:
            self.load_model_data()
        except FileNotFoundError:
            #Do things
            self.save_model_data()
    
    def load_model_data(self):
        pass
    
    def save_model_data(self):
        pass
    
    def match_atom_doc(self, doc: document, atom):
        word = str(atom)
        if word[0] == '~':
            word = word[1:]
            if word in self._corpus.documents_words_counter[doc].keys():
                return False
        else:
            if word not in self._corpus.documents_words_counter[doc].keys():
                return False
        return True
        
    def match_cc_doc(self, doc : document, cc):
        for item in cc.args:
            if not self.match_atom_doc(doc, item):
                return False
        return True
        
    def match_query_doc(self, doc : document, q_dnf) -> bool:
        
        for cc in q_dnf.args:
            if self.match_cc_doc(doc, cc):
                return True
        return False
             
    def exec_query(self, q : query) -> List[Tuple[document, float]]:
        recovery_docs : List[Tuple[document, float]]= []
        q_dnf = to_dnf(" ".join(q.boolean_text))
    
        for doc in self._corpus.documents_words_counter.keys():
            if q_dnf.is_Atom:
                if self.match_atom_doc(doc, q_dnf):
                    recovery_docs.append((doc,1))
            elif q_dnf.identity:
                if  self.match_cc_doc(doc, q_dnf):
                    recovery_docs.append((doc, 1))
            elif self.match_query_doc(doc, q_dnf):
                recovery_docs.append((doc, 1))
        
        return recovery_docs
          
class fuzzy_model(generic_mri_model):
    def __init__(self, corpus) -> None:
        super().__init__(corpus)
        
        try:
            self.load_model_data()
        except FileNotFoundError:
            pass
            self.correlation_dict : Dict[str, Dict[str,float]]= self.calc_correlation_dict()
            self.belongs_docs : Dict[document, Dict[str, float]] = self.calc_belongs_docs()
            self.save_model_data()
    
    def load_model_data(self):
        with open(self.path / f'belongs_docs.bak','rb') as f:
            self.belongs_docs = pk.load(f)
    
    def save_model_data(self):
        self.path.mkdir(parents=True, exist_ok= True)
        
        with open(self.path / f'belongs_docs.bak','wb') as f:
            pk.dump(self.belongs_docs, f)
    
    def docs_contain_word(self, word : str) -> List[document]:
        return [doc for doc in self._corpus.documents_words_counter.keys() 
                if word in self._corpus.documents_words_counter[doc]]
    
    def calc_correlation(self, word_i : str, word_j : str) -> float:
        docs_i = self.docs_contain_word(word_i)
        docs_j = self.docs_contain_word(word_j)
        
        n_i = len(docs_i)
        n_j = len(docs_j)
        n_ij = len(set(docs_i) & set(docs_j))
                
        return n_ij / (n_i + n_j - n_ij)
    
    def calc_correlation_dict(self) -> Dict[str, Dict[str, float]]:
        correlation_dict : Dict[str, Dict[str, float]] = {}
        
        for word_i in self._corpus.all_words_counter.keys():
            correlation_dict[word_i] = {}
            for word_j in self._corpus.all_words_counter.keys():
                if word_i != word_j:
                    correlation_dict[word_i][word_j] = self.calc_correlation(word_i, word_j)
        
        return correlation_dict

    def calc_belongs_doc_word(self, doc, word_i) -> float:
        mult_corr = 1
        for word_l in self._corpus.documents_words_counter[doc].keys():
            mult_corr  *= (1 - self.correlation_dict[word_i][word_l])
        
        return 1 - mult_corr    
    
    def calc_belongs_docs(self) -> Dict[document, Dict[str, float]]:
        belongs_docs : Dict[document, Dict[str, float]] = {}
        
        for doc in self._corpus.documents_words_counter.keys():
            belongs_docs[doc] = {}
            for word in self._corpus.all_words_counter.keys():
                belongs_docs[doc][word] = self.calc_belongs_doc_word(doc, word)
                
        return belongs_docs
    
    def to_complete_dnf(self, dnf):
        dnf = to_dnf(dnf)
        
        for var in dnf.free_symbols:
            new_dnf = ''
            for cc in dnf.args:
                if var not in cc.free_symbols:
                    exp = sympify(f'{var} | ~{var}')
                    new_cc = f'({str(cc)}) & ({str(exp)})'
                    new_dnf += f'({new_cc}) | '
                else:
                    new_dnf += f'({str(cc)}) | '
            new_dnf = new_dnf[:-3]
            dnf = to_dnf(new_dnf)
        
        return dnf
                    
    def calc_belong_doc_cc(self, doc, cc):
        belong_doc_cc = 1
        for atom in cc.args:
            if atom.is_negative:
                atom = str(atom)[1:]
                belong_doc_cc *= (1 - self.belongs_docs[doc][atom])
            else:
                atom = str(atom)
                belong_doc_cc *= self.belongs_docs[doc][atom]
        
        return belong_doc_cc
    
    def exec_query(self, query) -> List[Tuple[document, float]]:
        ranking : List[Tuple[document, float]] = []
        q_dnf = to_dnf(" ".join(query.boolean_text))
        
        if not q_dnf.is_Atom:
            q_dnf = self.to_complete_dnf(q_dnf)
        
        for doc in self._corpus.documents_words_counter.keys():
            if not q_dnf.is_Atom:
                belong_doc_query = 1
                
                for cc in q_dnf.args:
                    belong_doc_cc = self.calc_belong_doc_cc(doc, cc)
                    belong_doc_query *= (1 - belong_doc_cc)
                
                ranking.append((doc, 1 - belong_doc_query))    
            else:
                if not q_dnf.is_negative:
                    ranking.append((doc, self.belongs_docs[doc][str(q_dnf)]))
                else:
                    ranking.append((doc, 1 - self.belongs_docs[doc][str(q_dnf)[1:]]))
        
        ranking.sort(reverse = True, key= lambda x: x[1])
        
        return ranking