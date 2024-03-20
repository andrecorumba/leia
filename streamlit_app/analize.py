import os
import streamlit as st
import pandas as pd
import sqlite3

# Import local modules
import audio_formats

def analize(token, database_folder_path, temporary_folder_path, original_folder_path):
    
    '''
    Consulta os casos cadastrados. 
    A função é chamada no arquivo app.py e apresenta na tela o resultado da consulta.
    
    Parameters:
        token (str): Token de acesso ao banco de dados.
        database_folder_path (str): Caminho para a pasta onde estão os bancos de dados.
        temporary_folder_path (str): Caminho para a pasta temporária.
        original_folder_path (str): Caminho para a pasta onde estão os arquivos originais.
        
    '''      
    if os.path.isfile(os.path.join(database_folder_path, token)):

        try:
            
            # Connect to database
            conn = sqlite3.connect(os.path.join(database_folder_path, token))
            query = f'SELECT * FROM transcripts'
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
            

            mp3_audio_file = audio_formats.to_mp3(file_selected, original_folder_path, temporary_folder_path)
            
            
            # Play audio
            audio_bytes = open(os.path.join(temporary_folder_path, mp3_audio_file), 'rb').read()
            st.audio(audio_bytes)


            # Close connection
            conn.close()

        except Exception as e:

            st.error("Erro ao acessar os dados.")    

    else:
            
            st.error("Não foi possível acessar o banco de dados. Verifique se o Token está correto e tente novamente.")       
    