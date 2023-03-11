import zipfile
import sqlite3
import os

def find_opus_files(zip_file_path, db_file_path):
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