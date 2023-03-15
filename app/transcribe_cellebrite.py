import zipfile
import sqlite3
import os

def find_opus_files(zip_file_path, db_file_path):
    ''' 
    Encontra todos os arquivos .opus dentro de um arquivo compactado pelo Cellebrite (UFED) e os insere em um banco de dados. 
    Para maiores informações sobre o Cellebrite visite: https://www.cellebrite.com/.
    Funciona também para arquivos compactados com ZIP.
    
    Parameters:
        zip_file_path (str): Caminho do arquivo compactado pelo Cellebrite.
        db_file_path (str): Caminho do banco de dados onde os arquivos .opus serão armazenados.

    Returns:
        (None): None
    '''
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS opus_files (name TEXT, path TEXT, binary BLOB)")

    with zipfile.ZipFile(zip_file_path) as zip_file:
        # percorre todas as entradas do arquivo zip
        for entry in zip_file.infolist():
            # verifica se é um arquivo com a extensão .opus
            if entry.filename.endswith('.opus'):
                # obtém o conteúdo do arquivo
                binary = zip_file.read(entry)

                # insere as informações no banco de dados
                cursor.execute("INSERT INTO opus_files (name, path, binary) VALUES (?, ?, ?)", (entry.filename, os.path.dirname(entry.filename), binary))

    conn.commit()
    conn.close()