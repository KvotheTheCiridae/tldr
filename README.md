TL DR Too Long Didn't Read App
#----------------------------------------------------------------------------
# Created By: Olga Patricia Nieto, Daniel De León, Ernesto Alejandro Martínez, Alex Fabián Gómez, Marcela Sánchez Jiménez, Daniel Hernández, and David Aurelia Ayala Usma
# Created Date: 2022-07-07
# Version = 0.0.1
# ---------------------------------------------------------------------------
Requirements

General requirements: Can be found in the file setup.py
Front End Requirements


# --------------------------------------------------------------------------
Contents

1. shared - General storage for backend and general information not used directly in the use of the app
    1.1 assets/logo - Folder containing general images for the project as procolombia logo, team 19 logo.
    1.2 datasets - Folder containing general datasets extracted from various sources that may be called by the backend set up for complementary information
    1.3 EDA_Notebooks - Folder Containing different Jupiter Notebooks used to handle the backend information for testing and analysis before publishing the backend production modules
    1.4 PDF - Folder that receives and contains the web-scrapped PDF files of CONPES Documents during the backend set up process and must contain the documents for the database set-up process for processing.
2. src - Folder that contains the information needed to run the back-end and front-end of the app
    2.1 front_end - Contains the files and scripts related to the front-end functioning of the app
        2.1.1 app - This folder contains the scripts related to the streamlit service and all the front-end behavior (Here the file tldr.py must be initializated using the command streamlit run tldr.py in order to get front-end app deployed)
            2.1.1.1 __pycache__ - General cache information for the pages generated
            2.1.1.2 .streamlit - Contains the file for theme / color / style setting in the streamlit app
            2.1.1.3 frontend_behavior - Contains two scripts that control the functions and behavior of the front-end by doing calculations and calling the module data_interface for requests to the SQL database.
            2.1.1.4 page - Contains the pages of the app besides the home view. Most of the interactions and callbacks from users are handled and displayed from the code in each page script.
        2.1.2 assets - images used in the front-end (logos)
        2.1.3 data - common files used in the front-end (mainly for testing and debugging)
    2.2 modules - Contains the module folders for the back-end set-up and front end connection
        2.2.1 conpes_db - Contains the module script for processing the PDF files scrapped using the pdf_processor and topic_modeling modules and doing the full set-up (creation and upload) of the database. Backend setup Step 2
        2.2.2 conpes_download - Contains the module script for webscrapping of the CONPES documents to download them into the shared/PDF folder. Back-end setup Step 1
        2.2.3 data_interface - Contains the module script that contains the connections called by the front-end to get information from the database.
        2.2.4 pdf_processor - Contains the module script for PDF to text transformation and also divide the document into pages / paragraphs and extracting the executive summary, classification and keywords
        2.2.5 topic_modeling Contains the module script that transform text by using NLP tools like regex, NLTK and the spanish spaCy pipeline for processing into non-stop words, lemmas and standarization to keep only significative terms for the search and topic identification within the text.

#-------------------------------------------------------------------------
Back-End Setup process
1. Run the Source/modules/conpes_download script from the bash terminal for webscraping the PDF documents of the files from the DNP site. You can select the Year range of the documents webscrapped
2. Run the Source/modules/conpes_db script from the bash terminal to process all PDF documents in the shared/PDF folder using the pdf_processor and topic_modeling modules. (Takes about 2 hours to set up)

#------------------------------------------------------------------------
App Deployment process
1. Run the src/app/tldr.py script from the bash terminal using the command 'streamlit run tldr.py'

