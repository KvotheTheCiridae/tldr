#!/user/bin/emv python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------------------------------------
#Created By: Alex Fabián Gómez, Daniel de León, Marcela Sánchez Jimenez,Olga Patricia Nieto,Daniel Hernandez,
#            and David Aurelia Ayala Usma
# Created Date: 2022-06-28
# Version = 0.0.1 
#--------------------------------------------------------------------------------------------------------------------------------- 

##Description
"""PROCOLOMBIA's Natural Language Processing Streamlit app
    Page: CONPES DOCUMENT SEARCH
    Developed by: Correlation One - DS4A - COHORT 6 TEAM 19
"""
#---------------------------------------------------------------------------------------------------------------------------------
## Required libraries
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import sys
import os
import altair as alt
from streamlit_option_menu import option_menu
from streamlit_tags import st_tags_sidebar
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx
from wordcloud import WordCloud, STOPWORDS
from st_aggrid import GridOptionsBuilder, AgGrid


#---------------------------------------------------------------------------------------------------------------------------------
## Application modules
import frontend_behavior.frontend_behavior as fb
sys.path.append(os.path.realpath('../../modules/data_interface'))
import data_interface as di

#---------------------------------------------------------------------------------------------------------------------------------
## Session state definitions
if "docs_df" not in st.session_state or "topics_procolombia" not in st.session_state:
    #with st.spinner('Loading... Please wait!'):
        st.session_state.docs_df, st.session_state.topics_procolombia  = di.loading()
    #st.success('Done!')

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "doc_search"

if "search_bar" not in st.session_state:
    st.session_state.search_bar = None

range_years = di.get_years_list(st.session_state.docs_df)

if "start_year" not in st.session_state:
    st.session_state.start_year = min(range_years)
    st.session_state.end_year = max(range_years)

if 'document_selected' not in st.session_state:
    st.session_state.document_selected = ""


