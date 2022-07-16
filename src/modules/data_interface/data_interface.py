#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Olga Patricia Nieto, Daniel De León, Ernesto Alejandro Martínez, Alex Fabián Gómez, Marcela Sánchez Jiménez, Daniel Hernández, and David Aurelia Ayala Usma
# Created Date: 2022-06-05
# Version = 0.0.1
# ---------------------------------------------------------------------------

## Description
"""Module to connect to a PostgreSQL DB and execute Querys.
"""
# ---------------------------------------------------------------------------
## Required libraries

from sqlalchemy.dialects import postgresql
from urllib.request import urlopen
from datetime import datetime
import sqlalchemy as sql
import pandas as pd
import numpy as np
import time
import sys

# ---------------------------------------------------------------------------
## Static attributes
#### DB Credentials
__USER__ = 't19_admin'
__HOST__ = 't19-db-conpes.postgres.database.azure.com'
__PASSWORD__ = 'W5txYW5RfHKDJ+9'
__DB__ = 'postgres'


    # ---------------------------------------------------------------------------
## Module functions
#### Creating and populating tables: Documents, Keywords, and Classification

def db_connection():
    """
    Populating Documents table with the contents csv.

    Returns:
        db_conn (SQLAlchemy Connection): _description_
    """    
    
    conn = None
    
    print('Opening DB connection')
    alchemyEngine = sql.create_engine('postgresql+psycopg2://{user}:{password}@{host}/{db}'.format(host=__HOST__, user=__USER__, db=__DB__, password=__PASSWORD__),
                    connect_args={'sslmode': 'require'})
    print('Engine created')
    conn = alchemyEngine.connect().execution_options(autocommit=True)
    print('DB connection successful!')
    
    return conn

def documents_topics_df(db_conn,
     query = """
     SELECT d.conpesno,
            d.title,
            d.approvaldate,
            d.documenttype,
            d.URL,
            t.topic,
            t.counttopic
        FROM documents AS d
            LEFT JOIN topics AS t
                    ON t.conpesno = d.conpesno"""):

    """
    This function performs a SQL query to the DB joining the Documents and the Topics tables.

    Args:
        db_conn (SQLAlchemy Connection): _description_
        query (str, optional): _description_. 'Defaults to SELECT * FROM Documents AS d LEFT JOIN Topics AS t ON t.conpesno = d.conpesno'.

    Returns:
        Pandas DataFrame: Containing the join of Documents and Topics tables.
    """

    df = pd.read_sql_query(query, db_conn)
    df['approvaldate'] = pd.to_datetime(df['approvaldate'])
    df['year'] = df['approvaldate'].dt.year
    return df

def loading():
    db_conn = db_connection()
    df = documents_topics_df(db_conn)
    topics = get_procolombia_topics(db_conn)
    return df, topics

def get_years_list(df):
    years = list(set(df['year']))
    return years

def get_top_n_topics_over_time(df, n = 5):

    df_topics_general = df.groupby(['topic'], as_index=False).sum(['counttopic'])
    df_topics_general = df_topics_general.sort_values(by='counttopic', ascending = False).head(n)

    topics = df_topics_general['topic']

    df_lines = df.groupby(['year', 'topic'], as_index=False).sum(['counttopic'])
    df_lines = df_lines.sort_values(by='counttopic', ascending = False)
    df_lines = df_lines[df_lines['topic'].isin(topics)]
    
    return df_lines

def get_search_topics_over_time(df, search_terms):

    df_lines = df.groupby(['year', 'topic'], as_index=False).sum(['counttopic'])
    df_lines = df_lines.sort_values(by='counttopic', ascending = False)
    df_lines = df_lines[df_lines['topic'].isin(search_terms)]
    
    return df_lines

def get_procolombia_topics(db_conn,
     query = """
     SELECT axiscat
        FROM ProColombiaAxis"""):
    
    df = pd.read_sql_query(query, db_conn)
    topics_series = df['axiscat']
    return topics_series

def get_conpes_paragraphs(conpesno):

    db_conn = db_connection()
    
    get_string = sql.text("""SELECT page, paragraph, text FROM Paragraphs WHERE CONPESNo = :CONPESNo """)
    get_string = get_string.bindparams(CONPESNo = conpesno)
    get_string = get_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})

    document_elements = pd.read_sql_query(get_string, db_conn)
    document_elements = document_elements.sort_values(by=['page', 'paragraph'], ascending=True)
    return document_elements

def get_conpes_summary(conpesno):

    db_conn = db_connection()
    
    get_string = sql.text("""SELECT Summary FROM Documents WHERE CONPESNo = :CONPESNo """)
    get_string = get_string.bindparams(CONPESNo = conpesno)
    get_string = get_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})

    executive_sumary = pd.read_sql_query(get_string, db_conn)
    return executive_sumary

def get_conpes_topics(conpesno):

    db_conn = db_connection()
    
    get_string = sql.text("""SELECT Topic, CountTopic FROM Topics WHERE CONPESNo = :CONPESNo """)
    get_string = get_string.bindparams(CONPESNo = conpesno)
    get_string = get_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})

    conpes_topics = pd.read_sql_query(get_string, db_conn)
    return conpes_topics

def get_conpes_keywords():

    db_conn = db_connection()
    
    get_string = sql.text("""SELECT CONPESNo, Text FROM Keywords""")
    get_string = get_string.bindparams()
    get_string = get_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})

    conpes_keywords = pd.read_sql_query(get_string, db_conn)
    return conpes_keywords

def get_conpes_table(db_conn):
    
    get_string = sql.text("""SELECT * FROM Topics""")
    topics_table = pd.read_sql_query(get_string, db_conn)
    return topics_table

### ---------------------------------------------------------------- ###
## Main function

def data_interface():
    """
    """
    print('Holi!')
    db_conn = db_connection()
    start = time.time()
    df = documents_topics_df(db_conn)
    end = time.time()
    print('Database queried in ' + str(end-start) + ' seconds')
    print('The size of the Documents and Topics DataFrame is: ' + str(sys.getsizeof(df)) + ' bytes')
    ola = get_top_n_topics_over_time(df)
    db_conn.close()

### ---------------------------------------------------------------- ###
#Código que se va a ejecutar cuando se llame por línea de comandos
if __name__ == '__main__':    
    data_interface()
    df = get_conpes_keywords()
    #summary = get_conpes_summary("4080")
    #if summary.empty:
    #    print("Sin resumen")
    #else:
    #    print(summary)
    print(df.shape)
    db_conn = db_connection()
    db_conn.close()