from document import corpus, document, query
from models import generic_mri_model
from typing import Dict, Tuple
from statistics import mean
import ir_datasets
import re
import matplotlib.pyplot as plt
import numpy as np

PLT_COLORS = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]

def evaluate(_corpus : corpus, model : generic_mri_model):
    """Evaluate a model given a corpus

    Args:
        corpus (corpus): corpus with which the model will be evaluated
        model (generic_mri_model): model to evaluate

    Returns:
        tuple(precision_list, recall_list, f1_list, fallout_list): measurement results matrixes
        *precision_list, recall_list, f1_list and fallout_list are lists that contain in each row the results 
        of their respective measurements to a query for the different tops*

    """
    precision_list = []
    recall_list = []
    f1_list = []
    fallout_list = []
    
    queries = get_queries(_corpus)
    query_doc_relevance = get_query_doc_relevance(_corpus)
    for query in queries:
        r = model.exec_query(query)
        total_rel_doc, total_irrel_doc = get_total_relevant_documents(query,query_doc_relevance, _corpus.docs_count)
        #region Initializing Results Lists
        precision_top = []
        #query precision results for the different tops----------precision_top[i] is the query precision result for top=(i+1)*2
        recall_top = []
        #query recall results for the different tops-------------recall_top[i] is the query recall result for top=(i+1)*2
        f1_top = []
        #query f1 results for the different tops-----------------f1_top[i] is the query f1 result for top=(i+1)*2
        fallout_top = []
        #query fallout results for the different tops------------fallout_top[i] is the query fallout result for top=(i+1)*2
        #endregion

        for top in range(2,52,2):
            top = min(top,len(r))
            rr, ir = get_relevant_docs_count(r,query,query_doc_relevance,top) #number of relevant documents retrieved, number of relevant documents retrieved.
            try:
                precision = rr/top
            except:
                precision = 0
            precision_top.append(precision)
            try:
                recall = rr/total_rel_doc
            except:
                recall = 0
            recall_top.append(recall)
            f1 = calculate_measure_f(1,precision,recall)
            f1_top.append(f1)
            fallout = ir/total_irrel_doc
            fallout_top.append(fallout)
            
        precision_list.append(precision_top)
        recall_list.append(recall_top)
        f1_list.append(f1_top)
        fallout_list.append(fallout_top)
            
    names = ['Precisicion', 'Recall', 'F1', 'Fallout']
    tops = [n for n in range(2,51,2)]
    return draw_results((precision_list, recall_list, f1_list, fallout_list), model.__class__.__name__, _corpus.name, names, tops)

