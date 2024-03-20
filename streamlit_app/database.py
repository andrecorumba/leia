import sqlite3
import os
import pandas as pd
import streamlit as st

# Create database
def write_to_db(database_folder_path, token, df):
    
    '''
    Recebe o nome do arquivo e o texto transcrito e salva no banco de dados.

    Parameters:
        database_folder_path (str): Caminho da pasta onde o banco de dados está.
        token (str): Nome do caso.
        df (pandas.DataFrame): Dataframe com os dados a serem salvos.
    '''
    table_name = 'transcripts'
    # Create connection
    conn = sqlite3.connect(os.path.join(database_folder_path, token))

    try:        
        df.to_sql(table_name, con=conn, if_exists='replace', index=False)
        st.success(f"Trancrição Gravada no Banco de Dados.")

    except Exception as e:
        st.error(f"Algo deu errado. Não foi possível gravar no banco de dados.")
        st.error(e)
    
    conn.close()