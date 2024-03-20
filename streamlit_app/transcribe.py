import whisper
import streamlit as st
import os
import pandas as pd
import numpy as np

def transcribe(folder, type_model):
    '''
    Função que transcreve uma lista de arquivos de áudio ou vídeo.

    Parameters:
        folder (str): Caminho da pasta com os arquivos de áudio ou vídeo.
        type_model (str): Tipo de modelo a ser utilizado na transcrição.

    Returns:
        dic_transcribe (dict): Dicionário com o nome do arquivo e o texto transcrito.
    '''
    
    # Load whisper model
    model = whisper.load_model(type_model)

    dic_transcribe = {'arquivo'     : [ ],
                      'transcricao' : [ ]}
    
    audio_file_extensions = (".opus",".wav",".mp3",".ogg",".wma",
                             ".mp4", ".m4a", ".avi", ".mov", ".wmv")


    file_list = os.listdir(folder)

    for file in file_list:

        # Check if file is audio or video and not a hidden file
        if not file.startswith(".") and file.lower().endswith(audio_file_extensions):
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
    