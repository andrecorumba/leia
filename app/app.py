import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# Import local modules
import about
import analize
import settings
import transcribe_folder
import transcribe_file

def main(): 
    upload_path = "/Users/andreluiz/projetos/leia/uploads"
    download_path = "/Users/andreluiz/projetos/leia/downloads"  
        
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
        about.about()

    elif option == 'Transcrever Pasta':
        st.subheader('Transcrever Pasta')
        case_name = st.text_input("Informe um nome para esse caso (ex.: caso1. Não use espaços ou caracteres especiais)")
        if case_name:
            type_model = settings.select_model()
            folder = st.text_input('Informe o caminho da pasta (ex.: /home/audios/conversas)')
            if folder:
                if st.button('Transcrever'):
                    df = transcribe_folder.transcribe_folder(folder, case_name, type_model)
 
    elif option == 'Arquivos Cellebrite':
        ...
 
    elif option == 'Transcrever Arquivo':
        file_transcribe = ''
        st.subheader('Transcrever Arquivos')
        type_model = settings.select_model()
        uploaded_file = st.file_uploader('Selecione o arquivo de áudio ou vídeo', 
                                     type=["opus","wav","mp3","ogg","wma","aac","flac",
                                           "mp4","flv", "m4a", "avi", "mov", "wmv", "mkv", "webm"])
        
        if uploaded_file is not None:
            with open(os.path.join(upload_path,uploaded_file.name),"wb") as f:
                f.write((uploaded_file).getbuffer())
            
            output_audio_file = uploaded_file.name.split('.')[0] + '.mp3'
            output_audio_file = transcribe_file.to_mp3(uploaded_file, output_audio_file, upload_path, download_path)

            audio_file = open(os.path.join(download_path,output_audio_file), 'rb')
            audio_bytes = audio_file.read()

            st.audio(audio_bytes)
            
            if st.button('Transcrever'):
                with st.spinner(f"Processando Audio ... 💫"):
                    file_transcribe = transcribe_file.transcribe_file(output_audio_file, download_path, type_model)
                    st.write(file_transcribe)
                    st.download_button(label="Baixar Transcrição", 
                                       data=file_transcribe,
                                       file_name=f'{uploaded_file.name}.txt', 
                                       mime='text/plain')
            
    elif option == 'Analisar':
        st.subheader('Analisar')
        analize.analize()
    
    elif option == 'Configurações':
        st.subheader('Configurações')
        settings.adjust_settings(upload_path, download_path)

    
if __name__ == '__main__':
    main()
