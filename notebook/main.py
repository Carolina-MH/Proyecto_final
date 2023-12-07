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

page = st.sidebar.radio("Selecciona una página", ["Homepage", "Exploration"])

# Página de Inicio para Introducir Datos
if page == "Homepage":
    st.title('Bienvenido al Análisis de Datos de Turismo y Clima🧳🌤️')
    
elif page == "Exploration":
    st.title('Exploración de Datos - Todas las Gráficas')    

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
    tipo_datos_filter = st.sidebar.multiselect('Seleccionar Tipo de Datos', ['Pernoctaciones', 'Viajeros'])
    viajeros_pernoctaciones_filter= st.sidebar.multiselect('Seleccionar Tipo Viajeros/Pernoctaciones',['Espana', 'Extranjero'])
    clima_tipo_datos_filter = st.sidebar.selectbox('Seleccionar Tipo de Datos de Clima', ['Media_tmed', 'Media_prec', 'Media_sol', 'Media_tmin', 'Media_tmax'])
    


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


    
    
    
    # Visualizar datos

    col1, col2 = st.columns([1, 1]) 
    col1.header('Tabla de Pernoctaciones, Viajeros o Total según selección')
    if 'Pernoctaciones' in tipo_datos_filter:
        col1.write(pernoctaciones_filtered[['Provincia','Periodo', 'Viajeros_Pernoctaciones', 'Residencia', 'Total']])
    elif 'Viajeros' in tipo_datos_filter:
        viajeros_filtered_subset = viajeros_filtered[viajeros_filtered['Residencia'].isin(viajeros_pernoctaciones_filter)]
        col1.write(viajeros_filtered_subset[['Provincia', 'Periodo', 'Viajeros_Pernoctaciones', 'Residencia', 'Total']])

    col1.header('Tabla de Clima')
    col1.write(clima_filtered[['Provincia', 'Periodo', 'Media_tmed', 'Media_prec', 'Media_sol', 'Media_tmin', 'Media_tmax']])






    col2.header('Gráficos de Pernoctaciones y Viajeros')
    sns.set_theme(style="darkgrid", palette="dark:#001146")
    fig, ax = plt.subplots(figsize=(12, 6))
    # Verificar qué tipo de datos se ha seleccionado y crear barras correspondientes
    if 'Pernoctaciones' in tipo_datos_filter:
        sns.barplot(data=pernoctaciones_filtered, x='Provincia', y='Total', ci=None, ax=ax, color='#45E3E2', edgecolor='black', label='Pernoctaciones')
    if 'Viajeros' in tipo_datos_filter:
        sns.barplot(data=viajeros_filtered, x='Provincia', y='Total', ci=None, ax=ax, color='#1500FF', edgecolor='black', label='Viajeros')
    # Configuración del gráfico
    plt.title(f'Comparación de {", ".join(tipo_datos_filter)} por Provincia', color='white')
    plt.xlabel('Provincia', color='white')
    plt.ylabel('Cantidad', color='white')
    plt.xticks(rotation=45, ha='right', color='white')
    plt.yticks(color='white')
    plt.legend()  # Mostrar leyenda
    # Establecer el fondo del gráfico a negro
    fig.patch.set_facecolor('black')
    # Mostrar la figura en Streamlit
    col2.pyplot(fig)






    # Diagrama de Caja para Temperaturas Medias
    # Verificar si el filtro es 'Media_tmed', 'Media_prec', 'Media_sol', 'Media_tmin', o 'Media_tmax'
    if clima_tipo_datos_filter in ['Media_tmed', 'Media_prec', 'Media_sol', 'Media_tmin', 'Media_tmax']:
        # Crear un diagrama de caja con los resultados
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=clima_filtered, x='Provincia', y=clima_tipo_datos_filter, ax=ax, color='#FCB714', boxprops=dict(facecolor='#FCB714', color='#FCB714'), medianprops=dict(color='white'))
        # Ajustes del gráfico
        plt.title(f'Distribución de {clima_tipo_datos_filter} por Provincia', color='white')  # Título en blanco
        plt.xlabel('Provincia', color='white')
        plt.ylabel(clima_tipo_datos_filter, color='white')
        plt.xticks(rotation=45, ha='right', color='white')
        plt.yticks(color='white')
        # Establecer el fondo del gráfico a negro
        fig.patch.set_facecolor('black')
        # Mostrar la figura en Streamlit
        col2.pyplot(fig)
    else:
        # Si el filtro no es válido, mostrar un mensaje o realizar otra acción
        col2.write("Selecciona un tipo de datos de clima válido para visualizar el diagrama de caja.")





    # Crear subset antes de su uso
    viajeros_filtered_subset = viajeros_filtered[
        viajeros_filtered['Residencia'].isin(['Espana', 'Extranjero'])]
    # Verificar si el filtro es 'España' o 'Extranjero'
    if 'Espana' in viajeros_pernoctaciones_filter or 'Extranjero' in viajeros_pernoctaciones_filter:
        # Obtener el total de residentes en España y en el extranjero
        total_espana = viajeros_filtered_subset[viajeros_filtered_subset['Residencia'] == 'Espana']['Total'].sum()
        total_extranjero = viajeros_filtered_subset[viajeros_filtered_subset['Residencia'] == 'Extranjero']['Total'].sum()
        # Colores para el gráfico de pastel
        colores = ['#4C0035', '#B72F15']
        # Crear un gráfico de pastel con los resultados
        fig, ax = plt.subplots(figsize=(8, 8))
        plt.pie([total_espana, total_extranjero], labels=['España', 'Extranjero'], autopct='%1.1f%%', colors=colores, textprops=dict(color='white'))
        # Ajustes del gráfico
        plt.title('Distribución de Tipo de Residencia de Viajeros', color='white')  # Título en blanco
        # Establecer el fondo del gráfico a negro
        fig.patch.set_facecolor('black')
        # Mostrar la figura en Streamlit
        col2.pyplot(fig)  
        # Mostrar el total de residentes en España y en el extranjero
        col2.write(f"Total de residentes en España: {total_espana}")
        col2.write(f"Total de residentes en el Extranjero: {total_extranjero}")
    else:
        # Si el filtro no es 'España' ni 'Extranjero', mostrar un mensaje o realizar otra acción
        col2.write("Selecciona 'España' o 'Extranjero' en el filtro para visualizar el gráfico de pastel.")





  
    # Mapa interactivo de Foursquare
    foursquare_map_url = "https://studio.foursquare.com/public/a8a7e4bf-fc29-4962-b9ea-74c4458d7d34"
    # Crear un iframe HTML para incrustar el mapa
    iframe_html = f'<iframe src="{foursquare_map_url}" width="100%" height="600"></iframe>'
    # Mostrar el iframe en Streamlit
    st.markdown(iframe_html, unsafe_allow_html=True)














