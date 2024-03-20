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

def select_model(app_type):   
    '''
    Interface para o usuário selecionar o modelo de aprendizagem de máquina a ser usado na transcrição.

    Parameters:
        app_type (str): tipo do app 'web ou 'docker'
    
    Returns:
        (str): Nome do modelo de aprendizagem de máquina selecionado.
    '''
    if app_type == 'web':
        models_available = ['tiny','base']
    elif app_type == 'docker':
        models_available = ['tiny','base', 'small', 'medium','large'] 
    
    # Type 
    type_model = st.select_slider("Selecione o modelo: Quanto maior, mais preciso, porém mais lento na hora de transcrever. ", 
                                  models_available)
    return type_model

def install_models(app_type):
    ''' 
    Interface para o usuário ajustar as configurações da aplicação.
    '''
    st.subheader('Instalar Modelos de Aprendizagem de Máquina')
    type_model =  select_model(app_type)

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
        st.success("Pasta com Tokens removidas com sucesso!")
    
def read_secret_token(file_name):
    '''
    Lê o token secreto a partir de um arquivo.

    Parameters:
        file_name (str): Caminho do arquivo do token secreto.
    '''
    with open(file_name, 'r') as f:
        token = f.read().strip()
    return token