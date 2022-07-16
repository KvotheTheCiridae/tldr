#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Olga Patricia Nieto, Daniel De León, Ernesto Alejandro Martínez, Alex Fabián Gómez, Marcela Sánchez Jiménez, Daniel Hernández, and David Aurelia Ayala Usma
# Created Date: 2022-06-05
# Version = 0.0.1
# ---------------------------------------------------------------------------

## Description
"""Module to connect to a PostgreSQL DB and retrieving data.
"""
# ---------------------------------------------------------------------------
## Required libraries

from sqlalchemy.dialects import postgresql
from datetime import datetime
import sqlalchemy as sql
import pandas as pd
import numpy as np
import itertools
import psycopg2
import time
import math
import sys
import json

# ---------------------------------------------------------------------------
## Own modules

sys.path.append('/home/azureuser/devenv/CONPES_Explorer/src/modules/pdf_processor')
sys.path.append('/home/azureuser/devenv/CONPES_Explorer/src/modules/topic_modeling')
import pdf_processor as pdf
import topic_modeling as tm

# ---------------------------------------------------------------------------
## Static attributes
#### DB Credentials
__USER__ = 't19_admin'
__HOST__ = 't19-db-conpes.postgres.database.azure.com'
__PASSWORD__ = 'W5txYW5RfHKDJ+9'
__DB__ = 'postgres'

# ---------------------------------------------------------------------------
## Module functions

####  ----- Functions to create tables  ----- ####

def db_connection():
    """
    Populating Documents table with the contents csv.

    Returns:
        db_conn (SQL Alchemy Connection): _description_
    """    
    
    conn = None
    
    print('Opening DB connection')
    alchemyEngine = sql.create_engine('postgresql+psycopg2://{user}:{password}@{host}/{db}'.format(host=__HOST__, user=__USER__, db=__DB__, password=__PASSWORD__),
                    connect_args={'sslmode': 'require'})
    print('Engine created')
    conn = alchemyEngine.connect().execution_options(autocommit=True)
    print('DB connection successful!')
    
    return conn

def creating_main_documents_table(db_conn):
    """
    Creating Documents table.

    Args:
        db_conn (SQL Alchemy Connection): _description_
    """    
    
    #Creating the Documents table scheme
    db_conn.execute('DROP TABLE IF EXISTS Documents CASCADE;')
    db_conn.execute('CREATE TABLE Documents (CONPESNo VARCHAR NOT NULL, Title VARCHAR, ApprovalDate DATE, DocumentType VARCHAR, URL VARCHAR, URLPAS VARCHAR, URLOthers VARCHAR, Summary VARCHAR, PRIMARY KEY(CONPESNo));')
    print('Created table Documents!')
    return

def creating_paragraphs_table(db_conn):
    """
    Creating Paragraphs table.

    Args:
        db_conn (SQL Alchemy Connection): _description_
    """    

    db_conn.execute('DROP TABLE IF EXISTS Paragraphs;')
    db_conn.execute('CREATE TABLE Paragraphs (ParagraphId SERIAL, CONPESNo VARCHAR, Page INTEGER, Paragraph INTEGER, Text VARCHAR, PRIMARY KEY(ParagraphId), FOREIGN KEY(CONPESNo) REFERENCES Documents(CONPESNo));')
    print('Created table Paragraphs!')
    return

def creating_classify_table(db_conn):
    """
    Creating Classification table.

    Args:
        db_conn (SQL Alchemy Connection): _description_
    """    

    db_conn.execute('DROP TABLE IF EXISTS Classification;')

    db_conn.execute('CREATE TABLE Classification (ClassId SERIAL, CONPESNo VARCHAR, Classification VARCHAR, PRIMARY KEY(ClassId), FOREIGN KEY(CONPESNo) REFERENCES Documents(CONPESNo));')
    print('Created table Classification!')
    return

def creating_keywords_table(db_conn):
    """
    Creating Keywords table.

    Args:
        db_conn (SQL Alchemy Connection): _description_
    """    

    db_conn.execute('DROP TABLE IF EXISTS Keywords;')

    db_conn.execute('CREATE TABLE Keywords (KeywordsId SERIAL, CONPESNo VARCHAR, Text VARCHAR, PRIMARY KEY(KeywordsId), FOREIGN KEY(CONPESNo) REFERENCES Documents(CONPESNo));')
    print('Created table Keywords!')
    return

