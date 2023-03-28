import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from pydub import AudioSegment

# Import local modules
import about
import analize
import settings
import transcribe
import database
import token_leia
import extract_zip
import folders

def main(): 
    '''
    App Versão Docker. Inicia o menu lateral e as páginas. Interface do usuário. 
    O menu lateral é criado com a função option_menu do pacote streamlit_option_menu.
    As páginas são chamadas a partir da opção selecionada no menu lateral.
    '''

    main_folder_path = "etc"
        
    # Side Menu
    with st.sidebar:   
        option = option_menu("Versão Docker v.1.0.0", 
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
    elif option == "Áudio" or option == "Vídeo" or option == "Zip":  
        st.subheader('Transcrever Arquivos')   
        type_model = settings.select_model('docker')

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
    
        # Only zip files
        elif option == "Zip":
            uploaded_file_list = st.file_uploader('Selecione os arquivos de áudio ou vídeo', 
                                            type=["zip", "ufed"],
                                            accept_multiple_files=False)
       
        # Check if files were uploaded
        if uploaded_file_list is not None:
            if st.button('Transcrever'):
                # Create token
                token = token_leia.get_token_leia()

                # Crate token folders
                token_folder_path, database_folder_path, temporary_folder_path, original_folder_path = folders.create_folders(token, main_folder_path)
                
                if option == "Zip":     
                    with open(os.path.join(temporary_folder_path, 
                                           uploaded_file_list.name), "wb") as f:
                    
                        f.write((uploaded_file_list).getbuffer())

                    zip_file_list = extract_zip.extract_media_files(os.path.join(temporary_folder_path, 
                                                                                 uploaded_file_list.name), 
                                                                                 original_folder_path)
                    
                    #st.write(zip_file_list)
                
                else:
                    for file in uploaded_file_list:
                        # Save all files with original name
                        with open(os.path.join(original_folder_path, file.name),"wb") as f:
                            f.write((file).getbuffer())

                # Transcribe folder
                with st.spinner(f"Transcrevendo Arquivos ... 💫"):
                    # Transcribe file list
                    df = pd.DataFrame(transcribe.transcribe(original_folder_path, type_model))
                    st.dataframe(df)

                    # Write to database           
                    database.write_to_db(database_folder_path, token, df)

                    # Print Token
                    st.title("IMPORTANTE ⚠️")
                    st.subheader(f"Copie e GUARDE o Token a Seguir. ") 
                    st.text("Você precisará dele para acessar as transcrições.")
                    st.code(token)
                    st.markdown("O Token é um código único que identifica essa trasncrição." 
                            "Ele é gerado automaticamente e é único para cada conjunto de transcrições." 
                            "NÃO O PERCA! Sem o Token, não será possível acessar essas transcrições." 
                            "Os arquivos de áudio e vídeo não são salvos no banco de dados."
                            "As transcrições ficam salvas no banco de dados por 30 dias."
                            "Após esse período, os dados são apagados."
                            "Você pode acessar as transcrições a qualquer momento, basta inserir o Token no menu Analisar."
                            "Você poderá apagar as transcrições a qualquer momento no menu Configurações."
                            "Acesse o menu Analisar ao lado e insira o token.")
              
    # Option Analize          
    elif option == 'Analisar':
        st.subheader('Analisar')
        token = st.text_input("Informe o Token do caso que deseja analisar")
        
        # Check if token exists
        if token:
            token_folder_path, database_folder_path, temporary_folder_path, original_folder_path = folders.get_folders(token, main_folder_path)
            analize.analize(token, database_folder_path, temporary_folder_path, original_folder_path)
    
    # Option Settings
    elif option == 'Configurações':
       
        st.header('Configurações')
        
        st.subheader("Remove Tokens")
        token = st.text_input("Informe o Token das trancrições que deseja remover")

        # Check if token exists
        if token:    
            # Check if like secrete token
            if token == settings.read_secret_token('secret-token.txt'):
                settings.install_models('docker')
                
                if os.path.exists(main_folder_path):
                    if st.button('Remover Todos os Tokens'):
                        settings.remove_token(main_folder_path)
            
            else:
                try:
                    token_folder_path, database_folder_path, temporary_folder_path, original_folder_path = folders.get_folders(token, main_folder_path)
                    settings.remove_token(token_folder_path)
                    st.success("Transcrições removidas com sucesso!")
                
                except:
                    st.error("Token não encontrado. Verifique se o token está correto.")
   
if __name__ == '__main__':
    main()
