#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Olga Patricia Nieto, Daniel De León, Ernesto Alejandro Martínez, Alex Fabián Gómez, Marcela Sánchez Jiménez, Daniel Hernández, and David Aurelia Ayala Usma
# Created Date: 2022-05-27
# Version = 0.0.1
# ---------------------------------------------------------------------------

## Description
"""
This module takes a PDF filepath, reads the PDF content, extracts the paragraphs,
executive summary, keywords, and classification of the CONPES document.
"""
# ---------------------------------------------------------------------------
## Required libraries

from nltk.tokenize import regexp_tokenize
import pandas as pd
import numpy as np
import pdfplumber
import json
import os
import re

# ---------------------------------------------------------------------------
## Static attributes


# ---------------------------------------------------------------------------
## Module functions

def process_single_pdf(filename):
    """Receives a PDF file and opens it for reading.

    Args:
        filename (str): Path to the PDF file.

    Returns:
        pdfplumber.PDF: An iterable object containing the text in the PDF file.
    """    
    document = None
    document = pdfplumber.open(filename)
    return document

def convert_all_document(document):
    """Receives a PDF file and opens it for reading.

    Args:
        document (pdfplumber.PDF): An iterable object containing the text in the PDF file.

    Returns:
        str: The CONPES document like string.
    """    
    content = ''
    for i in range(len(document.pages)):
        page = document.pages[i] 
        page_content = '\n'.join(page.extract_text().split('\n')[:-1])
        content = content + page_content
 
    return content

def executive_summary(document):
    """Receives a PDF file and opens it for reading.

    Args:
        document (pdfplumber.PDF): An iterable object containing the text in the PDF file.

    Returns:
        str: The executive summary of the CONPES document.
    """

    summary = ""

    keywords = "Palabras clave:"
    page = document.pages[2]
    
    for last_page in range(2, len(document.pages)):
        summary= summary + document.pages[last_page].extract_text(use_text_flow=True)
        find_last_page = re.findall(keywords,summary)

        if (len(find_last_page) == 0):
            continue
        elif (len(find_last_page) != 0):
            break
    
    return summary

def divide_paragraphs(id_document,document):
    """ Receives a PDF file and opens it for reading.

    Args:
        id_document (str): Name the PDF file.
        document (pdfplumber.PDF): An iterable object containing the text in the PDF file.
        

    Returns:
        df_document (Pandas DataFrame): Two-dimensional, size-mutable, potentially heterogeneous tabular data.
    """    

    df_document = pd.DataFrame(columns = ['IdCONPES', 'Page', 'Paragraph', 'Text' ])

    for page in document.pages:
        text = page.extract_text(use_text_flow=True).rstrip().lstrip() #Removing unnecesary whitespaces
        paragraphs = regexp_tokenize(text, r'\.\s\n|\s*\n\s*\n\s*', gaps=True) #Dividing into paragraphs
        #paragraphs = paragraphs[:-1] #Removing the page number from the page
        paragraphs = [s.replace('\n', '') for s in paragraphs] #Removing spurious line breaks in paragraphs

        for paragraph_number, paragraph in enumerate(paragraphs, start=1):
            if(len(paragraph) > 4):
                new_row = pd.DataFrame.from_dict([{'IdCONPES': id_document, 'Page': page.page_number, 'Paragraph': paragraph_number, 'Text': paragraph }])
                df_document = pd.concat([df_document, new_row], ignore_index=True)

    return df_document

def classification_document(df_document):
    """ Receives a PDF file and opens it for reading.

    Args:
        df_document (Pandas DataFrame): Two-dimensional, size-mutable, potentially heterogeneous tabular data.
        
    Returns:
        df_classify (Pandas DataFrame): Two-dimensional, size-mutable, potentially heterogeneous tabular data.
    """    

    df_classify = pd.DataFrame()

    array_text = df_document[df_document["Text"].str.contains('Clasificación: ')]
    id_document = array_text["IdCONPES"].iloc[0]

    value_text=array_text["Text"].iloc[0]
    index_1 = value_text.index(':')

    if value_text.count(':') > 1:
        data = value_text.split(sep=':')
        value_text = re.sub('Palabras clave','', data[1])
        index_1 = 0
        
    index_2 = index_1 + 1
    type_char = value_text[:index_1]
    text_char = value_text[index_2:]
    data = { 'IdCONPES': id_document,'Type': type_char,'Text': text_char} 
    df_classify = create_class(data)

    return df_classify

