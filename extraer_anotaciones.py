#!/usr/bin/env python
# coding: utf-8


#import glob
#files = glob.glob('./datos/*.xml', recursive = True)

from bs4 import BeautifulSoup
import streamlit as st
import re 

st.markdown("<p style='color: blue; font-size: 32px; font-weight: bold;'>¡Extraigamos las anotaciones de Transkribus! ✨</p>", unsafe_allow_html=True)

D = {}

uploaded_files = st.file_uploader("Elije uno o varios archivos Transkribus XML", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    data = BeautifulSoup(bytes_data, "xml")
    D[uploaded_file.name] = data

data_list = []
for key in D.keys():

    data_list += D[key].find_all('rs')

# Inicializar el diccionario
etiquetas = {}

# Iterar sobre la lista y extraer los datos
for item in data_list:
    # Utilizar expresiones regulares para extraer el tipo y el valor
    match = re.match(r"<rs type=\"([^\"]+)\">(.+)</rs>", str(item))
    if match:
        data_type = match.group(1)
        data_value = match.group(2)

        # Agregar el valor al diccionario en la lista correspondiente al tipo
        if data_type in etiquetas:
            etiquetas[data_type].append(data_value)
        else:
            etiquetas[data_type] = [data_value]

from collections import Counter

etiquetas = {key:dict(Counter(etiquetas[key]).most_common()) for key in etiquetas.keys()}
st.write(etiquetas)



