import streamlit as st
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
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


sns.set_theme(style="darkgrid", palette="dark:#001146")

# Diagrama de Barras para Pernoctaciones
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=pernoctaciones_filtered, x='Provincia', y='Total', ci=None, ax=ax, color='#001146', edgecolor='black')  # Barras azules oscuro
plt.title('Pernoctaciones por Provincia', color='white')  # Título en blanco
plt.xlabel('Provincia', color='white')  # Etiqueta del eje x en blanco
plt.ylabel('Número de Pernoctaciones', color='white')  # Etiqueta del eje y en blanco
plt.xticks(rotation=45, ha='right', color='white')  # Etiquetas del eje x en blanco
plt.yticks(color='white')  # Etiquetas del eje y en blanco
# Establecer el fondo del gráfico a negro
fig.patch.set_facecolor('black')
# Mostrar la figura en Streamlit
st.pyplot(fig)


# Diagrama de Caja para Temperaturas Medias
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=clima_filtered, x='Provincia', y='Media_tmed', ax=ax, color='#001146', boxprops=dict(facecolor='black', color='black'), medianprops=dict(color='white'))  # Caja negra, mediana blanca
plt.title('Distribución de Temperaturas Medias por Provincia', color='white')  # Título en blanco
plt.xlabel('Provincia', color='white')  # Etiqueta del eje x en blanco
plt.ylabel('Temperatura Media', color='white')  # Etiqueta del eje y en blanco
plt.xticks(rotation=45, ha='right', color='white')  # Etiquetas del eje x en blanco
plt.yticks(color='white')  # Etiquetas del eje y en blanco
# Establecer el fondo del gráfico a negro
fig.patch.set_facecolor('black')
# Mostrar la figura en Streamlit
st.pyplot(fig)





# Crear subset antes de su uso
viajeros_filtered_subset = viajeros_filtered[
    viajeros_filtered['Residencia'].isin(viajeros_pernoctaciones_filter)]
# Contar la distribución de 'Residencia'
residencia_counts = viajeros_filtered_subset['Residencia'].value_counts()
# Crear un gráfico de pastel con los resultados
fig, ax = plt.subplots(figsize=(8, 8))
residencia_counts.plot.pie(autopct='%1.1f%%', labels=residencia_counts.index, ax=ax, colors=['#001146', 'black'])  # Azul oscuro y negro
plt.title('Distribución de Tipo de Residencia de Viajeros', color='white')  # Título en blanco
# Establecer el fondo del gráfico a negro
fig.patch.set_facecolor('black')
# Mostrar la figura en Streamlit
st.pyplot(fig)


    
# Mapa interactivo de Foursquare
foursquare_map_url = "https://studio.foursquare.com/public/a8a7e4bf-fc29-4962-b9ea-74c4458d7d34"
# Crear un iframe HTML para incrustar el mapa
iframe_html = f'<iframe src="{foursquare_map_url}" width="100%" height="600"></iframe>'
# Mostrar el iframe en Streamlit
st.markdown(iframe_html, unsafe_allow_html=True)















