import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from pydub import AudioSegment
import io

# Import local modules
import about
import analize
import settings
import transcribe
import audio_formats
import database
import token_leia
import extract_zip

def main(): 
    '''
    Versão Web. Main é a função principal do app. Inicia o menu lateral e as páginas. Interface do usuário. 
    O menu lateral é criado com a função option_menu do pacote streamlit_option_menu.
    As páginas são chamadas a partir da opção selecionada no menu lateral.
    '''
    upload_path = "uploads/token_files/"
    temporary_mp3_path = "uploads/temporary_mp3/"
    db_path = 'db'
    table_name = 'db_transcripts'
        
    # Side Menu
    with st.sidebar:
        
        option = option_menu("Versão Web", 
                         options=["Sobre", 
                                  "Áudio",
                                  "Vídeo",
                                  "Zip",
                                  "Analisar",
                                  "Configurações"],
                         
                         # Icons from https://icons.getbootstrap.com/
                         icons=['house',
                                'file-earmark-music-fill',
                                'file-play-fill',
                                'file-zip-fill',
                                'binoculars',
                                'wrench'],
                         menu_icon="cloud", default_index=0,
        )   
    
    # Pages
    if option == 'Sobre':
        
        about.about()
    
    
    # Option Transcribe Files
    elif option == "Áudio" or option == "Vídeo":
        
        st.subheader('Transcrever Arquivos')
    
        case_name = token_leia.get_token_leia()

        if case_name:
            
            type_model = settings.select_model()

            # Only audio files
            if option == "Áudio":
                
                uploaded_file_list = st.file_uploader('Selecione os arquivos de áudio', 
                                                     type=["opus","wav","mp3","ogg","wma"],
                                                     accept_multiple_files=True)
            # Only video files
            elif option == "Vídeo":
                    
                uploaded_file_list = st.file_uploader('Selecione os arquivos de vídeo', 
                                                      type=["mp4", "m4a", "avi", "mov", "wmv"],
                                                      accept_multiple_files=True)
        
            # Check if files were uploaded
            if uploaded_file_list is not None:
            
                if st.button('Transcrever'):

                    for file in uploaded_file_list:
                        # Save all files with original name
                        with open(os.path.join(upload_path, file.name),"wb") as f:
                            f.write((file).getbuffer())
                        
                    # Transcribe folder
                    with st.spinner(f"Transcrevendo Arquivos ... 💫"):
                
                        # Transcribe file list
                        df = pd.DataFrame(transcribe.transcribe(upload_path, type_model))
                        st.dataframe(df)

                        # Write to database           
                        database.write_to_db(db_path, case_name, table_name, df)

                        # Print Token
                        st.title("IMPORTANTE ⚠️")
                        st.subheader(f"Copie e GUARDE o Token a Seguir. ") 
                        st.text("Você precisará dele para acessar as transcrições.")
                        st.code(case_name)
                        st.markdown("O Token é um código único que identifica essa trasncrição." 
                                "Ele é gerado automaticamente e é único para cada conjunto de transcrições." 
                                "NÃO O PERCA! Sem o Token, não será possível acessar essas transcrições." 
                                "Os arquivos de áudio e vídeo não são salvos no banco de dados."
                                "As transcrições ficam salvas no banco de dados por 30 dias."
                                "Após esse período, os dados são apagados."
                                "Você pode acessar as transcrições a qualquer momento, basta inserir o Token no menu Analisar."
                                "Você poderá apagar as transcrições a qualquer momento no menu Configurações."
                                "Acesse o menu Analisar ao lado e insira o token.")

                        # Delete temporary files
                        #settings.clean_folder(upload_path)

    elif option == "Zip":
        
        st.header('Transcrever Arquivo Zip')

        case_name = token_leia.get_token_leia()

        if case_name:
            
            type_model = settings.select_model()

            # Only audio and video files
            zip_file_name = st.file_uploader('Selecione os arquivos de áudio ou vídeo', 
                                             type=["zip", "ufed"],
                                             accept_multiple_files=False)
        
            # Check if files were uploaded
            if zip_file_name is not None:
                    
                with open(os.path.join(upload_path, zip_file_name.name),"wb") as f:
                   
                    f.write((zip_file_name).getbuffer())
                
                try:
                   
                    zip_file_list = extract_zip.extract_media_files(zip_file_name, upload_path)
                    st.success(f"Arquivos extraídos com sucesso!")
                    st.write(zip_file_list)

                except Exception as e:
                   
                    st.error("Erro ao extrair arquivos!")
                    st.error(e)
            
                if st.button('Transcrever'):
                
                    with st.spinner(f"Transcrevendo Arquivos ... 💫"):
                
                        # Transcribe file list
                        df = pd.DataFrame(transcribe.transcribe(upload_path, type_model))
                        st.dataframe(df)

                        # Write to database           
                        database.write_to_db(db_path, case_name, table_name, df)

                        # Print Token
                        st.title("IMPORTANTE ⚠️")
                        st.subheader(f"Copie e GUARDE o Token a Seguir. ") 
                        st.text("Você precisará dele para acessar as transcrições.")
                        st.code(case_name)
                        st.write("O Token é um código único que identifica essa trasncrição." 
                                "Ele é gerado automaticamente e é único para cada conjunto de transcrições." 
                                "Não o perca! Sem o Token, não será possível acessar essas transcrições." 
                                "Os arquivos de áudio e vídeo não são salvos no banco de dados."
                                "As transcrições ficam salvas no banco de dados por 30 dias."
                                "Após esse período, os dados são apagados."
                                "Você pode acessar as transcrições a qualquer momento, basta inserir o Token no menu Analisar."
                                "Você poderá apagar as transcrições a qualquer momento no menu Configurações."
                                "Acesse o menu Analisar ao lado e insira o token.")

                        # Delete temporary files
                        #settings.clean_folder(upload_path)
    
    # Option Analize          
    elif option == 'Analisar':
       
        st.subheader('Analisar')

        case_name = st.text_input("Informe o Token do caso que deseja analisar")
        
        # Check if token exists
        if case_name:
                
                analize.analize(db_path, table_name, case_name)
    
    # Option Settings
    elif option == 'Configurações':
       
        st.header('Configurações')
        st.subheader("Remove Transcrições")
        token = st.text_input("Informe o Token das trancrições que deseja remover")
        
        # Check if token exists
        if token:

            try:
                
                settings.remove_token_file(token, db_path)
                st.success("Transcrições removidas com sucesso!")
            
            except:
            
                st.error("Token não encontrado. Verifique se o token está correto.")
        
        # Options Remove All. DON'T USE IN PRODUCTION
        settings.remove_all_db_tokens(db_path)
        settings.remove_all_temp_files(upload_path, temporary_mp3_path)
   
if __name__ == '__main__':
    main()
