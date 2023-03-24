import os
import streamlit as st
import pandas as pd
import sqlite3

# Import local modules
from audio_formats import to_mp3

def analize(db_path, table_name, token):
    
    '''
    Consulta os casos cadastrados. 
    A função é chamada no arquivo app.py e apresenta na tela o resultado da consulta.
    
    Parameters:
        db_path (str): Caminho para o banco de dados
        table_name (str): Nome da tabela
        case_name (str): Nome do caso
    '''      
    if os.path.isfile(os.path.join(db_path, token)):

        try:
            
            # Connect to database
            conn = sqlite3.connect(os.path.join(db_path, token))
            query = f'SELECT * FROM {table_name}'
            df = pd.read_sql(query, conn)
            
            # Show dataframe
            st.dataframe(df) 
            
            # Download dataframe
            st.download_button(label="Baixar CSV", 
                                data=df.to_csv(sep=';', encoding='utf-8', index=False),
                                file_name=f'LeIA_{token}.csv', 
                                mime='text/csv')
            
            # Play audio
            file_selected = st.selectbox("Selecione o arquivo para ouvir o áudio", df['arquivo'])
            
            temporary_mp3_path = '/Users/andreluiz/projetos/leia/uploads/temporary_mp3'
            token_folder = '/Users/andreluiz/projetos/leia/uploads/token_files'


            mp3_audio_file = to_mp3(file_selected, token_folder, temporary_mp3_path)
            
            
            # Play audio
            audio_bytes = open(os.path.join(temporary_mp3_path, mp3_audio_file), 'rb').read()
            st.audio(audio_bytes)


            # Close connection
            conn.close()

        except Exception as e:

            st.error("Erro ao acessar os dados.")    

    else:
            
            st.error("Não foi possível acessar o banco de dados. Verifique se o Token está correto e tente novamente.")       
    