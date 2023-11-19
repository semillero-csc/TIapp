import streamlit as st
from PIL import Image
import base64
import time
import pandas as pd
from maqueta.mensaje_principal import encabezado
from enviar_correo.correo import  correo2

#from motor_de_busqueda.motor_busqueda.pdf_miner import limpiador1
#from motor_de_busqueda.patrones_regex.patrones_actas import Patrones_actas
#from motor_de_busqueda.motor_busqueda.busqueda_tematica import unakey, operador_or, operador_and
import pandas as pd 
from unidecode import unidecode
import re

# Definimos las variables
df_resultado = None
motrar_resultado: bool = False
palabras_claves:list = None
keyword = None
ruta_nombre_archivo = 'resultados_busque/resultados_busqueda.csv'
mostrar_descarga_correo = False

encabezado()

# Encabezado de la aplicación
st.markdown(''' ## **Buscador Temático - Actas del Concejo de Medellín** 🕵️‍♂️📜 ''')

# Configuración de la Búsqueda:
st.write("""
   - En la sección "Ingresa el operador lógico y las palabras clave":
      - Selecciona el operador lógico (AND, OR, NONE) que mejor se adapte a tu búsqueda. 🤔
      - Si utilizas solo una palabra clave, selecciona el operador lógico 'NONE'. 🧐
      - En el cuadro de texto, introduce una o varias palabras clave, separadas por comas, que desees buscar dentro de las intervenciones del Concejo de Medellín. 📚
      - Una vez completada la búsqueda, puedes interactuar directamente con la tabla que se despliega. 🎉 Descárgala mediante el botón 'Descargar CSV' o envíala al correo que prefieras. 📤
""")


st.write("**HERE ADD ONE DESCRIPTION**")
keyword_list: list = []
st.markdown('### **Ingresa el operador lógico y las palabras clave**')

st.write("Puedes ingresar una o varias palabras clave, junto con un único operador lógico.")

with st.form("Ingresa el operador lógico y las palabras clave"):
    operador = st.selectbox('Operador: AND - OR - NONE',
                            ('AND', 'OR', 'NONE'))
    keyword = st.text_input('Ingrese la(s) palabra(s) clave(s). En caso de múltiples palabras clave, ingréselas separadas por comas.')
    keyword = keyword.lstrip().rstrip().split(',')
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        with st.spinner('Buscando...'):
            df_procesadas = pd.read_csv('intervenciones_concejo_medellin.csv')

            def buscador_and(palabras_claves, df):
                palabras_claves = [unidecode(palabra).lower() for palabra in palabras_claves]
                def verificador_de_palabras(texto):
                    for palabra in palabras_claves:
                        if palabra.lower().strip() not in unidecode(texto).lower():
                            return False
                    return True  # Agregado para casos en los que no hay discrepancias
                
                df['coincidencia'] = df['intervencion'].apply(verificador_de_palabras)
                condiciones = df['coincidencia'] == True
                df_filtrado = df[condiciones].copy()
                
                # Eliminar la columna 'coincidencia'
                df_filtrado.drop('coincidencia', axis=1, inplace=True)
                
                return df_filtrado

            palabras_claves: list = keyword
            expresion_regular: str = '|'.join(palabras_claves)

            # Dataframe con una palabras claves y operador NONE
            df_intervenciones_filtrado_una_key = df_procesadas[df_procesadas['intervencion'].str.contains(palabras_claves[0], case=False)]

            # Dataframe con las palabras palabras claves y operador OR
            df_intervenciones_filtrado_or = df_procesadas[df_procesadas['intervencion'].str.contains(expresion_regular, case=False, regex=True)]

            # Dataframe con las palabras palabras claves y operador AND
            df_intervenciones_filtrado_and = buscador_and(palabras_claves, df_procesadas)

            dict_intervenciones_filtradas: dict = {
                'OR': df_intervenciones_filtrado_or,
                'AND': df_intervenciones_filtrado_and,
                'NONE': df_intervenciones_filtrado_and
            }

            motrar_resultado = True

            df_resultado = None
            df_resultado = dict_intervenciones_filtradas[f'{operador}']
            df_resultado['intervencion'] = df_resultado['intervencion'].apply(lambda x: x.replace("@@@", ''))
            
            st.markdown(f'### La búsqueda temática generó {len(df_resultado)} resultados')

            # Muestra las primeras 10 filas del DataFrame en Streamlitdf_intervenciones_fil
            if motrar_resultado == True:
                st.dataframe(df_resultado, use_container_width=True)
        
                # Guardar el DataFrame como un archivo CSV 
                ruta_nombre_archivo = 'resultados_busque/resultados_busqueda.csv'
                df_resultado.to_csv(ruta_nombre_archivo, index=False)  # No incluye el índice en el archivo CSV
                mostrar_descarga_correo = True
                st.success('¡Búsqueda completada!')

#if mostrar_descarga_correo == True:
with st.spinner('Enviando...', ):
    # Agregar un botón para descargar el archivo CSV
    with open(ruta_nombre_archivo, "r") as file:
        btn = st.download_button(
            label="Descargar CSV",
            data=file,
            file_name='resultados_busqueda.csv',
        )
        
# Agregar un botón para enviar por correo electrónico
    with st.form("Ingresa el correo electronico"):
        correo_destino = st.text_input('Ingrese el correo electrónico de destino y luego Submit')
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success(f'El correo al que se enviará el archivo es: {correo_destino}')  
            correo2(ruta_nombre_archivo,correo_destino)
            st.balloons()
            
st.write("Outside the form")
#st.stop()



