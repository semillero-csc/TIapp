import smtplib
import ssl
from email.message import EmailMessage
from decouple import config
from email.message import EmailMessage
import ssl
import smtplib
import random
import streamlit as st



def correo2(nombre_archivo_docx:str, imail_usuario: str):
    enviado = False
    # Esto es para enviar el archivo a un correo
    imail_emisor = config('CORREO_PERSONAL')
    imail_contraseña = config('GOOGLE_KEY')
    imail_receptor = imail_usuario
    asunto = 'Resultado de la busqueda temática'
    cuerpo = 'Se adjunta archivo de la búsqueda temática'

    em = EmailMessage()
    em['From'] = imail_emisor
    em['To'] = imail_receptor
    em['Subject'] = asunto
    em.set_content(cuerpo)

    with open(nombre_archivo_docx, "rb") as f:
        em.add_attachment(
            f.read(),
            filename=nombre_archivo_docx,
            maintype="application",
            subtype="csv"
        )

    contexto = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
        smtp.login(imail_emisor, imail_contraseña)
        smtp.sendmail(imail_emisor, imail_receptor, em.as_string()) 
        smtp.quit()
        enviado = True
        if enviado == True:
            st.success('El correo ha sido enviado')


def correo_validacion(imail_usuario: str, codigo_verificacion:str):
    #codigo  = str(random.randint(1000, 9999))
    # Configuración del correo
    imail_emisor = config('CORREO_PERSONAL')
    imail_contraseña = config('GOOGLE_KEY')
    imail_receptor = imail_usuario

    asunto = 'Código de verificación'
    cuerpo = f'Codigo de verificación: {codigo_verificacion}'

    # Crear el objeto EmailMessage
    em = EmailMessage()
    em['From'] = imail_emisor
    em['To'] = imail_receptor
    em['Subject'] = asunto
    em.set_content(cuerpo)

    # Configuración del servidor SMTP
    contexto = ssl.create_default_context()

    # Enviar el correo sin adjunto
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
        smtp.login(imail_emisor, imail_contraseña)
        smtp.sendmail(imail_emisor, imail_receptor, em.as_string()) 
        smtp.quit()

    # Mostrar mensaje de éxito
    st.success('Se ha enviado a tu correo un codigo de validación para autenticar tu registro.')


