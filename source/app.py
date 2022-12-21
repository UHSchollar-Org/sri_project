from statistics import mean
import streamlit as st
import pandas as pd
import os
from pathlib import Path
from document import document, query
from models import vector_model, boolean_model, fuzzy_model
from txt_corpus import txt_corpus
from cran_corpus import cran_corpus
from cisi_corpus import cisi_corpus
from med_corpus import med_corpus
from twenty_news_corpus import twenty_news_corpus
import configparser

from eval import evaluate

state_vars = [
    "model",
    "str_model",
    "corpus",
    "str_corpus",
    "str_query"
]

st.set_page_config(layout="wide", page_title="Karelio's Information Retrieval System")   

#region Reading all settings
config = configparser.ConfigParser()
config.read('source/config.ini')

steamming = config.getboolean('DEFAULT','STEAMMING')
lemmatizing = config.getboolean('DEFAULT','LEMMATIZING')
datasets = eval(config['DEFAULT']['CORPUS'])
#endregion

#region Initializing values in Session State
for var in state_vars:
    if var not in st.session_state:
        st.session_state[var] = None
#endregion

#region Reseting values in Session State
def reset_search():
    st.session_state.results = []

def reset():
    st.session_state.str_query = ''
    st.session_state.corpus = None
    st.session_state.str_corpus = ''
    st.session_state.model = None
    st.session_state.str_model = ''
    
    reset_search()
#endregion
    
st.title("Information Retrieval System")

def show_result(result: document):
    doc_id = result.id
    expander_header = f"{doc_id} -- ".format(doc_id)
    if result.title != '':
        expander_header += result.title.capitalize()
    
        
        
    with st.expander(f"{expander_header}"):
        if result.title != '' :
            st.caption(f"**{result.title.upper()}**")
            
        if result.author != '':
            st.caption(f"**{result.author.upper()}**")
        
        st.markdown(result.text.capitalize())
        
reset()



if not datasets:
    st.write("No databases found")

#region Sidebar
st.sidebar.write("# Config :gear:")

dataset = st.sidebar.selectbox("Select a database", datasets)
if dataset != "-":
        if st.session_state.corpus is None or st.session_state.str_corpus != dataset:
            reset()
            
            corpus = None
            
            match dataset:
                case 'txt':
                    corpus = txt_corpus(steamming, lemmatizing)
                case 'Cranfield':
                    corpus = cran_corpus(steamming, lemmatizing)
                case '20NewsGroup':
                    corpus = twenty_news_corpus(steamming, lemmatizing)
                case 'CISI':
                    corpus = cisi_corpus(steamming, lemmatizing)
                case 'Medline':
                    corpus = med_corpus(steamming, lemmatizing)
                
            st.session_state.corpus = corpus
            st.session_state.str_corpus = dataset
    


str_model = st.sidebar.selectbox("Choose a retrieval model ", ["-", "Vectorial", "Boolean", "Fuzzy"])
if not str_model:
    st.error("Please select one model.")
if dataset != "-":
    model = None
        
    match str_model:
        case 'Boolean':
            model = boolean_model(st.session_state.corpus)
        case 'Vectorial':
            model = vector_model(st.session_state.corpus)
        case 'Fuzzy':
            model = fuzzy_model(st.session_state.corpus)
    st.session_state.model = model
    st.session_state.str_model = str_model
       
def make_visual_evaluation():
    if st.session_state.corpus is None:
        st.error('Please select a dataset first')
    elif st.session_state.model is None:
        st.error('Please select an ir model first')
    else:
        st.pyplot(evaluate(st.session_state.corpus, st.session_state.model))


#endregion
   
col1, col2 = st.columns([2,2])
with col1:
    st.write("###  🔍 Enter a query")
    str_query = st.text_input("", placeholder="Write your query here")
    st.session_state.str_query = str_query
    if  st.session_state.model != None and str_query != "":
        _query = query(0,str_query)
        result = st.session_state.model.exec_query(_query)
        st.write(f"Found {len(result)} results")
    
        for r in result:
            show_result(r[0])
with col2:
    if st.session_state.str_corpus == 'Cranfield' or st.session_state.str_model == 'Vectorial':
        if st.button("Show evaluation measures statistics 📈"):
            make_visual_evaluation()