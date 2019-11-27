import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, datetime
from sklearn import preprocessing
from joblib import  load
from sklearn.linear_model import LogisticRegression

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

# Importo el modelo pre-entrenado, el scaler ajustado a la matriz de datos de entrenamiento del mismo y el dataframe con una fila de 0s
modelo = load('./modelos/trained_logres.joblib')
scaler = load('./modelos/scaler.joblib')
df = load('./modelos/df_vacio.joblib') #voy a reemplazar directamente en este df vacio el valor correspondiente



# Leo todos los dataframes de las opciones de los selectobox
#marcas = load_data('./data/marcas.csv')
modelos = load_data('./data/modelos.csv')
#tipos = load_data('./data/tipos.csv')
#paises = load_data('./data/paises.csv')
provincias = load_data('./data/provincias.csv')

# Primero ingresamos la fecha del robo
st.subheader('Fecha del robo:')

tramite_fecha = st.date_input('Fecha del robo')
registro_seccional_provincia = st.selectbox('Provincia donde hiciste la denuncia', provincias.T.squeeze())

# Ingresamos los datos del titular
st.subheader('Datos del titular:')

df['titular_anio_nacimiento'] = st.slider('Año de nacimiento', 1920, 2001, 1980) #corregí 'Edad' por 'Año de nacimiento' y género abajo
titular_genero = st.selectbox('Genero', ['Masculino', 'Femenino', 'No aplica'])
#titular_pais_nacimiento = st.selectbox('País de nacimiento', paises.T.squeeze())
titular_domicilio_provincia = st.selectbox('Provincia en la que vivís', provincias.T.squeeze())
if titular_domicilio_provincia != 'TUCUMAN': # sacar tucuman porque lo sacamos cuando unimos los dummies
  df[titular_domicilio_provincia] = 1 # acá hay que hacer un pequeño bypass porque la variable va a tomar el nombre de la feature del df

# Ingresamos los datos del automotor
st.subheader('Datos del vehículo:')

#automotor_marca_descripcion = st.selectbox('Marca', marcas.T.squeeze())
automotor_modelo_descripcion = st.selectbox('Modelo', modelos.T.squeeze())
if automotor_modelo_descripcion != 'ZAFIRA': #sacar zafira porque lo sacamos cuando unimos los dummies
  df[automotor_modelo_descripcion] = 1 # acá hay que hacer un pequeño bypass porque la variable va a tomar el nombre de la feature del df
df['automotor_anio_modelo'] = st.slider('Año de fabricación', 1950, 2019, 2010)
#automotor_tipo_descripcion = st.selectbox('Tipo', tipos.T.squeeze())
automotor_origen = st.selectbox('Origen del automotor', ['Nacional (incluye Mercosur)', 'Importado']) #saqué 'Protocolo 21', lo incluimos en nacional
automotor_uso_descripcion = st.selectbox('Uso del automotor', ['Privado', 'Público', 'Oficial']) # saqué 'No declarado', los dropeamos para entrenar
titular_tipo_persona = 'Fisica' # Algunos datos los llenamos a mano para no complicar las cosas, pero acá no habría que poner jurídica tmb?
titular_porcentaje_titularidad = st.selectbox('¿Sos único dueño?', ['Sí', 'No'])
# La fecha de inscripción la ponemos como el primero de enero del año del modelo del coche
#fecha_inscripcion_inicial = date(automotor_anio_modelo,1,1)

#Manipulaciones de las respuestas para que queden en el formato con el que entrenamos al modelo
df['unico_duenio'] = 1 if titular_porcentaje_titularidad == 'Sí' else 0
df['tit_radicado'] = 1 if titular_domicilio_provincia == registro_seccional_provincia else 0
df['importado'] = 1 if automotor_origen == 'Importado' else 0
df['titular_pers_fisica'] = 1 if titular_tipo_persona == 'Fisica' else 0
df['titular_masculino'] = 1 if titular_genero == 'Masculino' else 0
df['Oficial'] = 1 if automotor_uso_descripcion == 'Oficial' else 0
df['Privado'] = 1 if automotor_uso_descripcion == 'Privado' else 0

df['dia_robo'] = tramite_fecha.isoweekday()
df['mes_robo'] = tramite_fecha.month
df['dia_anio'] = tramite_fecha.timetuple().tm_yday


# Cuando se cliquea este checkbox, se arma el dataframe, se lo procesa, se lo
# escalea, se ajusta el modelo y se muestra el resultado en pantalla
if st.button('Calcular la probablidad!!!'):
  # Creación del dataframe
  #st.dataframe(df)
  # Escaleo de los Datos
  escalado = scaler.transform(df)

  # Hago correr el modelo y Calculo de la probablidad
  prediccion = modelo.predict(escalado)
  probabilidad = modelo.predict_proba(escalado)
  prob = probabilidad[0][1]
  #prob = .9

   # Ploteo de la probabilidad
  st.title('La probabilidad de que lo recuperes es de '+ str(round(prob*100,3))+ '%')

  plt.figure(figsize=(5,.5))
  plt.barh(1, prob, color = "green")
  plt.axis('off')
  plt.barh(1, (1-prob), color = "red", left = prob)
  axes = plt.gca()
  plt.axvline(x=.5, color="black")
  st.pyplot()

  if prob > .5:
    st.success("Suerte en esa :)")
  else:
    st.error("Lo siento amiguito :(")

