import sqlite3
import os
import pandas as pd
import streamlit as st

def write_to_db(db_path, case_name, table_name, df):
    
    '''
    Recebe o nome do arquivo e o texto transcrito e salva no banco de dados.

    Parameters:
        db_path (str): Caminho da pasta onde o banco de dados está.
        file_name (str): Nome do arquivo de áudio ou vídeo.
        df (DataFrame): Dataframe com o nome do arquivo e o texto transcrito.

    Returns:
        None
    '''
    
    # Create connection
    conn = sqlite3.connect(os.path.join(db_path, case_name))

    try:        
        df.to_sql(table_name, con=conn, if_exists='append', index=False)
        st.success(f"Trancrição Gravada no Banco de Dados. Acesse o menu Analisar para consultar.")

    except Exception as e:
        st.error(f"Algo deu errado. Não foi possível gravar no banco de dados.")
        st.error(e)
    
    conn.close()