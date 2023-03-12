import whisper
import os
import pandas as pd
import sqlite3
import streamlit as st


def transcribe_folder(folder, case_name, type_model):
    model = whisper.load_model(type_model)
    file_list = []
    table_name = f'{case_name}_{type_model}'
    df_export = pd.DataFrame({  'arquivo'     : [],
                                'transcricao' : []})

    for file in os.listdir(folder):
        if file.endswith(".opus"):
            file_list.append(file)
    
    quantity = len(file_list)
    st.write(f"Encontrados {quantity} arquivos de áudio na pasta.")

    conn = sqlite3.connect(f'../db/{table_name}.db')

    for file_name in file_list:
        try:
            st.warning(f"Transcrevendo {file_name}")         
            result =  model.transcribe(os.path.join(folder,file_name))
            dic_transcribe= {'arquivo'     : [file_name],
                             'transcricao' : [result['text']]}
            df = pd.DataFrame(dic_transcribe)
            
            df.to_sql(table_name, con=conn, if_exists='append', index=False)

            df_export = pd.concat([df_export, df])
            #st.success(f"Arquivo Transcrito: {file_name}")

        except Exception as e:
            st.error(f"Algo deu errado")
            st.error(e)
    
    conn.close()

    st.success(f"{quantity} Áudios Transcritos! Acesse o menu Analisar para consultar.")
    
    return df_export