def creating_topics_table(db_conn):
    """
    Creating Topics table.

    Args:
        db_conn (SQL Alchemy Connection): _description_
    """    

    db_conn.execute('DROP TABLE IF EXISTS Topics;')
    print('Finished dropping table (if existed)')

    #Creating the Documents table scheme
    db_conn.execute('CREATE TABLE Topics (TopicId SERIAL, Topic VARCHAR NOT NULL, CONPESNo VARCHAR, CountTopic INTEGER, PRIMARY KEY(TopicID), FOREIGN KEY(CONPESNo) REFERENCES Documents(CONPESNo));')
    print('Created table Topics!')
    return


def creating_econlit_table(db_conn):
    """
    Creating econlit table.

    Args:
        db_conn (SQL Alchemy Connection): _description_
    """    

    db_conn.execute('DROP TABLE IF EXISTS Econlit;')
    print('Finished dropping table (if existed)')

    #Creating the Documents table scheme
    db_conn.execute('CREATE TABLE Econlit (EconlitId SERIAL, Code VARCHAR NOT NULL, Description VARCHAR, PRIMARY KEY(EconlitId));')
    print('Created table Econlit!')
    return


def creating_ProColombiaAxis_table(db_conn):
    """
    Creating ProColombiaAxis table.

    Args:
        db_conn (SQL Alchemy Connection): _description_
    """    

    db_conn.execute('DROP TABLE IF EXISTS ProColombiaAxis;')
    print('Finished dropping table (if existed)')

    #Creating the Documents table scheme
    db_conn.execute('CREATE TABLE ProColombiaAxis (ProColombiaAxisId SERIAL, Axis VARCHAR NOT NULL, AxisCat VARCHAR, AxisTheme VARCHAR, PRIMARY KEY(ProColombiaAxisId));')
    print('Created table ProColombiaAxis!')
    return


####  ----- Functions to populate tables  ----- ####

def populating_documents_table(db_conn, csv):
    """
    Populating Documents table with the contents csv.

    Args:
        db_conn (SQL Alchemy Connection): _description_
        csv (File csv): A file csv with CONPES document
    """    
    
    table = pd.read_csv(csv)
    
    for _, row in table.iterrows():
 
        insert_string = sql.text("""INSERT INTO Documents (CONPESNo, Title, ApprovalDate, URL) VALUES (:CONPESNo, :title, :approvaldate, :url)""")
        insert_string = insert_string.bindparams(CONPESNo = row['Numero'], title = row['Titulo'], approvaldate = row['FechaAprobacion'], url = row['URL'])
        insert_string = insert_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
        db_conn.execute(insert_string)
        print('CONPES No.: ' + str(row['Numero']) + ' ' + 'loaded.')
    return

def populating_paragraphs_table(db_conn, row, df_paragraph):
    """
    Populating the table Paragraphs with the contents of a table.

    Args:
        db_conn (SQL Alchemy Connection): _description_
        row (Pandas Series): A CONPES document record
        df_paragraph (Pandas DataFrame): The processed text of the document 
    """    

    for n, paragraphrow in df_paragraph.iterrows():
        insert_string = sql.text("""INSERT INTO Paragraphs (CONPESNo, Page, Paragraph, Text) VALUES (:CONPESNo, :Page, :Paragraph, :Text)""")
        insert_string = insert_string.bindparams(CONPESNo = row['Numero'], Page = paragraphrow['Page'], Paragraph = paragraphrow['Paragraph'], Text = paragraphrow['Text'])
        insert_string = insert_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
        db_conn.execute(insert_string)
    return

def populating_classification_table(db_conn, row, df_classify):
    """
    Populating the table Classification with the econlit descriptors.

    Args:
        db_conn (SQL Alchemy Connection): _description_
        row (Pandas Series): A CONPES document record
        df_classify (Pandas DataFrame): The econlit descriptors of the CONPES document 
    """    

    for n, classifyrow in df_classify.iterrows():
        insert_string = sql.text("""INSERT INTO Classification (CONPESNo, Classification) VALUES (:CONPESNo, :Classification)""")
        insert_string = insert_string.bindparams(CONPESNo = row['Numero'], Classification = classifyrow['Value'])
        insert_string = insert_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
        db_conn.execute(insert_string)
    return

def populating_keywords_table(db_conn, row, df_keywords):
    """
    Populating the table Keywords with the keywords of the CONPES document.

    Args:
        db_conn (SQL Alchemy Connection): _description_
        row (Pandas Series): A CONPES document record
        df_keywords (Pandas DataFrame): The keywords of the CONPES document 
    """    

    for n, keywordsrow in df_keywords.iterrows():
        insert_string = sql.text("""INSERT INTO Keywords (CONPESNo, Text) VALUES (:CONPESNo, :Text)""")
        insert_string = insert_string.bindparams(CONPESNo = row['Numero'], Text = keywordsrow['Value'])
        insert_string = insert_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
        db_conn.execute(insert_string)
    return

