import pickle as pk
from collections import Counter

from document import corpus, document
from text_processing import *

class twenty_news_corpus(corpus):
    
    def __init__(self, steamming, lemmatizing):
        self.themes = ['alt.atheism','comp.graphics','comp.os.ms.ms-windows.misc','comp.sys.ibm.pc.hardware','comp.sys.mac.hardware',
                       'comp.windows.x','msic.forsale','rec.autos','rec.motorcycles','rec.sport.baseball','rec.sport.hockey','sci.crypt',
                       'sci.electronics','sci.space','soc.religion.christian','talk.politics.guns','talk.politics.mideast',
                       'talk.politics.misc','talk.religion.misc']
        return super().__init__("20news", steamming, lemmatizing)
    
    def proccess_corpus(self):
        for theme in self.themes:
            data_path = self.path/'corpus/20news-18828'/theme
            path_list = data_path.glob('*')
            
            for file in path_list:
                with open(file, 'r') as f:
                    text1 = f.readline()
                    text2 = f.readline()
                    if text1.split()[0]=='From:':
                        doc_tittle = text2.split(':',1)[1].split('\n')[0]
                        doc_author = text1.split(':',1)[1].split('\n')[0]
                        doc = document(file.name,doc_tittle,doc_author,f.read())
                    else:
                        doc_tittle = text1.split(':',1)[1].split('\n')[0]
                        doc_author = text2.split(':',1)[1].split('\n')[0]
                        doc = document(file.name,doc_tittle,doc_author,f.read())
                clean_doc = clean_text(doc.text, self.stemming, self.lemmatizing)
                
                for word in set(clean_doc):
                    self.all_words_counter[word] = self.all_words_counter.get(word, 0) + 1
                
                self.documents_words_counter[doc] = Counter(clean_doc)  