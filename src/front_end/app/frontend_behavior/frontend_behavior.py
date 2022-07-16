#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Olga Patricia Nieto, Daniel De León, Ernesto Alejandro Martínez, Alex Fabián Gómez, Marcela Sánchez Jiménez, Daniel Hernández, and David Aurelia Ayala Usma
# Created Date: 2022-06-05
# Version = 0.0.1
# ---------------------------------------------------------------------------

## Description
"""Front end behavior functions.
"""
# ---------------------------------------------------------------------------
## Required libraries

from urllib.request import urlopen
from datetime import datetime
import pandas as pd
import numpy as np
import time
import sys

# ---------------------------------------------------------------------------
## Static attributes


#---------------------------------------------------------------------------------------------------------------------------------
##Module functions 

def filtered_topics_list(series):
    
    preprocess = series.astype('string').dropna()
    preprocess = ' '.join(preprocess.unique()).lower()
    preprocess = list(set(preprocess.split()))

    stopwords = [line.decode('UTF-8').strip() for line in urlopen('https://raw.githubusercontent.com/Alir3z4/stop-words/master/spanish.txt')]
    list_terms = [word.replace(',', '') for word in preprocess if word not in stopwords and word != '' and word != 'None']
    
    return list_terms

def topic_co_ocurrence_aggregation(df, start_year, end_year):
    sum = None
    year_range = [*range(start_year, end_year+1)]
    year_range = list(map(str, year_range))
    sum = df[year_range].sum(axis=1)
    return sum

# def cytoscape_selector_topics(df, *args):
#     topics = set()

#     for column in args:
#         topics.update(df[column].unique())

#     topics = list(topics)
#     return topics

def conpes_list_by_type(df, start_year, end_year, doc_type, search_terms):

    df['approvaldate'] = pd.to_datetime(df['approvaldate'])
    if(len(search_terms) > 0):
        df = df.sort_values(by='counttopic',ascending=False)
        lower_search_terms=[x.lower() for x in search_terms]
        filtered_conpes_df = df[(df['documenttype'] == doc_type) & (df['year'] >= start_year) & (df['year'] <= end_year) & (df['topic'].isin(lower_search_terms))]
    else:
        filtered_conpes_df = df[(df['documenttype'] == doc_type) & (df['year'] >= start_year) & (df['year'] <= end_year)]
    conpes_list = list(filtered_conpes_df['conpesno'].unique())
    conpes_list = ['CONPES No. ' + doc for doc in conpes_list]
    conpes_list = np.asarray(conpes_list)
    return conpes_list


### ---------------------------------------------------------------- ###
## Main function

def frontend_behavior():
    return

### ---------------------------------------------------------------- ###
#Código que se va a ejecutar cuando se llame por línea de comandos
if __name__ == '__main__':    
    frontend_behavior()