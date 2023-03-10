import os
import whisper
import pandas as pd
import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu
from pydub import AudioSegment

upload_path = "/Users/andreluiz/projetos/leia/uploads"
download_path = "/Users/andreluiz/projetos/leia/downloads"

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

    conn = sqlite3.connect(f'/Users/andreluiz/projetos/leia/db/{table_name}.db')

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

def transcribe_file(uploaded_file, folder, type_model):
    model = whisper.load_model(type_model)
    try:
        st.warning(f"Transcrevendo {uploaded_file}")         
        result =  model.transcribe(os.path.join(folder,uploaded_file))
        st.success(f"Arquivo Transcrito: {uploaded_file}")
        #st.write(result['text'])
    except Exception as e:
        st.error(f"Algo deu errado")
        st.error(e)
    
    return result['text']

def analize():
    case_list = os.listdir('/Users/andreluiz/projetos/leia/db/')

    case_name = st.selectbox('Selecione o caso', case_list)

    if case_name:
        if st.button('Consultar'):
            try:
                conn = sqlite3.connect(f'/Users/andreluiz/projetos/leia/db/{case_name}')
                table_name = case_name.replace('.db', '')
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

def about():
    st.subheader('Selecione uma opção no menu lateral.')
    st.text('''
    O Programa LEIA é um software de transcrição de áudio e vídeo.
    Você pode transcrever novos arquivos ou consultar casos já transcritos.
    Documentação em: https://github.com/andrecorumba/leia
    ''')

def select_model():   
    type_model = st.select_slider('Selecione o modelo: Quanto maior, mais preciso, porém mais lento na hora de transcrever', ['tiny','base', 'small', 'medium','large'], )
    return type_model

def adjust_settings():
    st.subheader('Instalar Modelos')
    type_model =  select_model()
    if st.button('Instalar'):
        with st.spinner(f"Instalando modelo {type_model} ... 💫"):
            whisper.load_model(type_model)
            st.success(f"Modelo {type_model} instalado com sucesso!")
    
    if os.listdir(upload_path) or os.listdir(download_path):
        temp_files = len(os.listdir(upload_path)) + len(os.listdir(download_path))
        st.subheader('Arquivos Temporários')
        st.write(f"Foram encontrados {temp_files} arquivos temporários. Clique no botão abaixo para removê-los.")
        if st.button('Remover arquivos temporários'):
            with st.spinner(f"Removendo arquivos temporários ... 💫"):
                clean_folder(upload_path)
                clean_folder(download_path)
                st.success(f"Todos os arquivos temporários foram removidos com sucesso!")
        
def to_mp3(audio_file, output_audio_file, upload_path, download_path):
    audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name))
    output_file_path = os.path.join(download_path,os.path.splitext(output_audio_file)[0] + ".mp3")
    audio_data.export(output_file_path, format="mp3")

    return output_audio_file

def clean_folder(folder_path):
    with st.spinner(f"Removendo arquivos temporários..."):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                st.error(f"Erro ao remover {file_path} devido a {e}")

import zipfile
import sqlite3
import os

def find_opus_files(zip_file_path, db_file_path):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS opus_files (name TEXT, path TEXT, binary BLOB)")

    with zipfile.ZipFile(zip_file_path) as zip_file:
        # percorre todas as entradas do arquivo zip
        for entry in zip_file.infolist():
            # verifica se é um arquivo com a extensão .opus
            if entry.filename.endswith('.opus'):
                # obtém o conteúdo do arquivo
                binary = zip_file.read(entry)

                # insere as informações no banco de dados
                cursor.execute("INSERT INTO opus_files (name, path, binary) VALUES (?, ?, ?)", (entry.filename, os.path.dirname(entry.filename), binary))

    conn.commit()
    conn.close()


def main():   
    st.title('LEIA - Trascrição de áudio e vídeos')
    with st.sidebar:
        option = option_menu("Selecione", 
                         options=["Sobre", 
                                  "Transcrever Pasta",
                                  "Transcrever Arquivo",
                                  "Arquivos Cellebrite",
                                  "Analisar",
                                  "Configurações"],
                         icons=['house',
                                'body-text',
                                'file-play-fill',
                                'phone',
                                'binoculars',
                                'wrench'],
                         menu_icon="app-indicator", default_index=0,
        )                           
    if option == 'Sobre':
        about()

    elif option == 'Transcrever Pasta':
        st.subheader('Transcrever Pasta')
        case_name = st.text_input("Informe um nome para esse caso (ex.: caso1. Não use espaços ou caracteres especiais)")
        if case_name:
            type_model = select_model()
            folder = st.text_input('Informe o caminho da pasta (ex.: /home/audios/conversas)')
            if folder:
                if st.button('Transcrever'):
                    df = transcribe_folder(folder, case_name, type_model)
 
    elif option == 'Arquivos Cellebrite':
        ...
 
    elif option == 'Transcrever Arquivo':
        file_transcribe = ''
        st.subheader('Transcrever Arquivos')
        type_model = select_model()
        uploaded_file = st.file_uploader('Selecione o arquivo de áudio ou vídeo', 
                                     type=["opus","wav","mp3","ogg","wma","aac","flac",
                                           "mp4","flv", "m4a", "avi", "mov", "wmv", "mkv", "webm"])
        
        if uploaded_file is not None:
            with open(os.path.join(upload_path,uploaded_file.name),"wb") as f:
                f.write((uploaded_file).getbuffer())
            
            output_audio_file = uploaded_file.name.split('.')[0] + '.mp3'
            output_audio_file = to_mp3(uploaded_file, output_audio_file, upload_path, download_path)

            audio_file = open(os.path.join(download_path,output_audio_file), 'rb')
            audio_bytes = audio_file.read()

            st.audio(audio_bytes)
            
            if st.button('Transcrever'):
                with st.spinner(f"Processando Audio ... 💫"):
                    file_transcribe = transcribe_file(output_audio_file, download_path, type_model)
                    st.write(file_transcribe)
                    st.download_button(label="Baixar Transcrição", 
                                       data=file_transcribe,
                                       file_name=f'{uploaded_file.name}.txt', 
                                       mime='text/plain')
            
    elif option == 'Analisar':
        st.subheader('Analisar')
        analize()
    
    elif option == 'Configurações':
        st.subheader('Configurações')
        adjust_settings()

    
if __name__ == '__main__':
    main()
