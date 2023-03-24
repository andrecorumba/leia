import whisper
import streamlit as st
import os
import pandas as pd
import numpy as np

from audio_formats import to_mp3_bytes

def transcribe(folder, type_model):
    '''
    Função que transcreve uma lista de arquivos de áudio ou vídeo.

    Parameters:
        file_list (list): Lista de arquivos de áudio ou vídeo.
        folder (str): Caminho da pasta onde os arquivos estão.
        type_model (str): Tipo de modelo a ser utilizado.
        type_transcribe (str): Tipo de transcrição a ser realizada.

    Returns:
        dic_transcribe (dict): Dicionário com o nome do arquivo e o texto transcrito.
    '''
    
    # Load whisper model
    model = whisper.load_model(type_model)

    dic_transcribe = {'arquivo'     : [ ],
                      'transcricao' : [ ]}


    file_list = os.listdir(folder)
    st.write(file_list)

    for file in file_list:
    
        try:
    
            st.warning(f"Transcrevendo {file}")   

            result =  model.transcribe(os.path.join(folder,file)) 
            
            dic_transcribe['arquivo'].append(file)
            dic_transcribe['transcricao'].append(result['text'])
        
            st.success(f"Arquivo Transcrito: {file}")
    
        except Exception as e:
    
            st.error(f"Algo deu errado")
            st.error(e)
        
    return dic_transcribe
    