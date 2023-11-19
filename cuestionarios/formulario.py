import streamlit as st
import json
import os
from datetime import datetime
import re

def formulario1(formulario_enviado:bool):
    formulario_enviado = False
    # Definir el nombre del archivo JSON
    archivo_json = "formulario_data.json"

    # Verificar si el archivo JSON ya existe
    if os.path.exists(archivo_json):
        # Cargar los datos existentes desde el archivo JSON
        with open(archivo_json, "r") as json_file:
            formularios = json.load(json_file)
    else:
        # Si el archivo no existe, crear una lista vacía
        formularios = []
        
    with st.form("Ingresa el correo electronico"):
        nombre = st.text_input("Nombre completo")
        correo = st.text_input("Correo institucional")
        rol = st.text_input("Rol en la Universidad")
        dependencia = st.text_input("Dependencia")
        semillero_grupo = st.text_input("Semillero o Grupo", "Si no perteneces a ningún grupo, solo pon 'No'")
        interes_inv = st.text_input("Interés investigativo")
        comentario = st.text_input("¿Qué piensas sobre nuestros desarrollos?")

        submitted = st.form_submit_button("Submit")
        if submitted:
            if re.search(r".+?@udea.edu.co",correo): 
                # Obtener la fecha y hora actual
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Crear un diccionario con la información del formulario, incluyendo la fecha
                nuevo_datos = {
                    "Fecha": fecha_actual,
                    "Nombre": nombre,
                    "Correo": correo,
                    "Rol": rol,
                    "Dependencia": dependencia,
                    "Semillero o Grupo": semillero_grupo,
                    "Interés investigativo": interes_inv,
                    "Comentario": comentario
                }

                # Agregar el nuevo formulario a la lista de formularios
                formularios.append(nuevo_datos)

                # Guardar la lista actualizada en el archivo JSON
                with open(archivo_json, "w", encoding="utf-8") as json_file:
                    json.dump(formularios, json_file, indent=4, ensure_ascii=False)

                if st.success(f'El cuestionario ha sido enviado. Ahora puedes descargar el archivo que contiene el texto de la transcripción'):
                    formulario_enviado = True
            else:
                st.error(f'El correo no es válido')
                
        st.write("Outside the form")
    

    return formulario_enviado

