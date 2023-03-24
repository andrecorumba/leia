import os

def create_folders(token, main_folder_path):
    '''
    Cria as pastas necessárias para o funcionamento da aplicação.

    Parameters:
        token (str): Token do usuário.
        main_folder_path (str): Caminho da pasta principal.

    Returns:
        token_folder_path (str): Caminho da pasta do token.
        database_folder_path (str): Caminho da pasta do banco de dados.
        temporary_folder_path (str): Caminho da pasta temporária.
        original_folder_path (str): Caminho da pasta original.
    '''

    # Create the main folder if it doesn't exist yet
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)

    # Paths to the token folder to be created
    token_folder_path = os.path.join(main_folder_path, token)

    # Paths to the subfolders to be created
    database_folder_path = os.path.join(token_folder_path, "database")
    temporary_folder_path = os.path.join(token_folder_path, "temporary")
    original_folder_path = os.path.join(token_folder_path, "original")

    # Create the subfolders if they don't exist yet
    for subfolder_path in [database_folder_path, temporary_folder_path, original_folder_path]:
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
    
    return token_folder_path, database_folder_path, temporary_folder_path, original_folder_path

def get_folders(token, main_folder_path):
    ''''
    Retorna os caminhos das pastas necessárias para o funcionamento da aplicação.
    
    Parameters:
        token (str): Token do usuário.
        main_folder_path (str): Caminho da pasta principal.

    Returns:
        token_folder_path (str): Caminho da pasta do token.
        database_folder_path (str): Caminho da pasta do banco de dados.
        temporary_folder_path (str): Caminho da pasta temporária.
        original_folder_path (str): Caminho da pasta original.
    '''

    # Get the main folder
    token_folder_path = os.path.join(main_folder_path, token)

    # Paths to the subfolders to be created
    database_folder_path = os.path.join(token_folder_path, "database")
    temporary_folder_path = os.path.join(token_folder_path, "temporary")
    original_folder_path = os.path.join(token_folder_path, "original")

    return token_folder_path, database_folder_path, temporary_folder_path, original_folder_path