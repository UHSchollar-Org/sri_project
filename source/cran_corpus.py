import pickle as plk
import re
from collections import Counter
from document import corpus, document
from text_processing import *

class cran_corpus(corpus):
    
        PATTERN = r'(\d+)\n\.T(.*)\n\.A(.*)\n\.B(.*)\n\.W(.*)'
        pattern = re.compile(PATTERN,re.DOTALL) 

        def __init__(self, stemming, lemmatizing) -> None:
            super().__init__('cranfield', stemming, lemmatizing,)
            self.docs_count = 1400
                    
        def proccess_corpus(self):
            data_path = self.path/'corpus/cran_corpus/cran.all.1400'
            
            with open(data_path, 'r') as f:
                texts = f.read().split('\n.I')
                for article in texts:
                    aux = self.pattern.search(article)
                    doc_id = int(aux.group(1))
                    doc_tittle = aux.group(2)
                    if doc_tittle != '':
                        doc_tittle = doc_tittle.split('\n')[1]
                    doc_author = aux.group(3)
                    if doc_author != '':
                        doc_author = doc_author.split('\n')[1]
                    doc_bibliography = aux.group(4)
                    doc_text = aux.group(5)
                    
                    doc = document(doc_id,doc_tittle,doc_author,doc_text)
                    
                    clean_doc = clean_text(doc.text, self.stemming, self.lemmatizing)
                
                    for word in set(clean_doc):
                        self.all_words_counter[word] = self.all_words_counter.get(word, 0) + 1
                
                    self.documents_words_counter[doc] = Counter(clean_doc)
