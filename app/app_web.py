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
import token_leia

def main(): 
    '''
    Versão Web. Possui menos funcionalidade do que a versão principal. Main é a função principal do app. Inicia o menu lateral e as páginas. Interface do usuário. 
    O menu lateral é criado com a função option_menu do pacote streamlit_option_menu.
    As páginas são chamadas a partir da opção selecionada no menu lateral.
    '''
    upload_path = "./uploads"
    db_path = './db/'
    table_name = 'db_transcripts'
        
    # Side Menu
    with st.sidebar:
        
        option = option_menu("Versão Web", 
                         options=["Sobre", 
                                  "Transcrever Arquivos",
                                  "Analisar",
                                  "Configurações"],
                         icons=['house',
                                'file-play-fill',
                                'binoculars',
                                'wrench'],
                         menu_icon="display", default_index=0,
        )                       
    
    # Pages
    if option == 'Sobre':
        
        about.about()
    
    
    # Option Transcribe Files
    elif option == 'Transcrever Arquivos':
        
        st.subheader('Transcrever Arquivos')
        #case_name = st.text_input("Informe um nome para esse caso (ex.: caso1. Não use espaços ou caracteres especiais)")
        case_name = token_leia.get_token_leia()

        if case_name:
            
            type_model = settings.select_model()

            # Only audio and video files
            uploaded_file_list = st.file_uploader('Selecione os arquivos de áudio ou vídeo', 
                                             type=["opus","wav","mp3","ogg","wma","aac","flac",
                                                   "mp4","flv", "m4a", "avi", "mov", "wmv", "mkv", "webm"],
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

                        # Print Token
                        st.success(f"Copie e GUARDE o Token a Seguir. Você precisará dele para acessar as transcrições")
                        st.code(case_name)

                        # Delete temporary files
                        settings.clean_folder(upload_path)

    # Option Analize           
    elif option == 'Analisar':
       
        st.subheader('Analisar')

        case_name = st.text_input("Informe o Token do caso que deseja analisar")
        
        # Check if token exists
        if case_name:
                
                analize.analize(db_path, table_name, case_name)
    
    # Option Settings
    elif option == 'Configurações':
       
        st.subheader('Configurações')
        settings.adjust_settings(upload_path, db_path)
   
if __name__ == '__main__':
    main()
