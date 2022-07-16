#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Olga Patricia Nieto, Daniel De León, Ernesto Alejandro Martínez, Alex Fabián Gómez, Marcela Sánchez Jiménez, Daniel Hernández, and David Aurelia Ayala Usma
# Created Date: 2022-05-27
# Version = 0.0.1
# ---------------------------------------------------------------------------

## Description
"""Module to download data and metadata from the approved CONPES documents list.
The output of the module is the complete list of approved CONPES documents, the PDF file links, 
the links to the appendices of each document if any, and the ID of the document.

Additionally this module downloads the PDF files of the specified range of CONPES
documents to the selected directory.
"""
# ---------------------------------------------------------------------------
## Required libraries
import requests as r
import pandas as pd
import numpy as np
import json
import os

# ---------------------------------------------------------------------------
## Static attributes
__cookies_url__ = 'https://sisconpes.dnp.gov.co/SisCONPESWeb/#documentos_conpes'
__download_url__ = 'https://sisconpes.dnp.gov.co/SisCONPESWeb/AccesoPublico/BuscarCONPES'

# ---------------------------------------------------------------------------
## Module functions
def get_auth_cookie(url):
    """Getting the authentication cookies for the DNP website.

    Args:
        url (str): The DNP website URL.

    Returns:
        dict: A dictionary with the cookie key-value pair.
    """    
    cookie = None

    cookie_retrieval = r.get(url)
    cookie = cookie_retrieval.cookies.get_dict()

    return cookie


def download_url_creation(cookie):
    """Obtaining the URL for CONPES documents' list.

    Args:
        cookie (dict): A dictionary with the cookie key-value pair.

    Returns:
        str: URL of the list of CONPES documents.
    """    
    url = None

    verification_cookie = [(k,v) for k,v in cookie.items()]
    columns_included = '&titulo=&numero=&fechaAprobacion1=&fechaAprobacion2='
    url = __download_url__ + '?' + verification_cookie[0][0] + '=' + verification_cookie[0][1] + columns_included

    return url


def retrieving_conpes_list(url_request):
    """_summary_

    Args:
        url_request (str): URL of the list of CONPES documents.

    Returns:
        Pandas DataFrame: Table containing the entire list of CONPES documents and the PDF document location for each.
    """    
    conpes_list = None

    raw_request = r.post(url_request)
    dict_request = json.loads(raw_request.text)
    conpes_list = pd.DataFrame(dict_request['rows'])
    conpes_list.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    conpes_list['FechaAprobacion'] = pd.to_datetime(conpes_list['FechaAprobacion'], format='%d/%m/%Y')
    conpes_list = conpes_list[['IdDocumentoCONPES','Titulo', 'Numero', 'FechaAprobacion', 'URL', 'URLPAS', 'URLOtros']] #Extracting only meaningful columns.

    return conpes_list

def filtering_conpes_list_by_date(conpes_list, filter_date='2017-01-01'):
    """Filtering the CONPES document list by date.

    Args:
        conpes_list (Pandas DataFrame): Table containing the entire list of CONPES documents and the PDF document location for each.
        filter_date (str, optional): Date to filter. Defaults to '2017-01-01'.

    Returns:
        DataFrame: The filtered CONPES document list.
    """    
    filtering_conpes_list = conpes_list[conpes_list['FechaAprobacion'] >= filter_date]
    return filtering_conpes_list


def exporting_conpes_list(conpes_list, outdir='../../shared/PDF/'):
    """Exporting the list of CONPES documents to be downloaded.

    Args:
        conpes_list (Pandas DataFrame): Table containing the entire list of CONPES documents and the PDF document location for each.
        outdir (str, optional): The location where documents will be downloaded. Defaults to '../../shared'.
    """    
    conpes_list.to_csv(outdir + 'approved_CONPES_documents.csv', header=True, index=False)
    print("CONPES list successfully exported!!")


def conpes_document_download(row, outdir='../../shared/PDF/'):
    """Performs the download request of the PDF file containing a single CONPES document.

    Args:
        row (Pandas Series): A row representing a single document from the CONPES document list.
        outdir (str, optional): The location where documents will be downloaded. Defaults to '../../shared'.
    """    
    file_name = outdir + 'PDF/CONPES_' + str(row['Numero']) + '.pdf'
    url = row['URL']
    doc_req = r.get(url, verify=False)
    
    with open(file_name, 'wb') as f:
        f.write(doc_req.content)
    
    print('Saved file: ' + file_name)


def conpes_list_mass_download(conpes_list):
    """Performing the mass download of a list of CONPES documents.

    Args:
        conpes_list (Pandas DataFrame): The filtered CONPES document list.
    """    

    print('Starting download process!')
    conpes_list.apply(conpes_document_download, axis=1)
    print('Finished process!')


### ---------------------------------------------------------------- ###
## Main function
def conpes_download():
    print("Script mode initialized.")
    print("System location: " + os.getcwd())
    cookie = get_auth_cookie(__cookies_url__)
    print("Authorization Cookie retrieved!")
    download_url = download_url_creation(cookie)
    print("The Download URL is: " + download_url)
    preliminary_list = retrieving_conpes_list(download_url)
    print("CONPES list retrieved!")
    filtered_list = filtering_conpes_list_by_date(preliminary_list)
    print("CONPES list filtered!")
    exporting_conpes_list(filtered_list)
    print("Filtered CONPES list exported!")
    conpes_list_mass_download(filtered_list)
    print("Success!")

### ---------------------------------------------------------------- ###
#Código que se va a ejecutar cuando se llame por línea de comandos
if __name__ == '__main__':
    conpes_download()