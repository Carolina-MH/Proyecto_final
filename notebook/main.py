import streamlit as st
import datetime as dt
import pandas as pd

from PIL import Image
import pylab as plt
import webbrowser
import base64
import io


st.set_page_config(
    page_title="Análisis de Datos de Turismo y Clima",
    page_icon="📊")

pernoctaciones = pd.read_csv('../data/ine_pernoctaciones.csv')
viajeros = pd.read_csv('../data/ine_viajeros.csv')
total = pd.read_csv('../data/ine_total.csv')
clima = pd.read_csv('../data/clima.csv')

#Encabezado
st.title('Análisis de Datos de Turismo y Clima🧳🌤️')
st.sidebar.title('Filtros')

#Filtros
clima['Periodo'] = pd.to_datetime(clima['Periodo'])
fecha_inicio = st.sidebar.date_input('Seleccionar Fecha de Inicio', clima['Periodo'].min())
fecha_fin = st.sidebar.date_input('Seleccionar Fecha de Fin', clima['Periodo'].max())
provincia_filter = st.sidebar.multiselect('Seleccionar Provincia(s)', pernoctaciones['Provincia'].unique())
tipo_datos_filter = st.sidebar.multiselect('Seleccionar Tipo de Datos', ['Pernoctaciones', 'Viajeros', 'Total'])

#DataFrames
foursquare_map_url = "https://studio.foursquare.com/public/a8a7e4bf-fc29-4962-b9ea-74c4458d7d34"

# Crea un iframe HTML para incrustar el mapa
iframe_html = f'<iframe src="{foursquare_map_url}" width="100%" height="600"></iframe>'

# Muestra el iframe en Streamlit
st.markdown(iframe_html, unsafe_allow_html=True)


