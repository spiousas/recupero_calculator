import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

st.title('Probabilidad de recupero de autos robados en Argentina')
st.write('Un trabajo de Brum, Carpaneto y Spiousas para ClusterAI')

st.write('Te robaron el auto y querés saber cuál es la probabilidad de que '+
         'se recupere?')

st.write('Ingresá tus datos y los del automotor y te decimos si vas a tener '+
         'la suerte (o la desgracia) de tenerlo de nuevo con vos')

# Función que queda en el cache (lee un datafram)
@st.cache
def load_data(filename):
    data = pd.read_csv(filename)
    return data

# Leo todos los dataframes de las opciones de los selectobox
marcas = load_data('./data/marcas.csv')
modelos = load_data('./data/modelos.csv')
tipos = load_data('./data/tipos.csv')
paises = load_data('./data/paises.csv')
provincias = load_data('./data/provincias.csv')

# Primero ingresamos la fecha del robo
st.subheader('Fecha del robo:')

tramite_fecha = st.date_input('Fecha del robo')
registro_seccional_provincia = st.selectbox('Provincia donde hiciste la denuncia', provincias.T.squeeze())

# Ingresamos los datos del titular
st.subheader('Datos del titular:')

titular_anio_nacimiento = st.slider('Edad', 1940, 2001, 1980)
titular_genero = st.selectbox('Año de nacimiento', ['Masculino', 'Femenino', 'No aplica'])
titular_pais_nacimiento = st.selectbox('País de nacimiento', paises.T.squeeze())
titular_domicilio_provincia = st.selectbox('Provincia en la que vivís', provincias.T.squeeze())

# Ingresamos los datos del automotor
st.subheader('Datos del vehículo:')

automotor_marca_descripcion = st.selectbox('Marca', marcas.T.squeeze())
automotor_modelo_descripcion = st.selectbox('Modelo', modelos.T.squeeze())
automotor_anio_modelo = st.slider('Año de fabricación', 1950, 2019, 2010)
automotor_tipo_descripcion = st.selectbox('Tipo', tipos.T.squeeze())
automotor_origen = st.selectbox('Origen del automotor', ['Nacional', 'Importado', 'Protocolo 21'])
automotor_uso_descripcion = st.selectbox('Uso del automotor', ['Privado', 'Público', 'No declarado', 'Oficial'])
titular_tipo_persona = 'Fisica' # Algunos datos los llenamos a mano para no complicar las cosas
titular_porcentaje_titularidad = 100
# La fecha de inscripción la ponemos como el primero de enero del año del modelo del coche
fecha_inscripcion_inicial = date(automotor_anio_modelo,1,1)

# Cuando se cliquea este checkbox, se arma el dataframe, se lo procesa, se lo
# escalea, se ajusta el modelo y se muestra el resultado en pantalla
if st.checkbox('Calcular la probablidad!!!'):
    # Creación del dataframe
    x = pd.DataFrame([[tramite_fecha, fecha_inscripcion_inicial,
                       registro_seccional_provincia, automotor_origen,
                       automotor_anio_modelo, automotor_tipo_descripcion,
                       automotor_marca_descripcion, automotor_modelo_descripcion,
                       automotor_uso_descripcion, titular_tipo_persona,
                       titular_domicilio_provincia, titular_genero,
                       titular_anio_nacimiento, titular_pais_nacimiento,
                       titular_pais_nacimiento]],
                       columns = ['tramite_fecha', 'fecha_inscripcion_inicial',
                       'registro_seccional_provincia', 'automotor_origen',
                       'automotor_anio_modelo', 'automotor_tipo_descripcion',
                       'automotor_marca_descripcion', 'automotor_modelo_descripcion',
                       'automotor_uso_descripcion', 'titular_tipo_persona',
                       'titular_domicilio_provincia', 'titular_genero',
                       'titular_anio_nacimiento', 'titular_pais_nacimiento',
                       'titular_pais_nacimiento'])
    st.dataframe(x)
    # Escaleo de los Datos

    # Calculo de la probablidad
    prob = .3

    # Ploteo de la probabilidad
    st.title('La probabilidad de que lo recuperes es de '+ str(prob*100)+ '%')

    plt.figure(figsize=(5,.5))
    plt.barh(1, prob, color = "green")
    plt.axis('off')
    plt.barh(1, (1-prob), color = "red", left = prob)
    axes = plt.gca()
    plt.axvline(x=.5, color="black")
    st.pyplot()

    if prob > .5:
      st.subheader("Suerte en esa :)")
    else:
      st.subheader("Lo siento amiguito :(")
