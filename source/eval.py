from document import corpus, document, query
from models import generic_mri_model
from typing import Dict, Tuple
import re

def evaluate(corpus : corpus, model : generic_mri_model):
    """Evaluate a model given a corpus

    Args:
        corpus (corpus): corpus with which the model will be evaluated
        model (generic_mri_model): model to evaluate
    """
    precision_list = []
    recall_list = []
    f1_list = []
    fallout_list = []
    
    queries = get_queries(corpus)
    query_doc_relevance = get_query_doc_relevance(corpus)
    for query in queries:
        r = model.exec_query(query)
        total_rel_doc, total_irrel_doc = get_total_relevant_documents(query,query_doc_relevance, corpus.docs_count)
        top = min(20,len(r))
        rr, ir = get_relevant_docs_count(r,query,query_doc_relevance,top) #number of relevant documents retrieved, number of relevant documents retrieved.
        precision = rr/top
        precision_list.append(precision)
        try:
            recall = rr/total_rel_doc
        except:
            recall = 0
        recall_list.append(recall)
        f1 = calculate_measure_f(1,precision,recall)
        f1_list.append(f1)
        fallout = ir/total_irrel_doc
        fallout_list.append(fallout)
    
    return precision_list, recall_list, f1_list, fallout_list

def calculate_measure_f(beta : float, precision : float, recall : float) -> float:
    """Return the result of calculating the measure f

    Args:
        beta (float): _description_
        precision (float): _description_
        recall (float): _description_

    Returns:
        float: _description_
    """
    return (1 + beta**2)/((1/precision)+(beta**2/recall)) if recall > 0 else 0

def get_total_relevant_documents(query:query, query_doc_relevance : Dict[Tuple[int,int], int], total_docs_count : int ) -> int:
    """Return the number of relevant documents and the number of irrelevant documents

    Args:
        query (query): query to be evaluated
        query_doc_relevance (Dict[Tuple[int,int], int]): _description_

    Returns:
        int: _description_
    """
    relevant = 0
    for item in query_doc_relevance.keys():
        if query.id == item[0]: 
            if query_doc_relevance[item] > 2:
                relevant+=1
    irrelevant = total_docs_count - relevant
        
    return relevant, irrelevant
            
def get_relevant_docs_count(r , query:query, query_doc_relevance: Dict[Tuple[int,int], int], top:int) -> int:
    """Return the number of relevant documents retrieved and irrelevant retrieved

    Args:
        r : documents retrieved from the given query
        query (query): query to evaluate
        query_doc_relevance (Dict[Tuple[int,int], int]): query-document-relevance relationship
        top (int): max number of documents retrieved

    Returns:
        int: number of relevant documents retrieved, number of irrelevant documents retrieved
    """
    rr = 0
    ir = 0
    
    for i in range(top):
        doc, rank = r[i]
        try:
            rel = query_doc_relevance[query.id,doc.id]
            if rel > 2:
                rr +=1
            else:
                ir+=1
        except:
            ir+=1
    
    return rr, ir

def get_queries(corpus:corpus):
    """
    Returns a list of test queries available for the given corpus
    """
    match corpus.name:
        case 'cranfield':
            queries_path = corpus.path/'corpus/cran_corpus/cran.qry'
            return get_cranfield_queries(queries_path)
        case other:
            raise Exception('Sorry but we can\'t evaluate this corpus')

def get_query_doc_relevance(corpus:corpus):
    match corpus.name:
        case 'cranfield':
            qrel_path = corpus.path/'corpus/cran_corpus/cranqrel'
            return get_cranfield_qrel(qrel_path)
        case other:
            raise Exception('Sorry but we can\'t evaluate this corpus')

def get_cranfield_qrel(qrel_path):
    result = {}
    with open(qrel_path, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            aux = line.split()
            result[int(aux[0]),int(aux[1])] = int(aux[2])
        return result
    
def get_cranfield_queries(queries_path):
    PATTERN = r'(\d+)\n\.W\n(.*)'
    pattern = re.compile(PATTERN,re.DOTALL)
    with open(queries_path, 'r') as f:
            result = []
            raw_queries = f.read().split('\n.I')
            for raw_query in raw_queries:
                aux = pattern.search(raw_query)
                query_id = int(aux.group(1))
                text = aux.group(2)
                qry = query(query_id, text)
                result.append(qry)
            return result