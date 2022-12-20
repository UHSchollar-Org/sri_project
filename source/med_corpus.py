import pickle as plk
import re
from collections import Counter
from document import corpus, document
from text_processing import *

class med_corpus(corpus):
    """Medical articles from Medline. This collection was used by TREC Genomics 2004-05 
    (2004 version of dataset) and by TREC Precision Medicine 2017-18 (2017 version).
    """
    
    PATTERN = r'(\d+)\n\.W(.*)'
    pattern = re.compile(PATTERN,re.DOTALL) 

    def __init__(self, stemming : bool, lemmatizing : bool) -> None:
        """Create a med_corpus using corpus.__init__

        Args:
            stemming (bool): True if when processing the corpus we will apply stemming
            lemmatizing (bool): True if when processing the corpus we will apply lemmatizing
        """
        super().__init__('medline', stemming, lemmatizing,)
    
    def proccess_corpus(self):
        """Processing and analysis of the corpus
        """
        data_path = self.path/'corpus/med/MED.ALL'
        
        with open(data_path, 'r') as f:
                texts = f.read().split('\n.I')
                for article in texts:
                    aux = self.pattern.search(article)
                    doc_id = int(aux.group(1))
                    doc_tittle = 'unknown'
                    doc_author = 'unknown'
                    doc_text = aux.group(2)
                    
                    doc = document(doc_id,doc_tittle,doc_author,doc_text)
                    self.docs_count+=1
                    
                    clean_doc = clean_text(doc.text, self.stemming, self.lemmatizing)
                
                    for word in set(clean_doc):
                        self.all_words_counter[word] = self.all_words_counter.get(word, 0) + 1
                
                    self.documents_words_counter[doc] = Counter(clean_doc)
