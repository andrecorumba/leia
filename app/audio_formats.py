import os
from pydub import AudioSegment

def to_mp3(uploaded_file, upload_path):
   
    '''
    Transforma um arquivo de áudio ou vídeo em mp3.

    Parameters:
        uploaded_file (str): Nome do arquivo de áudio ou vídeo.
        upload_path (str): Caminho da pasta de upload onde o arquivo está.
        
    Returns:
        output_audio_file (str): Nome do arquivo de áudio ou vídeo em mp3.

    Example:
        to_mp3('audio.avi', 'audio.mp3', '/home/audios', '/home/audios')
        'audio.mp3'
    '''
    
    # Check if file is mp3
    if os.path.splitext(uploaded_file.name)[1] != ".mp3":

        # Create mp3 file name
        mp3_audio_file = uploaded_file.name.split('.')[0] + '.mp3'

        # Convert to mp3
        audio = AudioSegment.from_file(os.path.join(upload_path, uploaded_file.name))

        # Save file in mp3 format to upload folder
        audio.export(os.path.join(upload_path, mp3_audio_file), format="mp3")

    return mp3_audio_file 