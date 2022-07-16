#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Olga Patricia Nieto, Daniel De León, Ernesto Alejandro Martínez, Alex Fabián Gómez, Marcela Sánchez Jiménez, Daniel Hernández, and David Aurelia Ayala Usma
# Created Date: 2022-05-27
# Version = 0.0.1
# ---------------------------------------------------------------------------

## Description
"""Module to process a string document and generate a Json object with the lemmas and frequency
"""
# ---------------------------------------------------------------------------
## Required libraries
from urllib.request import urlopen
import spacy
import es_core_news_md
import json
from string import punctuation
import re


# ---------------------------------------------------------------------------
## Static attributes

__punctuation__ = punctuation + '\n' + ''
__eng_stopwords__ = [line for line in urlopen('https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt')] 

# ---------------------------------------------------------------------------
## Module functions
def process_text(input_text):
    """Loads the input string into a spaCy Doc by using the spanish medium pipeline library and returns the spaCy doc object

    Args:
        input_text (str): Any string to be processed

    Returns:
        spacy.tokens.doc: A spaCy doc object that contains the string with all the properties extracted by the spanish medium pipeline library
    """ 
    #Loading the spanish medium pipeline library  
    nlp = es_core_news_md.load()
    #Processing input text through the pipeline
    doc=nlp(input_text)
    #returning the object
    return doc

def TokensOfNonStopWords(doc):
    """Extracts the Tokens of the Non-Stop words found in the input spaCy document

    Args:
        doc (spacy.tokens.doc.Doc): The doc obtained from processing a string with a spaCy pipeline (see process_text)

    Returns:
        list: A list with the spaCy tokens that represent the Non-stop words found in the input spaCy document
    """ 
    #Creating the list by iterating over the tokens of the document and only extracting the tokens that are non-stop words according to the pipeline
    filter_numerals = re.compile('^[0-9\.\-\:\,\(\)]*$')
    filter_literals = re.compile('^[A-Za-z]\.')
    filter_letters = re.compile('^[A-Za-z]$')
    filter_percentages = re.compile('^[0-9]+.*%$')
    filter_roman_numerals= re.compile('^[xivXIV\.]+$')
    filter_urls=re.compile('^http.*')
    filter_links=re.compile('^www.*')
    filter_conpes_common=['documento','documentoconpes','conpes','consejo','nacional','política','económica','social','república','colombia','departamento','planeación','concepto','favorable','nación','externo','multilateral','usd','equivalente','monedas','destinado','financiar','proyecto','fortalecimiento','institucional','áreas','ministerio','hacienda','público','versión','aprobada','bogotá','mayo','iván','duque','márquez','presidente','marta','lucía','ramírez','blanco','vicepresidenta','daniel','palacios','martínez','ministro','interior','ministra','relaciones','exteriores','josé','manuel','restrepo','abondano','wilson','ruíz','orejuela','justicia','derecho','diego','andrés','molano','aponte','rodolfo','enrique','zea','navarro','fernando','gómez','ángel','custodio','cabrera','báez','mesa','puyo','maría','ximena','lombana','villalba','victoria','angulo','gonzález','carlos','eduardo','correa','escaf','sostenible','susana','borrero','carmen','ligia','valderrama','rojas','ciudad','comunicaciones','ángela','orozco','angélica','mayolo','obregón','transporte','guillermo','antonio','herrera','castaño','tito','crissien','alejandra','carolina','botero','barco','directora','general','laura','milena','pabón','alvarado','amparo','garcía','montaña','subdirectora','prospectiva','sistema','yesid','parra','vera','lorena','garnica','espriella','subdirector','inversiones','descentralización','seguimiento','evaluación','territorial','resumen','ejecutivo','políticas','reconocidas','fundamentales','país','sentido','recientes','buscado','fomentar','definidas','artículo','ley','espacios','delimitados','reconocidos','fortalecer','incentivar','actividades','instrumentos','decisiones','administrativas','entidad','virtud','objetivo','integración','equipamientos','propósito','consolidar','procesos','manifestaciones','desarrollados','capacidades','consolidación','problemática','relacionada','insuficiente']
    unimportant_characters = {'-', '?', '/', '=', '%'}
    TokenList=[token for token in doc if (not token.is_stop and token.text.strip() not in __punctuation__ and token.text.strip() not in filter_conpes_common and not filter_numerals.match(token.text) 
                and not filter_literals.match(token.text) and not filter_letters.match(token.text) and token.text.strip() not in __eng_stopwords__) and len(token.text)>2
                and not filter_percentages.match(token.text) and not filter_roman_numerals.match(token.text) and not filter_urls.match(token.text) 
                and not filter_links.match(token.text)]
    TokenList = [word for word in TokenList if not unimportant_characters.intersection(word)]
    #returning the list of tokens
    return TokenList

