import streamlit as st

def about():
    st.subheader('Selecione uma opção no menu lateral.')
    st.text('''
    O Programa LEIA é um software de transcrição de áudio e vídeo.
    Você pode transcrever novos arquivos ou consultar casos já transcritos.
    Documentação em: https://github.com/andrecorumba/leia
    ''')