import json
import os
import streamlit as st
from enviar_correo.correo import  correo2


# Función para la autenticación del usuario.


def autenticacion_usuario():
    correo: str = None
    nombre: str = None
    permiso_ingreso: bool = False
    correo_autenricacion = None
    # Lee el contenido del archivo JSON
    with open('formulario_data.json', 'r') as file:
        lista_de_diccionarios = json.load(file)


    with st.form('Autenticación'):
        correo_usuario: str = st.text_input('ingresa el correo')
        contraseña: str = st.text_input('iIngrese la contraseña', type="password")
        if st.form_submit_button('Autenticar'):
            for diccionario in lista_de_diccionarios:
                if diccionario['Correo'] == correo_usuario and diccionario['Contraseña'] == contraseña:
                    correo = correo_usuario
                    nombre = diccionario['Nombre']
                    st.success('Usuario autenticado correctamente.')
                    permiso_ingreso = True 
                    break
                else:
                    continue
            if permiso_ingreso == False:
                st.error("No se pudo realizar la autenticación con los datos proporcionados. Verifiquelos o registrese.")
            
    return permiso_ingreso, correo, nombre            
                    

def historial_usuario(correo: str, app: str):
    archivo_json = 'historial_usuario_app.json'

    # Verifica si el archivo JSON existe
    if os.path.exists(archivo_json):
        with open(archivo_json, "r") as json_file:
            datos_uso = json.load(json_file)
    else:
        # Si el archivo no existe, inicializa datos_uso como un diccionario vacío
        datos_uso = {}

    # Verifica si el correo está presente en datos_uso
    if correo in datos_uso:
        # Verifica si la aplicación está presente en el historial del usuario
        if app in datos_uso[correo]:
            datos_uso[correo][app] += 1
        else:
            # Si la aplicación no está en el historial del usuario, inicializa su contador a 1
            datos_uso[correo][app] = 1
    else:
        # Si el correo no está en datos_uso, inicializa su entrada con la aplicación y el contador a 1
        datos_uso[correo] = {app: 1}

    # Guarda los datos actualizados en el archivo JSON
    with open(archivo_json, "w", encoding="utf-8") as json_file:
        json.dump(datos_uso, json_file, indent=4, ensure_ascii=False)