import streamlit as st
import pandas as pd
from PIL import Image
import pylab as plt
import webbrowser
import base64
import io


st.title('Visualización de Datos de Turismo')


st.header('Metodos para introducir texto')

st.header('Datos de Viajeros')
st.write(ine_viajeros)

st.header('Datos de Pernoctaciones')
st.write(ine_pernoctaciones)

st.header('Datos Totales')
st.write(ine_total)

st.header('Datos Climáticos')
st.write(ine_clima)