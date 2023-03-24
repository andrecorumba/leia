import os
from pydub import AudioSegment
from io import BytesIO

def to_mp3(file, folder, temporary_mp3_folder):
   
    '''
    Transforma um arquivo de áudio ou vídeo em mp3.

    Parameters:
        uploaded_file (str): Nome do arquivo de áudio ou vídeo.
        upload_path (str): Caminho da pasta de upload onde o arquivo está.
        temporary_mp3_path (str): Caminho da pasta temporária onde o arquivo será salvo.
        
    Returns:
        output_audio_file (str): Nome do arquivo de áudio ou vídeo em mp3.

    Example:
        to_mp3('audio.avi', 'audio.mp3', '/home/audios', '/home/audios')
        'audio.mp3'
    '''
    
    # Check if file is mp3
    if os.path.splitext(file)[1] != ".mp3":

        # Create mp3 file name
        mp3_audio_file = file.split('.')[0] + '.mp3'

        # Convert to mp3
        audio = AudioSegment.from_file(os.path.join(folder, file))

        # Save file in mp3 format to upload folder
        audio.export(os.path.join(temporary_mp3_folder, mp3_audio_file), format="mp3")

    return mp3_audio_file 


def to_mp3_bytes(file, folder):
   
    '''
    Transforma um arquivo de áudio ou vídeo em mp3.

    Parameters:
        uploaded_file (str): Nome do arquivo de áudio ou vídeo.
        upload_path (str): Caminho da pasta de upload onde o arquivo está.
        
    Returns:
        bytes: Bytes correspondentes ao arquivo em formato mp3.

    Example:
        to_mp3_bytes('audio.avi', '/home/audios')
    '''
    
    # Check if file is mp3
    if os.path.splitext(file)[1] != ".mp3":

        # Convert to mp3
        audio = AudioSegment.from_file(os.path.join(folder, file))

        # Export mp3 format to BytesIO object
        bytes_io = BytesIO()
        audio.export(bytes_io, format="mp3", bytesio=True)

        # Get bytes from BytesIO object
        mp3_bytes = bytes_io.getbuffer()

    else:
        with open(os.path.join(folder, file), 'rb') as f:
            mp3_bytes = f.read()

    return mp3_bytes
