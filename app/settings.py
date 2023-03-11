import os
import streamlit as st
import whisper
import pandas as pd

def clean_folder(folder_path):
    with st.spinner(f"Removendo arquivos temporários..."):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                st.error(f"Erro ao remover {file_path} devido a {e}")

def select_model():   
    type_model = st.select_slider('Selecione o modelo: Quanto maior, mais preciso, porém mais lento na hora de transcrever', ['tiny','base', 'small', 'medium','large'], )
    return type_model

def adjust_settings(upload_path, download_path):
    st.subheader('Instalar Modelos')
    type_model =  select_model()
    if st.button('Instalar'):
        with st.spinner(f"Instalando modelo {type_model} ... 💫"):
            whisper.load_model(type_model)
            st.success(f"Modelo {type_model} instalado com sucesso!")
    
    if os.listdir(upload_path) or os.listdir(download_path):
        temp_files = len(os.listdir(upload_path)) + len(os.listdir(download_path))
        st.subheader('Arquivos Temporários')
        st.write(f"Foram encontrados {temp_files} arquivos temporários. Clique no botão abaixo para removê-los.")
        if st.button('Remover arquivos temporários'):
            with st.spinner(f"Removendo arquivos temporários ... 💫"):
                clean_folder(upload_path)
                clean_folder(download_path)
                st.success(f"Todos os arquivos temporários foram removidos com sucesso!")
        