def update_document_table(db_conn, row, type_doc, summary):
    """
    Update the table Documents with the type_doc and summary.

    Args:
        db_conn (SQL Alchemy Connection): _description_
        row (Pandas Series): A CONPES document record
        type_doc (scr): The type of the CONPES document
        summary (scr): The executive summary of the CONPES document 
    """    

    update_string = sql.text("""UPDATE Documents SET DocumentType = :DocumentType, Summary = :Summary WHERE CONPESNo = :CONPESNo""")
    update_string = update_string.bindparams(CONPESNo = row['Numero'], DocumentType = type_doc, Summary = summary)
    update_string = update_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
    db_conn.execute(update_string)
    return

def populating_tables(db_conn, csv):
    """
    Populating Paragraphs, Classification, Documents, and Keywords with the contents of a table.

    Args:
        db_conn (SQL Alchemy Connection): _description_
        csv (File csv): A file csv with CONPES document
    """    
    
    table = pd.read_csv(csv)
    path="/home/azureuser/devenv/CONPES_Explorer/shared/PDF/"
    for _, row in table.iterrows():
        #if _ >10:break
        Number = row['Numero']
        file = path + "CONPES_" + Number + ".pdf"

        df_paragraph, df_classify, df_keywords, type_doc, summary = pdf.pdf_reader(file)

        populating_paragraphs_table(db_conn, row, df_paragraph)
        print('Paragraphs processed for CONPES Document: ' + str(row['Numero']))
        
        populating_classification_table(db_conn, row, df_classify)
        print('Classification processed for CONPES Document: ' + str(row['Numero']))

        populating_keywords_table(db_conn, row, df_keywords)
        print('Keywords processed for CONPES Document: ' + str(row['Numero']))

        update_document_table(db_conn, row, type_doc, summary)
        print('Documents table updated for CONPES Document: ' + str(row['Numero']))

        populating_topics_table(db_conn,row,df_paragraph)
        print('Topics list processed for CONPES Document: ' + str(row['Numero']))

    return

def populating_econlit_table(db_conn,JsonPath):
    """
    Populating the table Econlit with the descriptions of the code corresponding to the document classification of the CONPES document saved on the Classification Table.

    Args:
        db_conn (SQL Alchemy Connection): _description_
        JsonPath (String): The string of the path to the Json file with the Code Description information 
    """   

    with open(JsonPath) as a:
        ListEconlit = json.load(a)

    for Dict in ListEconlit:
        insert_string = sql.text("""INSERT INTO Econlit (Code, Description) VALUES (:Code, :Description)""")
        insert_string = insert_string.bindparams(Code = Dict['code'], Description = Dict['description'])
        insert_string = insert_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
        db_conn.execute(insert_string)
    return

def populating_ProColombiaAxis_table(db_conn,csvPath):
    """
    Populating the table ProColombiaAxis with the categories and Themes corresponding to every ProColombia axis for topic sugestions.

    Args:
        db_conn (SQL Alchemy Connection): _description_
        csvPath (String): The string of the path to the csv file with the theme categories and axis information 
    """   

    table = pd.read_csv(csvPath)

    for n,row in table.iterrows():
        insert_string = sql.text("""INSERT INTO ProColombiaAxis (Axis, AxisCat, AxisTheme) VALUES (:Axis, :AxisCat, :AxisTheme)""")
        insert_string = insert_string.bindparams(Axis = row['Eje'], AxisCat = row['Categoria'], AxisTheme = row['Tema'])
        insert_string = insert_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
        db_conn.execute(insert_string)
    return

def populating_topics_table(db_conn,row,df_paragraph):
    """
    Populating the table Topics with the words processed from the CONPES document.

    Args:
        db_conn (SQL Alchemy Connection): _description_
        row (Pandas Series): A CONPES document record
        df_paragraph (Pandas DataFrame): The processed text of the document 
    """
    #Joining the text of each paragraph into a single string separated by a single space in order to process the complete document        
    CompleteText=df_paragraph['Text'].str.cat(sep=" ")
    #Get the doc with the tokens from spacy
    doc=tm.process_text(CompleteText)
    #Get the Token List with each non-stop-word token
    TokenList=tm.TokensOfNonStopWords(doc)
    #Process the each token from TokenList into a Json with keys as words and values as count of the word in the document
    JsonWordCount=tm.CountWordsLower(TokenList)

    for key, value in JsonWordCount.items():
        insert_string = sql.text("""INSERT INTO Topics (CONPESNo, Topic, CountTopic) VALUES (:CONPESNo, :Topic, :CountTopic)""")
        insert_string = insert_string.bindparams(CONPESNo = row['Numero'], Topic = key, CountTopic=value)
        insert_string = insert_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
        db_conn.execute(insert_string)
    return

