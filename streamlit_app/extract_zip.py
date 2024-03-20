import os
import zipfile
import streamlit as st

def find_audio_files_in_zip(zip_file_name):
    '''Procura por arquivos de áudio dentro de um arquivo .zip
    e retorna uma lista com os nomes dos arquivos encontrados.
    
    Parameters:
        zip_file_name (str): Nome do arquivo .zip.
    '''
    
    audio_file_extensions = (".opus",".wav",".mp3",".ogg",".wma",
                             ".mp4", ".m4a", ".avi", ".mov", ".wmv")
    audio_files = []
    
    with zipfile.ZipFile(zip_file_name) as zip_file:
        for file_name in zip_file.namelist():
            if file_name.lower().endswith(audio_file_extensions):
                audio_files.append(file_name)
    
    return audio_files

def extract_file_from_zip_no_extension(filename, zip_file, destination_folder):
    """
    Procura pelo arquivo com o nome 'filename' (ignorando a extensão) dentro do arquivo .zip 'zip_file' 
    e extrai apenas esse arquivo na pasta 'destination_folder'.

    Parameters:
        filename (str): Nome do arquivo a ser extraído.
        zip_file (str): Nome do arquivo .zip.
        destination_folder (str): Nome da pasta de destino.
        
    """
    with zipfile.ZipFile(zip_file) as zf:
        for name in zf.namelist():
            if os.path.splitext(os.path.basename(name))[0] == os.path.splitext(filename)[0]:
                zf.extract(name, destination_folder)
                print(f"Arquivo '{filename}' extraído com sucesso para a pasta '{destination_folder}'.")
                return
    print(f"Arquivo '{filename}' não encontrado no arquivo .zip.")


def print_zip_file_name_list(zip_file, txt_file_output=None):
    """
    Imprime a lista de arquivos contidos no arquivo .zip 'zip_file'.

    Parameters:
        zip_file (str): Nome do arquivo .zip.
        txt_file_output (str): Nome do arquivo .txt de saída.
    """
    
    with zipfile.ZipFile(zip_file) as zf:

        if txt_file_output:
        
            with open(txt_file_output, "w") as f:
            
                for name in zf.namelist():
            
                    f.write(name + "\n")
            
                print("Arquivo name list gerado com sucesso!")
        
        return zf.namelist() 



def extract_media_files(zip_file, destination_folder):
    '''
    Extrai os arquivos de mídia de um arquivo .zip para uma pasta de destino.
    
    Parameters:
        zip_file (str): Nome do arquivo .zip.
        destination_folder (str): Nome da pasta de destino.

    '''
    
    media_extensions = (".opus",".wav",".mp3",".ogg",".wma",
                        ".mp4", ".m4a", ".avi", ".mov", ".wmv")
    media_files = []
    
    with zipfile.ZipFile(zip_file, "r") as zf:
       
        for file_name in zf.namelist():
       
            if file_name.lower().endswith(media_extensions):
                
                file_info = zf.getinfo(file_name)
                target_path = os.path.join(destination_folder, os.path.basename(file_name))
                
                with zf.open(file_info) as source, open(target_path, "wb") as target:
                
                    target.write(source.read())
                
                media_files.append(target_path)
                
    return media_files