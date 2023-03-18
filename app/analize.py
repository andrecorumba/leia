import os
import streamlit as st
import pandas as pd
import sqlite3

def analize(db_path, table_name):
    
    '''
    Consulta os casos cadastrados. 
    A função é chamada no arquivo app.py e apresenta na tela o resultado da consulta.
    
    Parameters:
        None

    Returns:
       (None): None
    '''

    case_list = os.listdir(db_path)

    case_name = st.selectbox('Selecione o caso', case_list)

    if case_name:
        
        if st.button('Consultar'):
        
            try:
        
                conn = sqlite3.connect(os.path.join(db_path, case_name))
                query = f'SELECT * FROM {table_name}'
                df = pd.read_sql(query, conn)
                st.dataframe(df) 
                st.download_button(label="Baixar CSV", 
                                   data=df.to_csv(sep=';', encoding='utf-8', index=False),
                                   file_name=f'{case_name}.csv', 
                                   mime='text/csv')
        
            except Exception as e:
        
                st.error(e)           
    else :
        
        st.error("Você não possui casos cadastrados.")