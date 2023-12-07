import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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
    col1.header('Tabla de Pernoctaciones, Viajeros o Total')
    if 'Pernoctaciones' in tipo_datos_filter:
        col1.write(pernoctaciones_filtered[['Provincia','Periodo', 'Viajeros_Pernoctaciones', 'Residencia', 'Total']])
    elif 'Viajeros' in tipo_datos_filter:
        viajeros_filtered_subset = viajeros_filtered[viajeros_filtered['Residencia'].isin(viajeros_pernoctaciones_filter)]
        col1.write(viajeros_filtered_subset[['Provincia', 'Periodo', 'Viajeros_Pernoctaciones', 'Residencia', 'Total']])

    col2.header('Tabla de Clima')
    col2.write(clima_filtered[['Provincia', 'Periodo', 'Media_tmed', 'Media_prec', 'Media_sol', 'Media_tmin', 'Media_tmax']])





    altura_graficos = 400

    sns.set_theme(style="darkgrid", palette="dark:#001146")
    
    
    
    
    total_pernoctaciones = pernoctaciones_filtered.groupby('Provincia')['Total'].sum().reset_index()
    total_viajeros = viajeros_filtered.groupby('Provincia')['Total'].sum().reset_index()

    # Crear figura de Plotly Express
    fig = px.bar()
    # Verificar qué tipo de datos se ha seleccionado y agregar barras correspondientes
    if 'Pernoctaciones' in tipo_datos_filter:
        fig.add_bar(x=total_pernoctaciones['Provincia'], y=total_pernoctaciones['Total'],
                    name='Pernoctaciones', marker_color='#45E3E2', marker_line_color='black', marker_line_width=1)
    if 'Viajeros' in tipo_datos_filter:
        fig.add_bar(x=total_viajeros['Provincia'], y=total_viajeros['Total'],
                    name='Viajeros', marker_color='#1500FF', marker_line_color='black', marker_line_width=1)
    # Configuración de la figura
    fig.update_layout(
        title=f'Total Sumatorio de {", ".join(tipo_datos_filter)} por Provincia',
        xaxis_title='Provincia',
        yaxis_title='Total Sumatorio',
        paper_bgcolor='rgba(14, 17, 23, 1)',
        plot_bgcolor='rgba(234, 234, 242, 1)',
        xaxis=dict(gridcolor='white'),  # Color de la cuadrícula en el eje x
        yaxis=dict(gridcolor='white'),
    )

    # Mostrar la figura en Streamlit
    col1.plotly_chart(fig)



    
    


    # Diagrama de Caja para Temperaturas Medias
    # Verificar si el filtro es 'Media_tmed', 'Media_prec', 'Media_sol', 'Media_tmin', o 'Media_tmax'
    if clima_tipo_datos_filter in ['Media_tmed', 'Media_prec', 'Media_sol', 'Media_tmin', 'Media_tmax']:
    # Crear un diagrama de caja con los resultados
        fig = px.box(clima_filtered, x='Provincia', y=clima_tipo_datos_filter, color_discrete_sequence=['#1500FF'], points="all", title=f'Distribución de {clima_tipo_datos_filter} por Provincia')

        # Configuración de la figura
        fig.update_layout(
            xaxis_title='Provincia',
            yaxis_title=clima_tipo_datos_filter,
            paper_bgcolor='rgba(14, 17, 23, 1)',
            plot_bgcolor='rgba(234, 234, 242, 1)',
            xaxis=dict(gridcolor='white'),  # Color de la cuadrícula en el eje x
            yaxis=dict(gridcolor='white'),
        )
        
        fig.update_traces(marker=dict(color='#7936D9'), boxmean="sd")
    
        # Mostrar la figura en Streamlit
        col2.plotly_chart(fig)
    else:
        # Si el filtro no es válido, mostrar un mensaje o realizar otra acción
        col2.write("Selecciona un tipo de datos de clima válido para visualizar el diagrama de caja.")
        
        
        
        
        
        
        
        
        
        
        
    # Gráfico de Líneas para Pernoctaciones a lo largo de los meses
    
    # Crear un gráfico de líneas con los resultados
    fig = px.line(pernoctaciones_filtered, x='Periodo', y='Total', color='Provincia', title='Pernoctaciones a lo largo de los meses por Provincia')

    # Configuración de la figura
    fig.update_layout(
        xaxis_title='Mes',
        yaxis_title='Cantidad',
        paper_bgcolor='rgba(14, 17, 23, 1)',
        plot_bgcolor='rgba(234, 234, 242, 1)',
        xaxis=dict(gridcolor='white'),  # Color de la cuadrícula en el eje x
        yaxis=dict(gridcolor='white'),
    )

    # Cambiar el fondo del gráfico
    fig.update_layout(
        paper_bgcolor='rgba(14, 17, 23, 1)',
        plot_bgcolor='rgba(234, 234, 242, 1)',
        xaxis=dict(gridcolor='white'),  # Color de la cuadrícula en el eje x
        yaxis=dict(gridcolor='white'),
    )

    # Mostrar la figura en Streamlit
    col1.plotly_chart(fig)
        
        
        
        
        
        
        
    treemap_data = pd.DataFrame()
    if not pernoctaciones_filtered.empty:
        treemap_data = pernoctaciones_filtered.groupby('Provincia')['Total'].sum().reset_index()
        title = f'Treemap: Ranking de Provincias por Pernoctaciones ({fecha_inicio} - {fecha_fin})'
    elif not viajeros_filtered.empty:
        treemap_data = viajeros_filtered.groupby('Provincia')['Total'].sum().reset_index()
        title = f'Treemap: Ranking de Provincias por Viajeros ({fecha_inicio} - {fecha_fin})'
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados")

    # Crear el treemap
    if not treemap_data.empty:
        fig = px.treemap(treemap_data, path=['Provincia'], values='Total', title=title)
        col2.plotly_chart(fig)    
        
        





    # Crear subset antes de su uso
    viajeros_filtered_subset = viajeros_filtered[
    viajeros_filtered['Residencia'].isin(['Espana', 'Extranjero'])]

    # Verificar si el filtro es 'España' o 'Extranjero'
    if 'Espana' in viajeros_pernoctaciones_filter or 'Extranjero' in viajeros_pernoctaciones_filter:
        # Obtener el total de residentes en España y en el extranjero
        total_espana = viajeros_filtered_subset[viajeros_filtered_subset['Residencia'] == 'Espana']['Total'].sum()
        total_extranjero = viajeros_filtered_subset[viajeros_filtered_subset['Residencia'] == 'Extranjero']['Total'].sum()

        # Crear un gráfico de pastel con los resultados
        fig = px.pie(names=['España', 'Extranjero'], values=[total_espana, total_extranjero], title='Distribución de Tipo de Residencia de Viajeros', color_discrete_sequence=['#4C0035', '#B72F15'])

        # Configuración de la figura
        fig.update_layout(
            paper_bgcolor='rgba(14, 17, 23, 1)',
            plot_bgcolor='rgba(14, 17, 23, 1)',
        )

        # Mostrar la figura en Streamlit
        col2.plotly_chart(fig)
    else:
        # Si el filtro no es 'España' ni 'Extranjero', mostrar un mensaje o realizar otra acción
        col2.write("Selecciona 'España' o 'Extranjero' en el filtro para visualizar el gráfico de pastel.")





  
    # Mapa interactivo de Foursquare
    foursquare_map_url = "https://studio.foursquare.com/public/a8a7e4bf-fc29-4962-b9ea-74c4458d7d34"
    # Crear un iframe HTML para incrustar el mapa
    iframe_html = f'<iframe src="{foursquare_map_url}" width="100%" height="600"></iframe>'
    # Mostrar el iframe en Streamlit
    st.markdown(iframe_html, unsafe_allow_html=True)














