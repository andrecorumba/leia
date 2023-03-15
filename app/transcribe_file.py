import whisper
import streamlit as st
import os
from pydub import AudioSegment

def to_mp3(audio_file, output_audio_file, upload_path, download_path):
    '''
    Transforma um arquivo de áudio ou vídeo em mp3.

    Parameters:
        audio_file (str): Nome do arquivo de áudio ou vídeo.
        output_audio_file (str): Nome do arquivo de áudio ou vídeo.
        upload_path (str): Caminho da pasta de upload onde o arquivo está.
        download_path (str): Caminho da pasta de download onde o arquivo será salvo.

    Returns:
        output_audio_file (str): Nome do arquivo de áudio ou vídeo em mp3.

    Example:
        >>> to_mp3('audio.avi', 'audio.mp3', '/home/audios', '/home/audios')
        'audio.mp3'
    '''
    if os.path.splitext(audio_file.name)[1] == ".mp3":
        return audio_file.name

    audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name))
    output_file_path = os.path.join(download_path, os.path.splitext(output_audio_file)[0] + ".mp3")
    audio_data.export(output_file_path, format="mp3")

    return output_audio_file

def transcribe_file(uploaded_file, folder, type_model):
    '''
    Transcreve um arquivo de áudio ou vídeo.

    Parameters:
        uploaded_file (str): Nome do arquivo de áudio ou vídeo.
        folder (str): Caminho da pasta onde o arquivo está.
        type_model (str): Tipo de modelo a ser utilizado.

    Returns:
        result (str): Texto transcrito.

    Example:
        >>> transcribe_file('audio.mp3', '/home/audios', 'base')
        {'text': 'Olá, tudo bem?'}
    '''
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