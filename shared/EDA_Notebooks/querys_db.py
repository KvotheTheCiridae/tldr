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

def query_documents(db_conn):
    result = db_conn.execute("""SELECT * FROM Documents WHERE CONPESNo = '4080'""")
    for row in result:
        print(row)

def query_paragrahs(db_conn):
    result = db_conn.execute("""SELECT * FROM paragraphs WHERE CONPESNo = '4080'AND Page = 25 """)
    for row in result:
        print(row)

def query_classification(db_conn):
    result = db_conn.execute("""SELECT * FROM Classification WHERE CONPESNo = '4080'""")
    for row in result:
        print(row)

def query_keywords(db_conn):
    result = db_conn.execute("""SELECT * FROM Keywords WHERE CONPESNo = '4080'""")
    for row in result:
        print(row)

def query_topics(db_conn):
    result = db_conn.execute("""SELECT * FROM Documents WHERE CONPESNo = '4061'""")
    #result = db_conn.execute("""SELECT * FROM Paragraphs WHERE CONPESNo = '4045'""")
    for row in result:
        print(row)

def query_generic(db_conn, query):
    df = pd.read_sql_query(query, db_conn)
    return df

### ---------------------------------------------------------------- ###
## Main function

def query_database():
    """This method execute querys all tables.
    """
    sys.stdout.flush()    
    start = time.time()
    print('Process started: ' + str(datetime.today()))
    db_conn = db_connection()
    # print("Document")
    # query_documents(db_conn)
    # print("Paragrahs")
    # query_paragrahs(db_conn)
    # print("Classification")
    # query_classification(db_conn)
    # print("Keywords")
    # query_keywords(db_conn)
    # print("Topics")
    query_topics(db_conn)
    db_conn.close()
    print('Process finished: ' + str(datetime.today()))
    end = time.time()
    print('Run time: ' + str(end - start) + ' seconds.')

### ---------------------------------------------------------------- ###
#Código que se va a ejecutar cuando se llame por línea de comandos
if __name__ == '__main__':    
    query_database()