import sqlite3
import os
import pandas as pd
import streamlit as st

def write_to_db(db_path, case_name, table_name, df):
    
    '''
    Recebe o nome do arquivo e o texto transcrito e salva no banco de dados.

    Parameters:
        db_path (str): Caminho da pasta onde o banco de dados está.
        case_name (str): Nome do caso.
        table_name (str): Nome da tabela.
        df (pandas.DataFrame): Dataframe com os dados a serem salvos.
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