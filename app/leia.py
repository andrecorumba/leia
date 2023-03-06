import os
import whisper
import pandas as pd
import sqlite3
import streamlit as st


def transcribe_folder(folder, table_name, type_model):
    model = whisper.load_model(type_model)
    opus_files = []
    df_export = pd.DataFrame({  'arquivo'     : [],
                                'transcricao' : []})

    for file in os.listdir(folder):
        if file.endswith(".opus"):
            opus_files.append(file)
    
    quantity = len(opus_files)
    st.write(f"Encontrados {quantity} arquivos .opus na pasta.")

    for file_name in opus_files:
        try:
            st.warning(f"Transcrevendo {file_name}")         
            result =  model.transcribe(os.path.join(folder,file_name))
            dic_transcribe= {'arquivo'     : [file_name],
                             'transcricao' : [result['text']]}
            df = pd.DataFrame(dic_transcribe)

            conn = sqlite3.connect('../banco-de-dados/leia.db')
            df.to_sql(table_name, con=conn, if_exists='append', index=False)
            conn.close()

            df_export = pd.concat([df_export, df])
            st.success(f"Arquivo Transcrito: {file_name}")

        except Exception as e:
            st.error(f"Algo deu errado")
            st.error(e)
    
    return df_export

@st.cache_data
def csv_export(table_name):
    conn = sqlite3.connect('../banco-de-dados/leia.db')
    query = f'SELECT * FROM {table_name}'
    df = pd.read_sql(query, conn)
    return df.to_csv(sep=';', encoding='utf-8', index=False)


def leia_arquivo(nome_arquivo, bytes_data, modelo, tabela):
    model = whisper.load_model(modelo)     
    result =  model.transcribe(bytes_data)
    dic_transcricao = {'arquivo'     : [nome_arquivo],
                       'transcricao' : [result['text']]}
    df = pd.DataFrame(dic_transcricao)
    conn = sqlite3.connect('../banco-de-dados/leia.db')
    df.to_sql(name=tabela, con=conn, if_exists='append', index=False)
    conn.close()
    st.success("Dados transcritos com sucesso!")
    

def main():   
    type_model = 'base'  # Use 'small' or 'large' for more accurate models
    st.title('LEIA - Trascrição de áudio e vídeos')
    table_name = st.text_input("Nome para esses itens (ex.: caso1. Não use espaços ou caracteres especiais)")
    type_input = st.radio("Escolha a forma de transcrição", ('Pasta', 'Arquivo'))

    if type_input == 'Pasta':
        folder = st.text_input('Informe o caminho da pasta (ex.: /home/audios/conversas)')

        if st.button('Transcrever'):
            df = transcribe_folder(folder, table_name, type_model)
            csv_file = csv_export(table_name)
            st.dataframe(df)
            st.download_button(label="Baixar CSV", 
                               data=csv_file, 
                               file_name=f'{table_name}.csv', 
                               mime='text/csv')
    else:
        uploaded_files = st.file_uploader("Faça upload dos seus arquivos aqui", 
                                          type=["opus"], 
                                          accept_multiple_files=True)
        if uploaded_files is not None:
            for file in uploaded_files:
                st.write(f"Transcrevendo {file.name}")
                leia_arquivo(file.name, file.getvalue(), type_model, table_name)
                st.write("Pronto!")

if __name__ == '__main__':
    main()
