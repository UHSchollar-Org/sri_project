import pickle as plk
import re
import ir_datasets
from collections import Counter
from document import corpus, document
from text_processing import *

class cran_corpus(corpus):
    """A small corpus of 1,400 scientific abstracts.
    """

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
        
        dataset = ir_datasets.load("cranfield")
        for doc in dataset.docs_iter():
            doc_id = int(doc[0])
            doc_tittle = doc[1]
            doc_text = doc[2]
            doc_author = doc[3]
                            
            doc = document(doc_id,doc_tittle,doc_author,doc_text)
                                        
            clean_doc = clean_text(doc.text, self.stemming, self.lemmatizing)
            
            for word in set(clean_doc):
                self.all_words_counter[word] = self.all_words_counter.get(word, 0) + 1
                
            self.documents_words_counter[doc] = Counter(clean_doc)
