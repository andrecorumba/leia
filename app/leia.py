# Script para transcrição de áudios e videos, usando biblioteca Openai-Whisper

import os
import whisper
import pandas as pd

import sqlite3

import streamlit as st


def transcreve_pasta(pasta, tabela, modelo):
    # Carrega o modelo 'base'. Para carregar outros modelos mais precisos substitua por 'small' ou 'large'
    # O tempo de execução será maior a depender do modelo
    # Mais info: https://github.com/openai/whisper
    model = whisper.load_model(modelo)
    
    arquivos_opus = []

    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".opus"):
            arquivos_opus.append(arquivo)

    quantidade = len(arquivos_opus)

    st.write(f"Encontrados {quantidade} arquivos .opus na pasta.")

    for nome_arquivo in arquivos_opus:
        try:
            st.warning(f"Transcrevendo {nome_arquivo}")
            
            result =  model.transcribe(os.path.join(pasta,nome_arquivo))
            
            dic_transcricao = {'arquivo'     : [nome_arquivo],
                               'transcricao' : [result['text']]}
            
            df = pd.DataFrame(dic_transcricao)

            # estabelece conexão com o banco de dados SQLite
            conn = sqlite3.connect('../banco-de-dados/leia.db')

            # escreve o DataFrame na tabela SQLite usando o método to_sql()
            df.to_sql(tabela, con=conn, if_exists='append', index=False)

            # fecha a conexão com o banco de dados
            conn.close()

            st.success(f"Arquivo Transcrito: {nome_arquivo}")

        except Exception as e:
            st.error(f"Algo deu errado")

@st.cache_data
def exporta_csv(tabela):
    # estabelece conexão com o banco de dados SQLite
    conn = sqlite3.connect('../banco-de-dados/leia.db')

    query = f'SELECT * FROM {tabela}'

    df = pd.read_sql(query, conn)

    arquivo_csv = f'../saidas/{tabela}.csv'

    return df.to_csv(sep=';', encoding='utf-8', index=False)


def leia_arquivo(nome_arquivo, bytes_data, modelo, tabela):
    model = whisper.load_model(modelo)
     
    result =  model.transcribe(bytes_data)
            
    dic_transcricao = {'arquivo'     : [nome_arquivo],
                       'transcricao' : [result['text']]}
            
    df = pd.DataFrame(dic_transcricao)

    # estabelece conexão com o banco de dados SQLite
    conn = sqlite3.connect('../banco-de-dados/leia.db')

    # escreve o DataFrame na tabela SQLite usando o método to_sql()
    df.to_sql(name=tabela, con=conn, if_exists='append', index=False)

    # fecha a conexão com o banco de dados
    conn.close()

    st.success("Dados transcritos com sucesso!")
    

def main():
    pasta = '/Users/andreluiz/projetos/leia/entradas/audios'
    modelo = 'base'

    st.title('LEIA - Trascrição de áudio e vídeos')

    tabela = st.text_input("Nome para esses itens (ex.: caso1. Não use espaços ou caracteres especiais)")

    tipo = st.radio("Escolha a forma de transcrição", ('Pasta', 'Arquivo'))

    if tipo == 'Pasta':
        pasta = st.text_input('Informe o caminho da pasta (ex.: /home/audios/conversas)')

        if st.button('Transcrever'):
            transcreve_pasta(pasta, tabela, modelo)
            arquivo_csv = exporta_csv(tabela)
            st.download_button(label="Baixar CSV", data=arquivo_csv, file_name=f'{tabela}.csv', mime='text/csv')
    else:
        uploaded_files = st.file_uploader("Faça upload dos seus áudios aqui", type=["opus"], accept_multiple_files=True)
        #st.write(uploaded_files.name)

if __name__ == '__main__':
    main()