#---------------------------------------------------------------------------------------------------------------------------------
##Module functions
def run():   
    #-------------------------------------------------------------------------------------
    #Sidebar
    #Function custom search
    def custom_search():
            
        #Search bar with suggested topics   
        personalized_search = st_tags_sidebar( #This is a list of terms
            label='Términos de búsqueda:',
            text='Presione enter',
            value=[],
            suggestions = fb.filtered_topics_list(st.session_state.docs_df['topic']),
            maxtags = 5,
            key='text')
        st.sidebar.markdown("<p style='text-align: left; color: auto; font-size:80%'>Digite máximo 5 términos</p>", unsafe_allow_html=True)
        personalized_search = [x.lower() for x in personalized_search]
        return personalized_search
            
    #Function suggested search
    def suggested_search():
        suggested_list = fb.filtered_topics_list(st.session_state.topics_procolombia)
        suggested_top = st.sidebar.selectbox('Términos sugeridos de búsqueda:',(suggested_list))
        return [suggested_top]
            
    #Search type selector
    search_type = st.sidebar.radio("Seleccione el tipo de búsqueda",('Búsqueda personalizada', 'Temas sugeridos'))
    if search_type == 'Búsqueda personalizada':
        st.session_state.search_bar = custom_search()
    else:
        st.session_state.search_bar = suggested_search()
            
    #Range Slider
    with st.sidebar.expander("Filtro por año"):
        st.session_state.start_year, st.session_state.end_year = st.select_slider('Seleccione el rango de fechas', options=range_years,  value=(min(range_years), max(range_years)))
     
    
    #Functions for dynamic view
    def search_view():
        st.session_state.view_mode = "doc_search"

    def docum_view():
        st.session_state.view_mode = "doc_view"



    #-------------------------------------------------------------------------------------
    #App layout deffinition
    associated_documents = st.container()
    st.write('---')
    dynamic_container = st.container()

    # associated document container   
    with associated_documents:
        st.subheader('Resultados de la búsqueda')
        st.write('')
        #st.write('')
        #st.write('')

        # 4 columns layout (CONPES politica list, details button, CONPES norma list, details button)   
        col_list_politica, col_download_politica,col_list_norma, col_download_norma = st.columns((3,1,3,1))
        
        # Column with CONPES politica list
        with col_list_politica:
            st.markdown('##### CONPES de Política')
            list_conpes_politica = fb.conpes_list_by_type(st.session_state.docs_df, st.session_state.start_year, st.session_state.end_year, 'Política', st.session_state.search_bar)
            conpes_politica_selected = st.selectbox("",(list_conpes_politica),key="conpes_politica_selection")
        
        # Column with details button    
        with col_download_politica:
            st.write('') #Blank spaces to align Button with selectbox
            st.write('') #Blank spaces to align Button with selectbox
            #st.write('') #Blank spaces to align Button with selectbox
            #st.write('') #Blank spaces to align Button with selectbox
            #st.write('') #Blank spaces to align Button with selectbox
            button2 = st.button('Ver detalles',key=10)
            if button2:
                st.session_state.document_selected = st.session_state.conpes_politica_selection
                docum_view()

        # Column with CONPES norma list   
        with col_list_norma: 
            list_conpes_norma = fb.conpes_list_by_type(st.session_state.docs_df, st.session_state.start_year, st.session_state.end_year, 'De Norma', st.session_state.search_bar)
            st.markdown('##### CONPES de Norma')
            conpes_norma_selected = st.selectbox("",(list_conpes_norma),key="conpes_norma_selection")

        # Column with details button            
        with col_download_norma:
            st.write('') #Blank spaces to align Button with selectbox
            st.write('') #Blank spaces to align Button with selectbox
            #st.write('') #Blank spaces to align Button with selectbox
            #st.write('') #Blank spaces to align Button with selectbox
            #st.write('') #Blank spaces to align Button with selectbox
            button1 = st.button('Ver detalles',key=11)
            if button1:
                st.session_state.document_selected = st.session_state.conpes_norma_selection
                docum_view()

        # 2 columns layout (title politica, title norma)
        brief_politica, brief_norma = st.columns(2)
        
        # column with title politica
        with brief_politica:
            #st.write('')
            st.markdown('###### **Título**')
            if(conpes_politica_selected != None):
                text_politica = st.session_state.docs_df[st.session_state.docs_df['conpesno'] == conpes_politica_selected.replace('CONPES No. ', '')]['title'].unique()[0]
                year_politica = st.session_state.docs_df[st.session_state.docs_df['conpesno'] == conpes_politica_selected.replace('CONPES No. ', '')]['year'].unique()[0]
                st.markdown('*  ' + '*' + str(text_politica) + '*' + "    (Año de emisión: " +  str(year_politica) + ")")
                keywords_politica = di.get_conpes_keywords()
                keywords_politica = keywords_politica[keywords_politica['conpesno'] == conpes_politica_selected.replace('CONPES No. ', '')]['text'].values.tolist()
                keywords_list_politica = ""
                for x in keywords_politica:
                    keywords_list_politica += x + ", "
                st.markdown('###### **Palabras clave**')
                st.write(keywords_list_politica)
        
        # column with title norma
        with brief_norma:
            #st.write('')
            st.markdown('###### **Título**')
            if(conpes_norma_selected != None):
                text_norma = st.session_state.docs_df[st.session_state.docs_df['conpesno'] == conpes_norma_selected.replace('CONPES No. ', '')]['title'].unique()[0]
                year_norma = st.session_state.docs_df[st.session_state.docs_df['conpesno'] == conpes_norma_selected.replace('CONPES No. ', '')]['year'].unique()[0]
                st.markdown('*  ' + '*' + str(text_norma) + '*' + "    (Año de emisión: " +  str(year_norma) + ")")
                keywords_norma = di.get_conpes_keywords()
                keywords_norma = keywords_norma[keywords_norma['conpesno'] == conpes_norma_selected.replace('CONPES No. ', '')]['text'].values.tolist()
                keywords_list_norma = ""
                for x in keywords_norma:
                    keywords_list_norma += x + ", "
                st.markdown('###### **Palabras clave**')
                st.write(keywords_list_norma)

    # Dynamic view container for charts related to document search
    with dynamic_container:
        if st.session_state.view_mode == "doc_search":
            
            # 2 columns layout (Linechart, cytoscape)
            col_linechart, col_cytoscape = st.columns(2)

            #Column with linechart
            with col_linechart:
                if(len(st.session_state.search_bar) > 0):
                    years = di.get_search_topics_over_time(st.session_state.docs_df, st.session_state.search_bar)
                else:
                    years = di.get_top_n_topics_over_time(st.session_state.docs_df)

                min_years=years['year'].min()
                max_years=years['year'].max() 
                years = years[years["year"].between(st.session_state.start_year, st.session_state.end_year)]
                st.subheader('Frecuencia de temas en el tiempo')
                chart = alt.Chart(data=years,mark='line',title = '').encode(
                            x=alt.X('year:Q',axis=alt.Axis(tickMinStep=1), title='Año'),
                            y= alt.Y('counttopic:Q', title='Frecuencia del tema en el año'),
                            color=alt.Color('topic:N', legend=alt.Legend(title=None))
                            ).properties(height=500)
                st.altair_chart(chart,use_container_width=True)
                st.markdown("<p style='text-align: left; color: auto;font-size:85%'>Este gráfico muestra la suma de la aparición de cada termino por cada año de aprobación</p>", unsafe_allow_html=True)

                #Column with cytoscape
                with col_cytoscape: 
                    # Read dataset (CSV)
                    df_interact = pd.read_csv('/home/azureuser/devenv/tldr/src/front_end/data/network_table.csv')
                    df_interact['weight'] = fb.topic_co_ocurrence_aggregation(df_interact, st.session_state.start_year, st.session_state.end_year) #Assigning weights according to co-occurrence

                    # Set header title
                    st.subheader('Temas asociados a los términos de búsqueda')

                    # Set info message on initial site load
                    if len(st.session_state.search_bar) == 0:
                        st.markdown('*Por favor seleccione o busque al menos un tema*')

                    # Create network graph when user selects >= 1 item
                    else:
                        df_select = df_interact.loc[df_interact['topic1'].isin(st.session_state.search_bar) | \
                                                        df_interact['topic2'].isin(st.session_state.search_bar)]
                        df_select = df_select.reset_index(drop=True)
                        df_select = df_select.sort_values(by='weight', ascending=False).head(100) #INCLUDE IN MODULE FRONTEND-BEHAVIOR

                        # Create networkx graph object from pandas dataframe
                        G = nx.from_pandas_edgelist(df_select, 'topic1', 'topic2', 'weight')

                        # Initiate PyVis network object
                        topic_net = Network(width='700px', bgcolor='#222222', font_color='white')

                        # Take Networkx graph and translate it to a PyVis graph format
                        topic_net.from_nx(G)

                        # Generate network with specific layout settings
                        topic_net.repulsion(node_distance=200, central_gravity=0.5,
                                            spring_length=150, spring_strength=0.10,
                                            damping=0.99)

                        # Save and read graph as HTML file (on Streamlit Sharing)
                        try:
                            path = '/tmp'
                            topic_net.save_graph(f'{path}/pyvis_graph.html')
                            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

                        # Save and read graph as HTML file (locally)
                        except:
                            path = '/html_files'
                            topic_net.save_graph(f'{path}/pyvis_graph.html')
                            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

                        # Load HTML file in HTML component for display on Streamlit page
                        components.html(HtmlFile.read(), height=500)
                        st.markdown("<p style='text-align: left; color: auto;font-size:85%'>En esta red, cada nodo representa un término de búsqueda y cada línea entre dos nodos representa que estos aparecen juntos en al menos un documento. Entre mayor el grosor de la línea, significa que los dos términos aparecen juntos en más documentos.</p>", unsafe_allow_html=True)
    st.write('---')

    #Dynamic view container for document contents
    with dynamic_container:
        if st.session_state.view_mode == "doc_view":
            dynamic_container.empty()
            button3 = st.sidebar.button("Atrás",on_click=search_view())    
            st.subheader('Contenidos del documento '+ str(st.session_state.document_selected))
            st.session_state.document_selected = st.session_state.document_selected.replace('CONPES No. ', '')
            url = st.session_state.docs_df[st.session_state.docs_df['conpesno'] == st.session_state.document_selected.replace('CONPES No. ', '')]['url'].unique()[0]
            st.markdown("[Descargar PDF](%s)" %url, unsafe_allow_html=True) 

            #Creating containers for page layout 
            buttons = st.container()
            summary_cont = st.container()
            doc_table = st.container()
            view_complement = st.container()

            #presentation of the executive summary: 
            with summary_cont:
                st.write('')
                summary = di.get_conpes_summary(st.session_state.document_selected).values.tolist()[0][0]
                if summary=="":
                    summary ="Sin resumen"
                
                st.markdown("<h6 style='text-align: left; color: auto;'>Resumen del documento</h5>", unsafe_allow_html=True)
                with st.expander('Resumen ejecutivo'):
                    st.markdown(summary.strip())
                
            #interactive table:
            with doc_table: #Creating an interactive table

                    st.write('')
                    st.write('')
                    st.markdown("<h6 style='text-align: left; color: auto;'>Navegador de párrafos</h5>", unsafe_allow_html=True)
                    conpes_table= di.get_conpes_paragraphs(st.session_state.document_selected)
                    conpes_table.columns = ['Página', 'Párrafo', 'Texto']
                    gb = GridOptionsBuilder.from_dataframe(conpes_table)
                    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
                    gb.configure_side_bar() #Add a sidebar
                    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
                    gridOptions = gb.build()

                    grid_response = AgGrid(
                        conpes_table,
                        gridOptions=gridOptions,
                        data_return_mode='AS_INPUT', 
                        update_mode='NO_UPDATE', 
                        fit_columns_on_grid_load=False,
                        theme='fresh', #Add theme color to the table
                        enable_enterprise_modules=True,
                        height=400, 
                        width='100%',
                        reload_data=False
                    )

            #Code related to the charts:
            with view_complement:
                    st.write('---')
                    select_box =st.container()
                    plots=st.container()
                    with plots:
                        # 2 columns layout (WordCloud, bar chart)
                        col1, col2 = st.columns(2)
                        #Wordcloud
                        with col1:
                            st.subheader('Nube de palabras')
                            conpes_df = di.get_conpes_topics(st.session_state.document_selected).sort_values(by='counttopic',ascending=False)
                            if conpes_df['counttopic'].any() == 'trabajo':
                                conpes_df = conpes_df[conpes_df['counttopic'].apply(lambda x: isinstance(x, float))] #para corregir error ValueError: could not convert string to float: 'trabajo'
                                conpes_dict=dict([(i) for i in zip(conpes_df['counttopic'],conpes_df['topic'])])
                            else:

                                conpes_df = conpes_df[conpes_df['topic'].apply(lambda x: isinstance(x, str))] #para corregir error ValueError: could not convert string to float: 'trabajo'
                                conpes_dict=dict([(i) for i in zip(conpes_df['topic'],conpes_df['counttopic'])])

                            # create the WordCloud object
                            wc = WordCloud(min_word_length =3,
                                     background_color='white',
                                     scale=10)

                            #generate the word cloud
                            wc = wc.fit_words(conpes_dict)
                            st.image(wc.to_array(), use_column_width='always')
                            st.markdown("<p style='text-align: left; color: auto;font-size:85%'>Este gráfico muestra los temas relevantes del documento. Las palabras más frecuentes tienen una fuente más grande</p>", unsafe_allow_html=True)

                        #Bar chart
                        with col2:
                            st.subheader('Frecuencia de temas en el documento')
                            df = di.get_conpes_topics(st.session_state.document_selected).sort_values(by='counttopic',ascending=False)
                            if len(st.session_state.search_bar) > 0:
                                filt_df_a = df[df['topic'].isin(st.session_state.search_bar)]
                                filt_df_b = df.head(10 - len(filt_df_a.index))
                                filt_df = pd.concat([filt_df_a,filt_df_b], axis=0).sort_values(by='counttopic',ascending=False)
                                
                            else:
                                filt_df = df.head(10)
                            chart = alt.Chart(data=filt_df,title = '', autosize='fit').mark_bar().encode(
                                x=alt.X('topic:N', title = 'Temas buscados',sort=None),
                                y=alt.Y('counttopic:Q', title='Frecuencia en el documento')
                                )
                            st.altair_chart(chart,use_container_width=True)
                            st.markdown("<p style='text-align: left; color: auto; font-size:85%'>Este gráfico muestra la frecuencia de aparición de las palabras buscadas en el documento seleccionado.</p>", unsafe_allow_html=True)

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
