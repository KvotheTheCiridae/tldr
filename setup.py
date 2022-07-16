import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'CONPES_Explorer' #$Debe coincidir con el nombre de la carpeta.
AUTHOR = 'Olga Patricia Nieto, Daniel De León, Ernesto Alejandro Martínez, Alex Fabián Gómez, Marcela Sánchez Jiménez, Daniel Hernández, and David Aurelia Ayala Usma'
AUTHOR_EMAIL = '' 
URL = '' 

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Aplicación para la exploración y lectura interactiva de documentos CONPES aprobados.' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

#Paquetes necesarios para que funcione la aplicación.
INSTALL_REQUIRES = [
    'pdfplumber','requests','pandas','numpy','json','markupsafe==2.0.1','spacy','nltk','matplotlib.pyplot',
    'wordcloud','sqlalchemy', 'dash-extensions', 'psycopg2', 'pandas', 'numpy', 'matplotlib', 'wordcloud',
    'altair', 'streamlit', 'bs4', 'streamlit-option-menu','streamlit-text-rating','streamlit-tags','streamlit-cytoscapejs',
    'tkinter', 'webbrowser', 'streamlit-aggrid', 'streamlit-modal'
    ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)