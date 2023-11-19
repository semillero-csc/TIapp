from maqueta.mensaje_principal import encabezado
from cuestionarios.formulario import formulario1
from archivos.doc_transcripcion import transcripcion_doc
from donaciones.donaciones_sc2 import donaciones
from app_transcripcion.speach_to_text import (mensaje_intruncciones,
                                              importar_audio_file,
                                              procesamiento_audio)


# Importamos y corremos la funcion encabezado del modulo mensaje principal. 
encabezado()

# importamos y corremos la funcion mensaje_intruncciones  del modulo speach_to_text que contiene el mensaje y las instrucciones de la app
mensaje_intruncciones()

# importamos y corremos la funcion importar_audio_file del modulo speach_to_text que contiene la caja para subir el archivo de audio
nombre_archivo = importar_audio_file()

# importamos y corremos la funcion procesamiento_audio del modulo speach_to_text que contiene los scripts para procesar el audio con Whisper
list_transcripciones = procesamiento_audio(nombre_archivo)
formulario_enviado = False

# importamos y corremos la funci[on ]
if len(list_transcripciones) > 0:
    formulario_enviado = formulario1(formulario_enviado)
    
if formulario_enviado == True:
    transcripcion_doc(list_transcripciones)
    donaciones()
    