def keywords_document(df_document):
    """ Receives a PDF file and opens it for reading.

    Args:
        df_document (Pandas DataFrame): Two-dimensional, size-mutable, potentially heterogeneous tabular data.
        
    Returns:
        df_keywords (Pandas DataFrame): Two-dimensional, size-mutable, potentially heterogeneous tabular data.
    """    

    df_keywords = pd.DataFrame()
    array_text = df_document[df_document["Text"].str.contains('Palabras clave: ')]

    id_document = array_text["IdCONPES"].iloc[0]
    value_text=array_text["Text"].iloc[0]
    index_1 = value_text.index(':')

    if value_text.count(':') > 1:
        data = value_text.split(sep=':')
        value_text = re.sub('Palabras clave','', data[2])
        index_1 = 0

    index_2 = index_1 + 1
    type_char = value_text[:index_1]
    text_char = value_text[index_2:].lower()
    data = { 'IdCONPES': id_document,'Type': type_char,'Text': text_char} 
    df_keywords = create_class(data) 

    return df_keywords


def create_class(data):
    """ Receives an information clasification/keywords.

    Args:
        data (Dictionary): Two-dimensional, size-mutable, potentially heterogeneous tabular data.
        
    Returns:
        df_class (Pandas DataFrame): Two-dimensional, size-mutable, potentially heterogeneous tabular data.
    """    

    df_class = pd.DataFrame()
    words = data["Text"].strip().split(sep=',')

    for word in words:
        if(word == ''):
            pass
        else:
            word = re.sub(r'[^\w\s]', '', word)
            word = word.strip()
            new_row = pd.DataFrame.from_dict([{ 'Value': word, 'IdCONPES': data["IdCONPES"]}])
            df_class = pd.concat([df_class,new_row], ignore_index=True)

    return df_class

def classify_document(content):
    """Receives a PDF file and opens it for reading.

    Args:
        content(str): containing the text of document CONPES file.

    Returns:
        type_doc (str): Classification CONPES document like string.
    """    
    type_doc = "De Norma"
    find_words = "DEFINICIÓN DE LA POLÍTICA..."
    find_text = re.findall(find_words,content)
    if len(find_text) > 0:
        type_doc = "Política" 
    
    return type_doc

### ---------------------------------------------------------------- ###
## Main function
def pdf_reader(file = "/home/azureuser/devenv/CONPES_Explorer/shared/PDF/CONPES_4076.pdf"):
    """This method runs the entire pdf processing before NLP takes place.

    Args:
        file (str): The filepath of a CONPES PDF file.

    Returns:
        df_paragraph (Pandas DataFrame): A DataFrame containing the paragraphs of the document.
        df_classify (Pandas DataFrame): A DataFrame containing the classification of the document.
        df_keywords (Pandas DataFrame): A DataFrame containing the keywords of the document.
        type_doc (str): The type of the CONPES document.
        summary (str): The executive summary of the CONPES document.
    """    

    DocId=re.sub('^.*/', '', file)
    DocId=re.sub('\.pdf$','', DocId)
    document = process_single_pdf(file)
    content = convert_all_document(document)
    df_paragraph = divide_paragraphs(DocId,document)
    keywords = "Palabras clave:"
    find_text = re.findall(keywords,content)
    df_classify = pd.DataFrame()
    if find_text == []:
        summary = ""
        df_classify = pd.DataFrame()
        df_keywords = pd.DataFrame()
    else:
        summary = executive_summary(document)
        df_classify = classification_document(df_paragraph)
        df_keywords = keywords_document(df_paragraph)
    type_doc = classify_document(content)

    return df_paragraph, df_classify, df_keywords, type_doc, summary

### ---------------------------------------------------------------- ###
#Código que se va a ejecutar cuando se llame por línea de comandos
if __name__ == '__main__':
    pdf_reader()    
