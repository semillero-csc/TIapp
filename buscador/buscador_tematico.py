from unidecode import unidecode
import pandas as pd 
import re


def buscador_and(palabras_claves, df):
    palabras_claves = [unidecode(palabra).lower() for palabra in palabras_claves]
    def verificador_de_palabras(texto):
        for palabra in palabras_claves:
            if palabra.lower() not in unidecode(texto).lower():
                return False
        return True  # Agregado para casos en los que no hay discrepancias
    
    df['coincidencia'] = df['intervencion'].apply(verificador_de_palabras)
    condiciones = df['coincidencia'] == True
    df_filtrado = df[condiciones].copy()
    
    # Eliminar la columna 'coincidencia'
    df_filtrado.drop('coincidencia', axis=1, inplace=True)
    
    return df_filtrado