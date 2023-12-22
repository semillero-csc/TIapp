import streamlit as st
import json
import os
from datetime import datetime
import re
import random
from maqueta.mensaje_principal import encabezado
from enviar_correo.correo import correo_validacion

encabezado()

codigo = None


def formulario1(formulario_enviado: bool):
    formulario_enviado = False
    archivo_json = "formulario_data.json"

    if os.path.exists(archivo_json):
        with open(archivo_json, "r") as json_file:
            formularios = json.load(json_file)
    else:
        formularios = []

    st.write("Ingresa el correo electrónico")
    validador_de_proceso = True

    with st.form("Datos personales"):
        nombre = st.text_input("Nombre completo")
        correo = st.text_input("Correo institucional")
        contraseña = st.text_input("Ingrese una contraseña", type="password")
        validador_de_contraseña = st.text_input("Ingrese de nuevo la contraseña", type="password")
        rol = st.selectbox("Selecciona tu rol:", ["Estudiante", "Profesor", "Investigador", "Trabajador", "Otro"])
        programa = st.text_input("Ingresa el programa del que haces parte")
        facultad_dependencia = st.text_input("Dependencia")
        semillero_grupo = st.text_input("Semillero o Grupo", "Si no perteneces a ningún grupo, solo pon 'No'")
        interes_inv = st.text_input("Interés investigativo")
        comentario = st.text_input("¿Qué piensas sobre nuestros desarrollos?")

        if st.form_submit_button("Enviar datos"):
            if validador_de_proceso:
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nuevo_datos = {
                    "Fecha": fecha_actual,
                    "Nombre": nombre.title(),
                    "Correo": correo,
                    "Contraseña": contraseña,
                    "Rol": rol,
                    "Programa": programa,
                    "Dependencia": facultad_dependencia,
                    "Semillero_o_Grupo": semillero_grupo,
                    "Interés_investigativo": interes_inv,
                    "Comentario": comentario
                }
                formularios.append(nuevo_datos)
                with open(archivo_json, "w", encoding="utf-8") as json_file:
                    json.dump(formularios, json_file, indent=4, ensure_ascii=False)
                formulario_enviado = True

    
    with st.form("Código de validación"):
        random.seed(len(nombre))
        codigo = str(random.randint(1000, 9999))
        try:
            correo_validacion(correo, codigo)
        except:
            print("Error")
        verificacion_codigo_autenticacion = st.text_input("Ingrese el código de verificación")
        if st.form_submit_button("Verificar código"):
            if verificacion_codigo_autenticacion and len(verificacion_codigo_autenticacion) == 4:
                if verificacion_codigo_autenticacion == codigo:
                    st.success('El usuario ha sido creado.')
                else:
                    st.error('El código de verificación no coincide.')

    return formulario_enviado

formulario_enviado = formulario1(True)



