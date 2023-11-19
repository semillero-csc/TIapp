import streamlit as st
import datetime
import openai 
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
import datetime
from decouple import config
from dotenv import load_dotenv

import time
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset



def whisper3():
    permiso = False
    with st.spinner('Descargando modelo...'):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = "openai/whisper-large-v3"

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)

        processor = AutoProcessor.from_pretrained(model_id)
        global pipe
        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
        )
        permiso = True
    
        return permiso


def mensaje_intruncciones()->None:

    st.markdown(''' ## **Modelo: Speech to text** ''')
    
    st.markdown(
    '''
    Con ayuda de este modelo, podras transcribir tus audios solamente siguiendo estas instrucciones:\n
    1. Asegurate que los audios estén en formato .mp3, .m4a o .ogg y no pesen más de 20 MG.
    2. Arrastra o adjunta tu archivo en la caja receptora.
    3. Espera mientras termina de procesar el audio.
    4. Una vez termine el proceso, descarga tu archivo .dox el cual contendrá el texto formateado.

    Este y otros proyectos en construcción se sostendrán a lo largo del tiempo gracias a las donaciones.
    Si deseas y puedes contribuir a la causa, cualquier monto es bienvenido. Sin embargo, si no estás en
    posición de hacerlo en este momento, no te preocupes; siempre habrá otra oportunidad.
    Por ahora, disfruta de esta fantástica aplicación.:loudspeaker::technologist: 
    ''')
    

def importar_audio_file()->str:
    # Cargar el archivo de audio
    archivo_audio = st.file_uploader('Arrastra o ingresa tu archivo .mp3, .ma4, .ogg', type=['.mp3','.m4a', '.ogg'])
    nombre_archivo: str = ''            
    # Verificar si se ha cargado un archivo
    if archivo_audio is not None:
        nombre_archivo = archivo_audio.name
        # Abrir un archivo en modo escritura binaria ('wb') para guardar el archivo de audio
        
        with open(f'archivos/audios/{nombre_archivo}', 'wb') as new_file:
            # Leer los datos del archivo cargado y escribirlos en el nuevo archivo
            new_file.write(archivo_audio.read())

        st.success(f'Archivo de audio "{nombre_archivo}" ha sido guardado exitosamente.')
        # No olvides manejar los casos en los que no se cargue un archivo o haya algún error.
        st.success(f'Archivo de audio "{nombre_archivo}" pronto estará procesandose.')
    
    return nombre_archivo

        
def procesamiento_audio(nombre_archivo: str)->list: 
    # Procesamiento del audio con Whisper-1

    resultado: str = ''
    list_transcripciones: dict = []
    fecha_hora_actual = datetime.datetime.now()
    fecha_hora = f"{fecha_hora_actual.strftime('%Y-%m-%d__%H:%M:%S')}"

    # Abre el archivo de audio
    if nombre_archivo:
        resultado = pipe(f'archivos/audios/{nombre_archivo}')
    print(f'Este es el resultado ------> {resultado}')
    
    list_transcripciones.append({'nombre_archivo': nombre_archivo,
                                'texto': resultado['text'],
                                'fecha': fecha_hora,
                                'numero_palabras': len(resultado.strip().split())})

    print(f'El archivo: {nombre_archivo} ha sido procesado\n', sep='-->')
    print(list_transcripciones)

    st.success(f'Archivo de audio "{nombre_archivo}" ha sido procesado.')
    st.markdown(''' ## **Texto:** ''')

    texto_a_mostar = ''
    num_caracteres = 0
    if len(list_transcripciones) > 0:
        
        texto_a_mostar = list_transcripciones[0]['texto']
        num_caracteres = round(len(texto_a_mostar) /3)
        
        st.write(f'''
        {texto_a_mostar[:num_caracteres]}...
        ''')
        st.success(f'El resto del texto lo podrás descargar una vez diligencies el formulario')
    
    return list_transcripciones


