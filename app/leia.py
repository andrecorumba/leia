import os
import whisper
import pandas as pd
import sqlite3
import streamlit as st


def transcribe_folder(folder, case_name, type_model):
    model = whisper.load_model(type_model)
    opus_files = []
    df_export = pd.DataFrame({  'arquivo'     : [],
                                'transcricao' : []})

    for file in os.listdir(folder):
        if file.endswith(".opus"):
            opus_files.append(file)
    
    quantity = len(opus_files)
    st.write(f"Encontrados {quantity} arquivos .opus na pasta.")

    conn = sqlite3.connect(f'/Users/andreluiz/projetos/leia/banco-de-dados/{case_name}.db')

    for file_name in opus_files:
        try:
            st.warning(f"Transcrevendo {file_name}")         
            result =  model.transcribe(os.path.join(folder,file_name))
            dic_transcribe= {'arquivo'     : [file_name],
                             'transcricao' : [result['text']]}
            df = pd.DataFrame(dic_transcribe)
            
            df.to_sql(case_name, con=conn, if_exists='append', index=False)

            df_export = pd.concat([df_export, df])
            st.success(f"Arquivo Transcrito: {file_name}")

        except Exception as e:
            st.error(f"Algo deu errado")
            st.error(e)
    
    conn.close()

    st.success(f"Áudios Trancritos: {quantity}")
    
    return df_export
   
def consult():
    case_list = os.listdir('/Users/andreluiz/projetos/leia/banco-de-dados/')

    case_name = st.selectbox('Selecione o caso', case_list)

    if case_name:
        if st.button('Consultar'):
            try:
                conn = sqlite3.connect(f'/Users/andreluiz/projetos/leia/banco-de-dados/{case_name}')
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

def select():
    st.subheader('Selecione uma opção no menu lateral.')
    st.text('''
    O Programa LEIA é um software de transcrição de áudio e vídeo.
    Você pode transcrever novos arquivos ou consultar casos já transcritos.
    Documentação em: https://github.com/andrecorumba/leia
    ''')

def main():   
    
    st.title('LEIA - Trascrição de áudio e vídeos')

    bar = st.sidebar

    option = bar.selectbox('O que você deseja fazer?',
                          ('Selecione','Transcrever Novos', 'Consultar'))
    
    if option == 'Selecione':
        select()
    elif option == 'Transcrever Novos':
        type_model = 'base'  # Whisper Model. Use 'small' or 'large' for more accurate models
        st.subheader('Transcrever novos arquivos')
        case_name = st.text_input("Informe um nome para esse caso (ex.: caso1. Não use espaços ou caracteres especiais)")
        type_input = st.radio("Escolha a forma de transcrição", ('Pasta', 'Arquivo'))
        if type_input == 'Pasta':
            folder = st.text_input('Informe o caminho da pasta (ex.: /home/audios/conversas)')
            if st.button('Transcrever'):
                df = transcribe_folder(folder, case_name, type_model)
    elif option == 'Consultar':
        st.subheader('Consultar')
        consult()

    
if __name__ == '__main__':
    main()
