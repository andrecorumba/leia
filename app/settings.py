import os
import streamlit as st
import whisper
import shutil

def clean_folder(folder_path):
    '''
    Remove todos os arquivos temporários usados pela aplicação.

    Parameters:
        folder_path (str): Caminho da pasta onde os arquivos temporários estão armazenados.

    Example:
        >>> clean_folder('/uploads')
    '''
    with st.spinner(f"Removendo arquivos temporários..."):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                st.error(f"Erro ao remover {file_path} devido a {e}")

def select_model():   
    '''
    Interface para o usuário selecionar o modelo de aprendizagem de máquina a ser usado na transcrição.
    
    Returns:
        (str): Nome do modelo de aprendizagem de máquina selecionado.
    '''
    # type_model = st.select_slider('Selecione o modelo: Quanto maior, mais preciso, porém mais lento na hora de transcrever', 
    #                               ['tiny','base', 'small', 'medium','large'], )
    
    # Just 'tiny' and 'base' models are available for now
    type_model = st.select_slider("Selecione o modelo: Quanto maior, mais preciso, porém mais lento na hora de transcrever. "
                                  "Apenas os modelos 'tiny' e 'base' estão disponíveis no momento.", 
                                  ['tiny','base'], )
    return type_model

def install_models():
    ''' 
    Interface para o usuário ajustar as configurações da aplicação.
    '''
    st.subheader('Instalar Modelos de Aprendizagem de Máquina')
    type_model =  select_model()

    if st.button('Instalar'):
        with st.spinner(f"Instalando modelo {type_model} ... 💫"):
            whisper.load_model(type_model)
            st.success(f"Modelo {type_model} instalado com sucesso!")
    

def remove_token(folder_path):
    '''
    Remove todos os arquivos temporários usados pela aplicação por token.

    Parameters:
        folder_path (str): Caminho da pasta onde os arquivos temporários estão armazenados.
    '''

    if os.listdir(folder_path):
        shutil.rmtree(folder_path)