####  ----- Clean-up functions  ----- ####

def cleaning_unique_low_freq_topics(db_conn,lowFreqThreshold):

    delete_string = sql.text("""DELETE FROM Topics WHERE Topic IN (SELECT Topic FROM Topics GROUP BY Topic HAVING COUNT(Topic)=1 AND SUM(CountTopic)<=:Numero)""")
    delete_string = delete_string.bindparams(Numero = lowFreqThreshold)
    delete_string = delete_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
    db_conn.execute(delete_string)

    return

####  -----Insert keyword in Topics ---- ####

def update_keywords_in_topics_table(db_conn):
    """
    Populating the table Topics with the keywords corresponding to every CONPES Docuement.

    Args:
        db_conn (SQL Alchemy Connection): _description_
    """   

    query_string = sql.text("""SELECT * FROM Keywords""")
    df_keywords = pd.read_sql_query(query_string, db_conn)
    #print(df_keywords)

    for n,row in df_keywords.iterrows():
        #Verify if topics exists
        query_string = sql.text("""SELECT * FROM Topics WHERE CONPESNo = :CONPESNo AND topic = :Topic""")
        query_string = query_string.bindparams(CONPESNo = row['conpesno'], Topic = row['text'])
        query_string = query_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
        result = pd.read_sql_query(query_string, db_conn)
        if result.empty:
            insert_string = sql.text("""INSERT INTO Topics (CONPESNo, Topic, CountTopic) VALUES (:CONPESNo, :Topic, :CountTopic)""")
            insert_string = insert_string.bindparams(CONPESNo = row['conpesno'], Topic = row['text'], CountTopic=1)
            insert_string = insert_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
            db_conn.execute(insert_string)
        else:
            new_count = result["counttopic"].values[0] + 1
            update_string = sql.text("""UPDATE Topics SET CountTopic= :CountTopic WHERE CONPESNo = :CONPESNo AND topic = :Topic""")
            update_string = update_string.bindparams(CountTopic = int(new_count), CONPESNo = row['conpesno'], Topic = row['text'])
            update_string = update_string.compile(dialect=postgresql.dialect(), compile_kwargs={"render_postcompile": True})
            db_conn.execute(update_string)
    return

def update_classification_in_topics_table(db_conn):
    """
    Populating the table Topics with the calssification corresponding to every CONPES Docuement.

    Args:
        db_conn (SQL Alchemy Connection): _description_
    """   

    query_string = sql.text("""SELECT * FROM Classification""")
    df_classification = pd.read_sql_query(query_string, db_conn)
    #print(df_keywords)

    for n,row in df_classification.iterrows():
        #Verify if topics exists
        query_string = sql.text("""SELECT * FROM Topics WHERE CONPESNo = :CONPESNo AND topic = :Topic""")
        query_string = query_string.bindparams(CONPESNo = row['conpesno'], Topic = row['text'])
        query_string = query_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
        result = pd.read_sql_query(query_string, db_conn)
        if result.empty:
            insert_string = sql.text("""INSERT INTO Topics (CONPESNo, Topic, CountTopic) VALUES (:CONPESNo, :Topic, :CountTopic)""")
            insert_string = insert_string.bindparams(CONPESNo = row['conpesno'], Topic = row['text'], CountTopic=1)
            insert_string = insert_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
            db_conn.execute(insert_string)
            print("insert")
        else:
            new_count = result["counttopic"].values[0] + 1
            update_string = sql.text("""UPDATE Topics SET CountTopic= :CountTopic WHERE CONPESNo = :CONPESNo AND topic = :Topic""")
            update_string = update_string.bindparams(CountTopic = int(new_count), CONPESNo = row['conpesno'], Topic = row['text'])
            update_string = update_string.compile(dialect=postgresql.dialect(), compile_kwargs={"render_postcompile": True})
            db_conn.execute(update_string)
            print("update")
    return

####  ----- Topic Network Table ----- ####

def creating_topic_network_table(db_conn):
    """
    Creating topic_network table.

    Args:
        db_conn (SQL Alchemy Connection)
    """    

    db_conn.execute('DROP TABLE IF EXISTS TopicNetwork;')
    print('Finished dropping table (if existed)')

    #Creating the Documents table scheme
    db_conn.execute('CREATE TABLE TopicNetwork (TopicNetworkId SERIAL, Topic1 VARCHAR NOT NULL, Topic2 VARCHAR, Year INTEGER, NumberCoOccurrences INTEGER, PRIMARY KEY(TopicNetworkId));')
    print('Created table TopicNetwork!')
    return

