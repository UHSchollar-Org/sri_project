import pickle as plk
import re
from collections import Counter
from document import corpus, document
from text_processing import *

class cisi_corpus(corpus):
    """The data were collected by the Centre for Inventions and Scientific Information ("CISI") 
    and consist of text data about 1,460 documents and 112 associated queries. Its purpose is 
    to be used to build models of information retrieval where a given query will return a list 
    of document IDs relevant to the query. The file "CISI.REL" contains the correct list 
    (ie. "gold standard" or "ground proof") of query-document matching and your model can be 
    compared against this "gold standard" to see how it has performed.
    """
    
    PATTERN = r'(\d+)\n\.T(.*)\n\.A(.*)\n\.W(.*)\n\.X(.*)'
    pattern = re.compile(PATTERN,re.DOTALL) 

    def __init__(self, stemming : bool, lemmatizing : bool) -> None:
        """Create a cisi_corpus using corpus.__init__ and

        Args:
            stemming (bool): True if when processing the corpus we will apply stemming
            lemmatizing (bool): True if when processing the corpus we will apply lemmatizing
        """
        super().__init__('cisi', stemming, lemmatizing,)
    
    def proccess_corpus(self):
        """Processing and analysis of the corpus
        """
        data_path = self.path/'corpus/cisi/CISI.ALL'
        
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
                    doc_text = aux.group(4)
                    cross_references = aux.group(5)
                    
                    doc = document(doc_id,doc_tittle,doc_author,doc_text)
                    
                    clean_doc = clean_text(doc.text, self.stemming, self.lemmatizing)
                
                    for word in set(clean_doc):
                        self.all_words_counter[word] = self.all_words_counter.get(word, 0) + 1
                
                    self.documents_words_counter[doc] = Counter(clean_doc)
