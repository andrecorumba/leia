import os
import streamlit as st
import whisper

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
    type_model = st.select_slider('Selecione o modelo: Quanto maior, mais preciso, porém mais lento na hora de transcrever', 
                                  ['tiny','base', 'small', 'medium','large'], )
    return type_model

def adjust_settings(upload_path, database_path):
    ''' 
    Interface para o usuário ajustar as configurações da aplicação.

    Parameters:
        upload_path (str): Caminho da pasta onde os arquivos de áudio são armazenados.
    '''
    st.subheader('Instalar Modelos de Aprendizagem de Máquina')
    type_model =  select_model()

    if st.button('Instalar'):
        with st.spinner(f"Instalando modelo {type_model} ... 💫"):
            whisper.load_model(type_model)
            st.success(f"Modelo {type_model} instalado com sucesso!")
    


def remove_token_file(token, db_path):
    '''
    Remove o arquivo de banco de dados.

    Parameters:
        token (str): Token da transcrição.
        db_path (str): Caminho da pasta onde o banco de dados está.
    '''
    os.remove(os.path.join(db_path,token))

def remove_all_db_tokens(database_path):
    '''
    Remove todos os arquivos de banco de dados usados pela aplicação.

    Parameters:
        database_path (str): Caminho da pasta onde os arquivos de banco de dados estão armazenados.
    '''
     
    if os.listdir(database_path):
     
        temp_files = len(os.listdir(database_path))
        st.subheader('Casos Arquivados')
        st.write(f"Foram encontrados {temp_files} arquivos de casos arquivados." 
                 "Clique no botão abaixo se quiser removê-los.")
    
        if st.button('Remover todos os tokens arquivados'):
            with st.spinner(f"Removendo tokens arquivados ... 💫"):
                clean_folder(database_path)
                st.success(f"Todos os tokens foram removidos com sucesso!")

def remove_all_temp_files(upload_path, temporary_mp3_path):
    '''
    Remove todos os arquivos temporários usados pela aplicação.

    Parameters:
        upload_path (str): Caminho da pasta onde os arquivos temporários estão armazenados.
    '''

    if os.listdir(upload_path) or os.listdir(temporary_mp3_path):
       
        temp_files = len(os.listdir(upload_path)) + len(os.listdir(temporary_mp3_path))
        st.subheader('Arquivos Temporários')
        st.write(f"Foram encontrados {temp_files} arquivos temporários. Clique no botão abaixo para removê-los.")
        
        if st.button('Remover arquivos temporários'):
        
            with st.spinner(f"Removendo arquivos temporários ... 💫"):
        
                clean_folder(upload_path)
                clean_folder(temporary_mp3_path)
                st.success(f"Todos os arquivos temporários foram removidos com sucesso!")