def topic_network_table(db_conn):
    
    #Extracting the data from the DB
    topic_data = pd.read_sql_query('Select t.topic, extract (year from d.approvaldate)::int as year, t.conpesno from Topics as t left join documents as d on d.conpesno = t.conpesno', db_conn)
    topics_per_year = topic_data.groupby('year')['topic'].apply(lambda x: sorted(list(set(x)))).reset_index()

    #Auxiliary functions
    def comb(k):         
        row=int((math.sqrt(1+8*k)+1)/2)    
        column=int(k-(row-1)*(row)/2)  
        return row, column

    def verifying_topic_presence(set_topics, topic1, topic2):
        presence = (topic1 in set_topics and topic2 in set_topics)
        return presence

    #Calculation of the co-occurrence of topics
    for year in topics_per_year['year']:
        topic_conpes = topic_data[topic_data['year'] == year].groupby('conpesno')['topic'].apply(set)
        topics_evaluate = topics_per_year[topics_per_year['year'] == year]['topic']

        length = topics_evaluate.map(len)
        size = int(length * (length-1)/2)

        for pair in range(size):
            index1, index2 = comb(pair)
            topic1 = topics_evaluate[0][index1]
            topic2 = topics_evaluate[0][index2]
            presence = sum(topic_conpes.apply(lambda x: verifying_topic_presence(x, topic1, topic2)))
            insert_string = sql.text("""INSERT INTO TopicNetwork (Topic1, Topic2, Year, NumberCoOccurrences) VALUES (:Topic1, :Topic2, :Year, :NumberCoOccurrences)""")
            insert_string = insert_string.bindparams(Topic1 = topic1, Topic2 = topic2, Year=year, NumberCoOccurrences=presence)
            insert_string = insert_string.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True})
            db_conn.execute(insert_string)
            if (pair % 10000 == 0):
                print(str(pair) + ' pairs completed out of ' + str(size) + ' total pairs in the year ' + str(year), flush=True)

    print('Network table uploaded to the database!', flush=True)

    return

####  ----- Testing queries ----- ####
def query(db_conn):

    #result = db_conn.execute("""SELECT Topic, COUNT(*), SUM(CountTopic) AS TotalCount FROM Topics GROUP BY Topic LIMIT 20""")
    #result = db_conn.execute("""SELECT * FROM Topics WHERE Topic = 'alimentación escolar'""")
    result = db_conn.execute("""SELECT * FROM Keywords WHERE CONPESNo = '4024'""")
    for row in result:
        print(row)

### ---------------------------------------------------------------- ###
## Main function

def database():
    """This method creates, inserts, and update all tables.
    """
    sys.stdout.flush()    
    start = time.time()
    print('Process started: ' + str(datetime.today()))
    db_conn = db_connection()
    # creating_main_documents_table(db_conn)
    # creating_paragraphs_table(db_conn)
    # creating_classify_table(db_conn)
    # creating_keywords_table(db_conn)
    # creating_topics_table(db_conn)
    # creating_econlit_table(db_conn)
    # creating_ProColombiaAxis_table(db_conn)
    # populating_documents_table(db_conn, csv='/home/azureuser/devenv/CONPES_Explorer/shared/approved_CONPES_documents.csv')
    # populating_tables(db_conn, csv='/home/azureuser/devenv/CONPES_Explorer/shared/approved_CONPES_documents.csv')
    # populating_topic_tables(db_conn, csv='/home/azureuser/devenv/CONPES_Explorer/shared/approved_CONPES_documents.csv')
    # populating_econlit_table(db_conn, JsonPath='/home/azureuser/devenv/CONPES_Explorer/shared/datasets/econlit_descriptors.json')
    # populating_ProColombiaAxis_table(db_conn,csvPath='/home/azureuser/devenv/CONPES_Explorer/shared/datasets/EjesYTemas.csv')
    #cleaning_unique_low_freq_topics(db_conn,5)
    creating_topic_network_table(db_conn)
    topic_network_table(db_conn)
    #update_keywords_in_topics_table(db_conn)
    #update_classification_in_topics_table
    #query(db_conn)
    db_conn.close()
    print('Process finished: ' + str(datetime.today()))
    end = time.time()
    print('Run time: ' + str(end - start) + ' seconds.')

### ---------------------------------------------------------------- ###
#Código que se va a ejecutar cuando se llame por línea de comandos
if __name__ == '__main__':    
    database()