import streamlit as st
import pandas as pd
import streamlit as st
import seaborn as sns
from PIL import Image
import pylab as plt
import webbrowser
import base64
import io

# Cargar datos
pernoctaciones = pd.read_csv('../data/ine_pernoctaciones.csv')
viajeros = pd.read_csv('../data/ine_viajeros.csv')
total = pd.read_csv('../data/ine_total.csv')
clima = pd.read_csv('../data/clima.csv')

# Configuración de página
st.set_page_config(
    page_title="Análisis de Datos de Turismo y Clima",
    page_icon="📊"
)

# Encabezado
st.title('Análisis de Datos de Turismo y Clima🧳🌤️')
st.sidebar.title('Filtros')



# Filtros
clima['Periodo'] = pd.to_datetime(clima['Periodo'])
pernoctaciones['Periodo'] = pd.to_datetime(pernoctaciones['Periodo'])
viajeros['Periodo'] = pd.to_datetime(viajeros['Periodo'])
total['Periodo'] = pd.to_datetime(total['Periodo'])

fecha_inicio = st.sidebar.date_input('Seleccionar Fecha de Inicio', clima['Periodo'].min())
fecha_fin = st.sidebar.date_input('Seleccionar Fecha de Fin', clima['Periodo'].max())

# Convierte fecha_inicio y fecha_fin a Timestamp
fecha_inicio = pd.Timestamp(fecha_inicio)
fecha_fin = pd.Timestamp(fecha_fin)

provincia_filter = st.sidebar.multiselect('Seleccionar Provincia(s)', pernoctaciones['Provincia'].unique())
tipo_datos_filter = st.sidebar.multiselect('Seleccionar Tipo de Datos', ['Pernoctaciones', 'Viajeros', 'Total'])

viajeros_pernoctaciones_filter= st.sidebar.multiselect('Seleccionar Tipo Viajeros/Pernoctaciones',['General', 'Espana', 'Extranjero'])

# Aplicar filtros
pernoctaciones_filtered = pernoctaciones.loc[
    (pernoctaciones['Provincia'].isin(provincia_filter)) & 
    (pernoctaciones['Periodo'] >= fecha_inicio) & 
    (pernoctaciones['Periodo'] <= fecha_fin)
]
viajeros_filtered = viajeros.loc[
    (viajeros['Provincia'].isin(provincia_filter)) & 
    (viajeros['Periodo'] >= fecha_inicio) & 
    (viajeros['Periodo'] <= fecha_fin)
]
clima_filtered = clima.loc[
    (clima['Provincia'].isin(provincia_filter)) & 
    (clima['Periodo'] >= fecha_inicio) & 
    (clima['Periodo'] <= fecha_fin)
]
total_filtered = total.loc[
    (total['Totales_Territoriales'].isin(provincia_filter)) & 
    (total['Periodo'] >= fecha_inicio) & 
    (total['Periodo'] <= fecha_fin)
]

# Visualizar datos
st.header('Tabla de Pernoctaciones, Viajeros o Total según selección')

if 'Pernoctaciones' in tipo_datos_filter:
    st.write(pernoctaciones_filtered[['Provincia','Periodo', 'Viajeros_Pernoctaciones', 'Residencia', 'Total']])
    
elif 'Viajeros' in tipo_datos_filter:
    viajeros_filtered_subset = viajeros_filtered[
        viajeros_filtered['Residencia'].isin(viajeros_pernoctaciones_filter)]
    st.write(viajeros_filtered_subset[['Provincia','Periodo', 'Viajeros_Pernoctaciones', 'Residencia', 'Total']])
    
elif 'Total' in tipo_datos_filter:
    total_filtered_with_additional_filter = total_filtered[
        total_filtered['Residencia'].isin(viajeros_pernoctaciones_filter)]
    st.write(total_filtered_with_additional_filter)


st.header('Tabla de Clima')
st.write(clima_filtered[['Provincia', 'Periodo', 'Media_tmed', 'Media_prec', 'Media_sol', 'Media_tmin', 'Media_tmax']])


    
# Mapa interactivo de Foursquare
foursquare_map_url = "https://studio.foursquare.com/public/a8a7e4bf-fc29-4962-b9ea-74c4458d7d34"
# Crear un iframe HTML para incrustar el mapa
iframe_html = f'<iframe src="{foursquare_map_url}" width="100%" height="600"></iframe>'
# Mostrar el iframe en Streamlit
st.markdown(iframe_html, unsafe_allow_html=True)



# Gráfico de barras para Pernoctaciones por Provincia
plt.figure(figsize=(12, 6))
sns.barplot(data=pernoctaciones_filtered, x='Provincia', y='Viajeros_Pernoctaciones', ci=None)
plt.title('Pernoctaciones por Provincia')
plt.xticks(rotation=45, ha='right')
st.pyplot();