def draw_results(results : tuple, model_name, corpus_name, names, tops):
    """Graph the results obtained in the evaluation of the models
    Args:
        measure (list[list]): matrix of measure values
    """
    fig, axs = plt.subplots(2, 2, figsize=(12, 7))
    for ax in axs.flatten():
        ax.grid(True)
        ax.set_xlabel("Top")
        ax.set_ylabel("Mean")
    fig.suptitle(f'{corpus_name} - {model_name}', fontsize=16)
    for i, measure in enumerate(results):
        name = names[i]
        color = PLT_COLORS[i % len(PLT_COLORS)]
        plt.sca(axs[i//2, i%2])        
        draw_measure_result(measure, tops, names[i], color)
        i += 1
        plt.tight_layout()
    for ax in axs.flatten():
        ax.legend()
    
    plt.show()  
    return fig
    
def draw_measure_result(measure : list[list], tops, title, color, show: bool = False):
    """Graph the results of the specific measure

    Args:
        measure (list[list]): measurement results according to the different tops
        tops (_type_): 
        title (_type_): measure name
        color (_type_): color to use for plotting
        show (bool, optional): True if the graph will be displayed. Defaults to False.
    """
    mean_vals = []
    std_vals = []
    min_vals = []
    max_vals = []
    
    for top in range(len(measure[0])):
        itop_values : set = set()
        for query in range(len(measure)):
            itop_values.add(measure[query][top])
        max_vals.append(max(itop_values))
        min_vals.append(min(itop_values))
        mean_vals.append(mean(itop_values))
        std_vals.append(np.std(list(itop_values)))
    

    plt.plot(
        tops,
        max_vals,
        "--",
        label=f"{title} max",
        alpha=0.5,
        color=color,
    )
    plt.fill_between(
        tops,
        np.array(mean_vals) - np.array(std_vals),
        np.array(mean_vals) + np.array(std_vals),
        alpha=0.4,
        color=color,
        label=f"{title} std",
    )
    plt.plot(tops, mean_vals, label=f"Avg. {title}", color=color)
    plt.plot(tops,min_vals,"--",label=f"{title} min",alpha=0.5, color=color,)
    plt.grid()
    plt.xlabel("Top")
    plt.ylabel(title)
    plt.title(title)
    plt.legend(loc="best")
    if show:
        plt.show()

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
            
def get_relevant_docs_count(r , _query:query, query_doc_relevance: Dict[Tuple[int,int], int], top:int) -> int:
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
        doc, _ = r[i]
        try:
            rel = query_doc_relevance[_query.id,doc.id]
            if rel > 2:
                rr +=1
            else:
                ir+=1
        except:
            ir+=1
    
    return rr, ir

def get_queries(_corpus:corpus):
    """
    Returns a list of test queries available for the given corpus
    """
    match _corpus.name:
        case 'cranfield':
            dataset = ir_datasets.load("cranfield")
            return get_dataset_queries(dataset)
        case 'cisi':
            queries_path = _corpus.path/'corpus/cisi/CISI.QRY'
            return read_queries_file(queries_path)
        case 'medline':
            queries_path = _corpus.path/'corpus/med/MED.QRY'
            return read_queries_file(queries_path)
        case other:
            raise Exception('Sorry but we can\'t evaluate this corpus')

def get_query_doc_relevance(_corpus:corpus):
    match _corpus.name:
        case 'cranfield':
            """qrel_path = _corpus.path/'corpus/cran_corpus/cranqrel'
            return get_cranfield_qrel(qrel_path)"""
            dataset = ir_datasets.load("cranfield")
            return get_dataset_qrels(dataset)
        case 'cisi':
            qrel_path = _corpus.path/'corpus/cisi/CISI.REL'
            return get_cisi_qrels(qrel_path)
        case 'medline':
            qrel_path = _corpus.path/'corpus/med/MED.REL.OLD'
            return get_cisi_qrels(qrel_path)
            #MED.REL.OLD has the same format as CISI.REL, so get_cisi_qrel() is reused        
        case other:
            raise Exception('Sorry but we can\'t evaluate this corpus')

def get_cranfield_qrel(qrel_path) -> dict:
    """Given an address, it reads the relevance cranfield file and returns the dictionary 
    that relates the query-doc-relevance.

    Args:
        qrel_path (path): Path where the cranfield file containing the relevance of the 
        documents for the query is located

    Returns:
        dict: Dictionary that has as key the tuple query-document and as value 
        the relevance of that document for that query
    """
    result = {}
    with open(qrel_path, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            aux = line.split()
            result[int(aux[0]),int(aux[1])] = int(aux[2])
        return result
    
def get_cisi_qrels(qrel_path) -> dict:
    """Given an address, it reads the relevance cisi file and returns the dictionary 
    that relates the query-doc-relevance.

    Args:
        qrel_path (path): Path where the cisi file containing the relevance of the 
        documents for the query is located

    Returns:
        dict: Dictionary that has as key the tuple query-document and as value 
        the relevance of that document for that query
    """
    result = {}
    with open(qrel_path, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            aux = line.split()
            result[int(aux[0]),int(aux[1])] = 4
            #we interpret the relevance as binary, if the query-document tuple is found,
            #that document is considered relevant for the query, therefore it is assigned 4
        return result

def get_dataset_queries(dataset):
    queries = []
    
    for dataset_query in dataset.queries_iter():
        new_query = query(int(dataset_query[0]),dataset_query[1])
        queries.append(new_query)
        
    return queries

def get_dataset_qrels(dataset):
    qrels = {}
    
    for dataset_qrel in dataset.qrels_iter():
        qrels[int(dataset_qrel[0]),int(dataset_qrel[1])] = int(dataset_qrel[2])
    
    return qrels

def read_queries_file(queries_path) -> list:
    """Given an address, it reads the queries file and returns the list of queries read

    Args:
        queries_path (path): Path where the file containing the queries is located

    Returns:
        list: list of queries read
    """
    PATTERN1 = r'(\d+)\n\.W\n(.*)'
    pattern1 = re.compile(PATTERN1,re.DOTALL)
    PATTERN2 = r'(\d+)\n\.T\n(.*)\n\.A\n(.*)\n\.W\n(.*)'
    pattern2 = re.compile(PATTERN2,re.DOTALL)
    PATTERN3 = r'(\d+)\n\.T\n(.*)\n\.A\n(.*)\n\.W\n(.*)\n\.B\n(.*)'
    pattern3 = re.compile(PATTERN3,re.DOTALL)
    
    with open(queries_path, 'r') as f:
            result = []
            raw_queries = f.read().split('\n.I')
            for raw_query in raw_queries:
                aux = pattern1.search(raw_query)
                if aux is not None:
                    query_id = int(aux.group(1))
                    text = aux.group(2)
                    qry = query(query_id, text)
                    result.append(qry)
                else:
                    aux = pattern3.search(raw_query)
                    try:
                        query_id = int(aux.group(1))
                        text = aux.group(4)
                        qry = query(query_id, text)
                        result.append(qry)
                    except:
                        aux = pattern2.search(raw_queries)
                        query_id = int(aux.group(1))
                        text = aux.group(4)
                        qry = query(query_id, text)
                        result.append(qry)
            return result