def CountWordsLower(TokenList):
    """Extracts the lowercase version of the words from the TokenList provided and returns a Json object containing the count of each word

    Args:
        TokenList (List): The list containing the Tokens extracted from a spaCy doc

    Returns:
        json: A JSON object with the lowercase words as keys and the count of the words as values
    """ 
    #Iterate over each token in the list to extract the lowercase word (str) and then add the word or count into a JSON object
    JsonNonStopWords={}
    for token in TokenList:
        if token.lower_ not in JsonNonStopWords:
            JsonNonStopWords[token.lower_] = 1
        else:
            JsonNonStopWords[token.lower_] += 1

    #returning the JSON object with the lowercase words as keys and the count of the words as values
    return JsonNonStopWords

def CountWords(TokenList):
    """Extracts the words from the TokenList provided as they are and returns a Json object containing the count of each word

    Args:
        TokenList (List): The list containing the Tokens extracted from a spaCy doc

    Returns:
        json: A JSON object with the words as keys and the count of the words as values
    """ 
    #Iterate over each token in the list to extract the word (str) and then add the word or count into a JSON object
    JsonNonStopWords={}
    for token in TokenList:
        if token.text not in JsonNonStopWords:
            JsonNonStopWords[token.text] = 1
        else:
            JsonNonStopWords[token.text] += 1

    #returning the JSON object with the words as keys and the count of the words as values
    return JsonNonStopWords

def CountLemma(TokenList):
    """Extracts the words from the TokenList provided as they are and returns a Json object containing the count of each word

    Args:
        TokenList (List): The list containing the Tokens extracted from a spaCy doc

    Returns:
        json: A JSON object with the lemmas as keys and the count of the lemmas as values
    """ 
    #Iterate over each token in the list to extract the lemma from the word (str) and then add the lemma or count into a JSON object
    JsonLemmas={}
    for token in TokenList:
        if token.lemma_ not in JsonLemmas:
            JsonLemmas[token.lemma_] = 1
        else:
            JsonLemmas[token.lemma_] += 1

    #returning the JSON object with the words as keys and the count of the words as values
    return JsonLemmas

def NormalizeFrequencyJSON(JsonWordCount):
    """Normalize a JSON values from count to a percentage frecuency considering the most frequent word in the text (Useful to compare texts of different longitude to know how important is 
        a word.
    
    Args:
        JsonWordCount (JSON): The json object with key words and values as the count of each word in the text

    Returns:
        json: A JSON object with the words as keys and the values as the count of the each word divided by the count of the most frequent word in the initial JSON object
    """ 
    #Iterate over each token in the list to extract the lemma from the word (str) and then add the lemma or count into a JSON object
    mostfrequentwordcount = max(JsonWordCount.values())
    JsonWordNormalFrequency = {}
    for key in JsonWordCount.keys():
        ##to do https://www.numpyninja.com/post/text-summarization-through-use-of-spacy-library
        JsonWordNormalFrequency[key]=JsonWordCount[key]/mostfrequentwordcount
    #returning the list of tokens
    return JsonWordNormalFrequency

def PercentageFrequencyJSON(JsonWordCount):
    """Normalize a JSON values from count to a percentage frecuency considering the number of words in the texts. Very similar to the normalized but when comparing text of different length
    
    Args:
        JsonWordCount (JSON): The json object with key words and values as the count of each word in the text

    Returns:
        json: A JSON object with the words as keys and the values as the count of the each word divided by the sum of the word frequency in the initial JSON object
    """ 
    #Iterate over each token in the list to extract the lemma from the word (str) and then add the lemma or count into a JSON object
    totalwordcount = sum(JsonWordCount.values())
    JsonWordPercentageFrequency = {}
    for key in JsonWordCount.keys():
        ##to do https://www.numpyninja.com/post/text-summarization-through-use-of-spacy-library
        JsonWordPercentageFrequency[key]=JsonWordCount[key]/totalwordcount
    #returning the list of tokens
    return JsonWordPercentageFrequency


### ---------------------------------------------------------------- ###
## Main function
def topic_modeling():
    print("Script mode initialized.")
    test1=process_text("Texto de prueba no autorizado pero que aparece bueno para no intentar probar unas funciones www.ods.gov.co https://www.finagro.com.co/agroguia que funcionan de maneras extrañas 20.5% III ? a ,r viii fin de la prueba")
    print(type(test1))
    test2=TokensOfNonStopWords(test1)
    print(test2)
    test3=CountWordsLower(test2)
    print(test3)
    test4=CountWords(test2)
    print(test4)
    test5=CountLemma(test2)
    print(test5)
    test6=NormalizeFrequencyJSON(test3)
    print(test6)
    test7=PercentageFrequencyJSON(test3)
    print(test7)

### ---------------------------------------------------------------- ###
#Código que se va a ejecutar cuando se llame por línea de comandos
if __name__ == '__main__':
    topic_modeling()



