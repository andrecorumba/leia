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
    Procura pelo arquivo com o nome 'filename' (ignorando a extensão) dentro do arquivo .zip 'zip_file' e extrai apenas esse arquivo na pasta 'destination_folder'.
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

# def extract_media_files(zip_file, destination_folder):
#     media_extensions = (".opus",".wav",".mp3",".ogg",".wma",
#                         ".mp4", ".m4a", ".avi", ".mov", ".wmv")
#     media_files = []
    
#     with zipfile.ZipFile(zip_file) as zf:
       
#         for file_name in zf.namelist():
       
#             if file_name.lower().endswith(media_extensions):
       
#                 zf.extract(file_name, destination_folder)
#                 st.write(f"Arquivo '{file_name}' extraído com sucesso para a pasta '{destination_folder}'.")
#                 media_files.append(file_name)
                
#     return media_files

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

def main():
    filename = '7d84a529-7881-44cb-aeb6-715635f09ba1'
    zip_file = '/Volumes/Seagate Expansion Drive/AnexoLaudo499_2021_SETEC_RN/Midia/RelatorioPA/Apple_iPhone Xs Max(A1921)_2021-12-02_Relatório.ufdr'
    destination_folder = '/Users/andreluiz/Downloads/extracao'

    extract_file_from_zip_no_extension(filename, zip_file, destination_folder)

if __name__ == '__main__':
    main()