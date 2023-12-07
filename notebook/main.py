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
st.set_page_config(page_title="Análisis de Datos de Turismo y Clima", page_icon="📊")

#Configuración colores en la página
background_color = "#262730"
border_color = "#0068c9"
selected_color = "#83c9ff"
text_color = "#FFFFFF"

custom_css = f"""
    <style>
        .st-bw {{
            background-color: {background_color} !important; /* Fondo de la caja */
        }}
        .st-c7, .st-ec, .st-dh {{
            border: 1px solid {border_color} !important; /* Bordes y línea alrededor de la caja */
        }}
        .st-ew, .st-e0, .st-c2.st-c5.st-dq.st-ew.st-ex.st-c4.st-dw.st-e0.st-c7 {{
            background-color: {selected_color} !important; /* Fondo de las opciones seleccionadas */
            color: {text_color} !important;
        }}
        .css-145kmo2 {{
            background-color: {background_color} !important; /* Fondo de la selección de página */
            color: {text_color} !important; /* Texto blanco para la selección de página */
        }}
        .st-ci {{
            background-color: #404040 !important; /* Fondo gris oscuro para la barra lateral en la página "Exploration" */
            color: #FFFFFF !important; /* Texto blanco para la barra lateral en la página "Exploration" */
        }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

#Creación multipages
page = st.sidebar.radio("Selecciona una página", ["🏠Home", "🔥Mapa", "🔍Exploración"])
if page == "🏠Home":

    st.title('Análisis de Datos de Turismo y Clima🧳🌤️')
    video_path= '../img/home.mp4'
    st.video(video_path)
    
    st.markdown("""Sumérgete en un viaje a través de los últimos 10 años y descubre cómo la industria turística en España ha enfrentado
    desafíos, se ha adaptado a cambios y ha emergido con nuevas perspectivas después del impacto del COVID-19.""")
    
    st.header('Secciones Destacadas')
    
    st.subheader('Evolución Histórica📊🔄')
    st.markdown("""Viaja en el tiempo y explora cómo el turismo ha evolucionado desde 2014 hasta hoy. Descubre los secretos de la industria
    a través de patrones y tendencias.""")
    
    st.subheader('Impacto del COVID-19 🦠🌍')
    st.markdown("""Descubre cómo la pandemia de COVID-19 ha impactado directamente en el turismo en España. Analiza los cambios en las
    pernoctaciones, la llegada de viajeros y las regiones más afectadas.""")
    
    st.subheader('Recuperación y Tendencias Actuales 🚀🔍')
    st.markdown("""Despega hacia la fase post-COVID y observa cómo las provincias están mostrando signos de recuperación. Explora las
    nuevas tendencias que están definiendo el turismo actual en España.""")
    
    
elif page == "🔥Mapa":
    st.title('Destinos en el Mapa con Hexbin y Heatmap 🗺️🌡️')
    
    #Cargar el mapa itneractivo de Foursquare
    foursquare_map_url = "https://studio.foursquare.com/public/a8a7e4bf-fc29-4962-b9ea-74c4458d7d34"
    iframe_html = f'<iframe src="{foursquare_map_url}" width="100%" height="600"></iframe>'
    st.markdown(iframe_html, unsafe_allow_html=True)
    
    image_path = '../img/Leyenda.png'
    image = st.image(image_path)
    
    st.subheader('Recuperación y Tendencias Actuales 🚀🔍')
    st.markdown("""El heatmap revela una relación clara entre la temperatura y el flujo de viajeros. Cuando las temperaturas bajan,
    disminuye la afluencia de turistas. Destacan provincias como Madrid, Barcelona, Málaga, Granada y Alicante, sugiriendo que estos
    destinos mantienen cierta actividad incluso en estaciones más frescas, posiblemente debido a razones laborales o comerciales.
    En contraste, las Islas Baleares muestran una marcada disminución en invierno, mientras que las Islas Canarias, con temperaturas más
    cálidas, mantienen una afluencia constante.
    El impacto del COVID-19 fue significativo en el turismo español. A partir de la declaración de la pandemia, la afluencia turística se
    vio afectada por cierres de fronteras y restricciones de viaje. Notamos un declive notable a partir de octubre de 2019.La situación
    alcanzó su punto más bajo durante el verano de 2020, reflejando la marcada disminución de turistas debido a las restricciones
    implementadas. Sin embargo, a partir de abril de 2020, se evidencian signos de recuperación, mostrando la resiliencia del sector
    turístico y la adaptabilidad a las nuevas condiciones.""")
    
    st.subheader('Ranking de Pernoctaciones: Destinos Más Populares 🌙✨')
    st.markdown("""En el ámbito de pernoctaciones, las Islas Baleares lideran, seguidas por Las Palmas de Gran Canaria, Barcelona, Santa
    Cruz de Tenerife, Madrid y Málaga. Estos destinos destacan por su atractivo natural, historia rica y una oferta variada que atrae tanto
    a turistas de placer como a aquellos en busca de oportunidades laborales.""")
    
elif page == "🔍Exploración":
    st.title('1. Tendencias Temporales: Clima y Turismo')    

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
                    name='Pernoctaciones', marker_color='#83c9ff', marker_line_color='black', marker_line_width=1)
    if 'Viajeros' in tipo_datos_filter:
        fig.add_bar(x=total_viajeros['Provincia'], y=total_viajeros['Total'],
                    name='Viajeros', marker_color='#0068c9', marker_line_color='black', marker_line_width=1)
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
        fig = px.box(clima_filtered, x='Provincia', y=clima_tipo_datos_filter, color_discrete_sequence=['#ffabab'], points="all", title=f'Distribución de {clima_tipo_datos_filter} por Provincia')

        # Configuración de la figura
        fig.update_layout(
            xaxis_title='Provincia',
            yaxis_title=clima_tipo_datos_filter,
            paper_bgcolor='rgba(14, 17, 23, 1)',
            plot_bgcolor='rgba(234, 234, 242, 1)',
            xaxis=dict(gridcolor='white'),  # Color de la cuadrícula en el eje x
            yaxis=dict(gridcolor='white'),
        )
        
        fig.update_traces(
        boxmean="sd",  # Tipo de línea para la media y la línea del borde de la caja
        line_color='black',  # Color de la línea del borde de la caja, la línea de la media y los bigotes
    )
    
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
        
        





    viajeros_filtered_subset = viajeros_filtered[
    viajeros_filtered['Residencia'].isin(viajeros_pernoctaciones_filter)
    ]

    # Verificar si el filtro está seleccionado y si la opción es 'Viajeros'
    if 'Viajeros' in tipo_datos_filter and viajeros_pernoctaciones_filter:
        # Obtener el total de residentes según el filtro seleccionado
        total_residentes = viajeros_filtered_subset.groupby('Residencia')['Total'].sum()

        # Crear un gráfico de pastel con los resultados
        fig = px.pie(names=total_residentes.index, values=total_residentes.values, title='Distribución de Tipo de Residencia de Viajeros', color_discrete_sequence=['#32D7ED', '#7C32ED'])

        # Configuración de la figura
        fig.update_layout(
            paper_bgcolor='rgba(14, 17, 23, 1)',
            plot_bgcolor='rgba(14, 17, 23, 1)',
        )

        # Mostrar la figura en Streamlit
        st.plotly_chart(fig)
    # Verificar si el filtro está seleccionado y si la opción es 'Pernoctaciones'
    elif 'Pernoctaciones' in tipo_datos_filter and viajeros_pernoctaciones_filter:
        # Obtener el total de pernoctaciones según el filtro seleccionado
        total_pernoctaciones = pernoctaciones_filtered.groupby('Residencia')['Total'].sum()

        # Crear un gráfico de pastel con los resultados
        fig = px.pie(names=total_pernoctaciones.index, values=total_pernoctaciones.values, title='Distribución de Tipo de Residencia de Pernoctaciones', color_discrete_sequence=['#32D7ED', '#7C32ED'])

        # Configuración de la figura
        fig.update_layout(
            paper_bgcolor='rgba(14, 17, 23, 1)',
            plot_bgcolor='rgba(14, 17, 23, 1)',
        )

        # Mostrar la figura en Streamlit
        st.plotly_chart(fig)
    else:
        # Si no se selecciona un filtro válido, mostrar un mensaje o realizar otra acción
        st.write("Selecciona al menos un tipo de residencia y asegúrate de que el filtro de 'Viajeros/Pernoctaciones' está seleccionado para visualizar el gráfico de pastel.")





  
    














