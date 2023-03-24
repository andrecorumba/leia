import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# Import local modules
import about
import analize
import settings
import transcribe
import audio_formats
import database

def main(): 
    '''
    Versão Desktop. Função principal do app. Inicia o menu lateral e as páginas. Interface do usuário. 
    O menu lateral é criado com a função option_menu do pacote streamlit_option_menu.
    As páginas são chamadas a partir da opção selecionada no menu lateral.
    '''
    upload_path = "./uploads"
    db_path = './db/'
    table_name = 'db_transcripts'
        
    # Side Menu
    with st.sidebar:
        
        option = option_menu("Versão Desktop", 
                         options=["Sobre", 
                                  "Transcrever Pasta",
                                  "Áudio",
                                  "Vídeo",
                                  "Zip",
                                  "Analisar",
                                  "Configurações"],
                         # Icons from https://icons.getbootstrap.com/
                         icons=['house',
                                'folder',
                                'file-earmark-music-fill',
                                'file-play-fill',
                                'file-zip-fill',
                                'binoculars',
                                'wrench'],
                         menu_icon="display", default_index=0,
        )                       
    
    # Pages
    if option == 'Sobre':
        
        about.about()
    
    # Option Transcribe Folder
    elif option == 'Transcrever Pasta':
        
        st.subheader('Transcrever Pasta')
        case_name = st.text_input("Informe um nome para esse caso (ex.: caso1. Não use espaços ou caracteres especiais)")
        
        # Check if case name was informed
        if case_name:
       
            type_model = settings.select_model()
            folder = st.text_input('Informe o caminho da pasta (ex.: /home/audios/conversas)')
       
            # Check if folder was informed
            if folder:

                file_list = os.listdir(folder)
                if st.button('Transcrever'):
       
                    #df = transcribe_folder.transcribe_folder(folder, case_name, type_model)
                    #df = transcribe_file.transcribe_file_list(folder, case_name, type_model)
                    #df = pd.DataFrame(transcribe_folder.transcribe_folder(file_list, folder, type_model))
                    
                    # Transcribe files in a folder
                    df = pd.DataFrame(transcribe.transcribe(file_list, folder, type_model, 'folder'))
                    
                    # Write to database           
                    database.write_to_db(db_path, case_name, table_name, df)

                    # Delete temporary files
                    settings.clean_folder(upload_path)
 
    # Option Transcribe Files
    elif option == 'Áudio' or option == 'Vídeo':
        
        st.subheader('Transcrever Arquivos')
        case_name = st.text_input("Informe um nome para esse caso (ex.: caso1. Não use espaços ou caracteres especiais)")
        
        if case_name:
            
            type_model = settings.select_model()

            # Only audio and video files
            uploaded_file_list = st.file_uploader('Selecione os arquivos de áudio ou vídeo', 
                                             type=["opus","wav","mp3","ogg","wma",
                                                   "mp4", "m4a", "avi", "mov", "wmv"],
                                             accept_multiple_files=True)
        
            # Check if files were uploaded
            if uploaded_file_list is not None:
                
                for uploaded_file in uploaded_file_list:
                    
                    st.write(f"Arquivo selecionado: {uploaded_file.name}")
                
                    with open(os.path.join(upload_path, uploaded_file.name),"wb") as f:
                
                        f.write((uploaded_file).getbuffer())
                    
                    # Convert to mp3
                    mp3_audio_file = audio_formats.to_mp3(uploaded_file, upload_path)
                
                    # Play audio
                    audio_bytes = open(os.path.join(upload_path, mp3_audio_file), 'rb').read()
                    st.audio(audio_bytes)
            
                if st.button('Transcrever'):
                
                    with st.spinner(f"Transcrevendo Arquivos ... 💫"):
                
                        # Transcribe file list
                        df = pd.DataFrame(transcribe.transcribe(uploaded_file_list, upload_path, type_model, 'file_list'))
                        st.dataframe(df)

                        # Write to database           
                        database.write_to_db(db_path, case_name, table_name, df)

                        # Delete temporary files
                        settings.clean_folder(upload_path)

    # Option Zip
    elif option == 'Zip':
        
        st.subheader('Arquivos Zip')
        st.write('Em breve')

    # Option Analize           
    elif option == 'Analisar':
       
        st.subheader('Analisar')
        
        # List only files in folder
        case_list = [f for f in os.listdir(db_path) if not f.endswith('.py')]
        case_name = st.selectbox('Selecione o caso', case_list)

        # Check if case was selected
        if case_name:
        
            if st.button('Consultar'):
                
                analize.analize(db_path, table_name, case_name)
    
        else :
            
            st.error("Você não possui casos cadastrados.")

    # Option Settings
    elif option == 'Configurações':
       
        st.subheader('Configurações')
        settings.adjust_settings(upload_path, db_path)
   
if __name__ == '__main__':
    main()
