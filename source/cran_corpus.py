import pickle as plk
import re
import ir_datasets
from collections import Counter
from document import corpus, document
from text_processing import *

class cran_corpus(corpus):
    """A small corpus of 1,400 scientific abstracts.
    """
    
    PATTERN = r'(\d+)\n\.T(.*)\n\.A(.*)\n\.B(.*)\n\.W(.*)'
    pattern = re.compile(PATTERN,re.DOTALL) 

    def __init__(self, stemming : bool, lemmatizing : bool) -> None:
        """reate a cran_corpus using corpus.__init__ and

        Args:
            stemming (bool): True if when processing the corpus we will apply stemming
            lemmatizing (bool): True if when processing the corpus we will apply lemmatizing
        """
        super().__init__('cranfield', stemming, lemmatizing,)
        
                    
    def proccess_corpus(self):
        """Processing and analysis of the corpus
        """
        #data_path = self.path/'corpus/cran_corpus/cran.all.1400'
        
        dataset = ir_datasets.load("cranfield")
        for doc in dataset.docs_iter():
            doc_id = int(doc[0])
            doc_tittle = doc[1]
            doc_text = doc[2]
            doc_author = doc[3]
            
            """with open(data_path, 'r') as f:
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
                doc_text = aux.group(5)"""
                
            doc = document(doc_id,doc_tittle,doc_author,doc_text)
                                        
            clean_doc = clean_text(doc.text, self.stemming, self.lemmatizing)
            
            for word in set(clean_doc):
                self.all_words_counter[word] = self.all_words_counter.get(word, 0) + 1
                
            self.documents_words_counter[doc] = Counter(clean_doc)
