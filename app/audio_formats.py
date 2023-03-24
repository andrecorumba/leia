import os
from pydub import AudioSegment

# Convert audio file to mp3
def to_mp3(file_selected, original_folder_path, temporary_folder_path):
    '''
    Transforma um arquivo de áudio ou vídeo em mp3.

    Parameters:
        file_selected (str): Nome do arquivo de áudio ou vídeo.
        original_folder_path (str): Caminho da pasta de upload onde o arquivo está.
        temporary_folder_path (str): Caminho da pasta temporária onde o arquivo será salvo.
        
    Returns:
        mp3_audio_file (str): Nome do arquivo em formato mp3.
    '''
    
    # Check if file is mp3
    if os.path.splitext(file_selected)[1] != ".mp3":
        
        # Create mp3 file name
        mp3_audio_file = file_selected.split('.')[0] + '.mp3'

        # Convert to mp3
        audio = AudioSegment.from_file(os.path.join(original_folder_path, file_selected))

        # Save file in mp3 format to upload folder
        audio.export(os.path.join(temporary_folder_path, mp3_audio_file), format="mp3")

    return mp3_audio_file 
