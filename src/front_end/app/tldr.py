#!/user/bin/emv python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------------------------------------
#Created By: Alex Fabián Gómez, Daniel de León, Marcela Sánchez Jimenez,Olga Patricia Nieto,Daniel Hernandez,
#            and David Aurelia Ayala Usma
# Created Date: 2022-06-28
# Version = 0.0.1 
#--------------------------------------------------------------------------------------------------------------------------------- 
##Description
""" Brief application - Document automation
    Customized streamlit app for PROCOLOMBIA's Natural Language Processing
"""
#---------------------------------------------------------------------------------------------------------------------------------
## Required libraries
from streamlit_option_menu import option_menu
import streamlit as st
from PIL import Image
import sys
import os

#---------------------------------------------------------------------------------------------------------------------------------
## Application modules
sys.path.append(os.path.realpath('../../modules/data_interface'))
import data_interface as di
from page import document_search 

#---------------------------------------------------------------------------------------------------------------------------------
## Setting app
st.set_page_config(page_title="Too long, didn't read", page_icon='🔎', layout='wide', initial_sidebar_state="expanded",menu_items=None)
padding_top = 0
st.markdown(f"""<style>.appview-container .main .block-container{{padding-top: {padding_top}rem;}}</style>""",unsafe_allow_html=True)
st.markdown("""<style>[data-baseweb="select"] {margin-top: -44px;}</style>""",unsafe_allow_html=True)
st.markdown("""<style>[title="streamlit_tags.streamlit_tags"] {margin-top: -30px; margin-bottom: -20px; }</style>""",unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------
## Session State Configuration

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "doc_search"

if "docs_df" not in st.session_state or "topics_procolombia" not in st.session_state:
    with st.spinner('Loading... Please wait!'):
        st.session_state.docs_df, st.session_state.topics_procolombia = di.loading()
    st.success('Done!')

#---------------------------------------------------------------------------------------------------------------------------------
##Module functions


#---------------------------------------------------------------------------------------------------------------------------------
##Home page
def home():
    st.header("Too long, didn't read")
    st.subheader("Por: Team 19 - Cohort 6 - DS4A 6.0")
    
    st.write("")
    st.markdown("""<p style='text-align: justify; color: auto;font-size:100%'>
        Esta APP le permite consultar los documentos CONPES de los últimos 5 años. Puede ingresar entre 1 y 5 términos para 
        realizar una búsqueda personalizada o a través de términos sugeridos. Es posible reducir la búsqueda a un periodo de tiempo, usando 
        la barra donde se visualizan los años. Los documentos están clasificados de "Norma" o de "Política", puede seleccionar uno de éstos para visualizar el contenido 
        en la sección inferior. Se muestran todos los párrafos del documento, el resumen ejecutivo.</p>""", unsafe_allow_html=True)
    
    st.write("")
    st.write("")

    st.markdown("""<p style='text-align: justify; color: auto;font-size:100%'>
        This APP allows you to consult the CONPES documents of the last 5 years. You can enter between 1 and 5 terms to perform 
        a personalized search or through suggested terms. It is possible to reduce the search to a period, using the bar where the years are displayed. 
        The documents are classified as "Standard" or "Policy", you can select one of these to view the content in the lower section. 
        There are all paragraphs of the document, and the executive summary are shown.</p>""", unsafe_allow_html=True)

    st.write("")
    st.write("")    
    st.write("")
    st.write("")    
    st.write("")
    st.write("")    
    st.write("")
    st.write("")
    st.markdown("<h6 style='text-align: left; color: auto;font-size:100%'>Team 19:</h6>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: auto;font-size:90%'>Aurelia Ayala, Daniel De León, Daniel Hernandez, Ernesto Martinez, Fabian Gomez, Marcela Sanchez, Olga Nieto</p>", unsafe_allow_html=True)


#Sidebar logo
logo_procolombia = Image.open(r"../assets/logo_procolombia.png")
logo_ds4a = Image.open(r'../assets/logo_ds4a.png')
logo_team19 = Image.open(r'../assets/logo_team19_2.png')
st.sidebar.image(logo_procolombia, use_column_width=True)
logo1, logo2 = st.sidebar.columns((0.71,0.29))
with logo1:
    st.image(logo_ds4a)
with logo2:
    st.image(logo_team19)


#Sidebar menu
with st.sidebar:
    page_menu = option_menu(None,["Home","Búsqueda de documentos"],
                                icons=['house', 'search'],
                                styles={
                                    "container": {"padding": "0!important", "background-color": "#ffcb00"},
                                    "icon": {"color": "red", "font-size": "22px"}, 
                                    "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#ffcb00"},
                                    "nav-link-selected": {"background-color": "#008fd6"},
                                }
                            )

if page_menu == 'Búsqueda de documentos':
    document_search.run()
else:
    home()
