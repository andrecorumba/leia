import whisper
import streamlit as st
import os
from pydub import AudioSegment

def to_mp3(audio_file, output_audio_file, upload_path, download_path):
    audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name))
    output_file_path = os.path.join(download_path,os.path.splitext(output_audio_file)[0] + ".mp3")
    audio_data.export(output_file_path, format="mp3")

    return output_audio_file

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