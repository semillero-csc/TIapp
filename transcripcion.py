import streamlit as st
import os
import json
from datetime import datetime
from maqueta.mensaje_principal import encabezado
from autenticacion.autenticar import autenticacion_usuario, historial_usuario
from archivos.doc_transcripcion import transcripcion_doc
from donaciones.donaciones_sc2 import donaciones
from app_transcripcion.speach_to_text import (mensaje_intruncciones,
                                              importar_audio_file2,
                                              procesamiento_audio3,
                                              whisper3,
                                              whisper4)


from datetime import datetime
import datetime
import time
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline





# Importamos y corremos la funcion encabezado del modulo mensaje principal. 
encabezado()

# importamos y corremos la funcion mensaje_intruncciones  del modulo speach_to_text que contiene el mensaje y las instrucciones de la app
mensaje_intruncciones()
with st.spinner('Cargando el modelo para la transcripción...', ):
    pipe = whisper4()
    result = None

formulario_enviado = False

# importamos y corremos la funcion importar_audio_file del modulo speach_to_text que contiene la caja para subir el archivo de audio

nombre_archivo = importar_audio_file2()
ruta_archivo = f'archivos/audios/{nombre_archivo}'


if len(nombre_archivo) > 0:
    formulario_enviado, correo, nombre = autenticacion_usuario()

if formulario_enviado == True:
    
    historial_usuario(correo, 'transcriptor') 
    # importamos y corremos la funcion procesamiento_audio del modulo speach_to_text que contiene los scripts para procesar el audio con Whisper
    
    with st.spinner('Transcribien... El proceso puede tardar.', ):
        result = pipe(ruta_archivo, return_timestamps=True, generate_kwargs={"language": "spanish"})
        
        
        list_transcripciones = procesamiento_audio3(ruta_archivo, nombre_archivo, result)
        transcripcion_doc(list_transcripciones)
        donaciones()
        
        archivo_json = 'historial_uso_app.json'
        if os.path.exists(archivo_json):
            with open(archivo_json, "r") as json_file:
                datos_uso = json.load(json_file)
        else:
            datos_uso = []  
            
        from datetime import datetime
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        datos = {
            'nombre_usuario': nombre,
            'correo' : correo,
            'fecha': fecha_actual,
            'aplicacion_usada': 'transcriptor'
        }

        datos_uso.append(datos)
        with open(archivo_json, "w", encoding="utf-8") as json_file:
            json.dump(datos_uso, json_file, indent=4, ensure_ascii=False)  