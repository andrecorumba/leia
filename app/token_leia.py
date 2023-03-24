import string
from random import choice

def get_token_leia():
    ''' 
    Função que gera um token aleatório para identificar o caso de uso do app.

    Returns:
        Token (str): Token aleatório de 32 caracteres.
    '''

    return ''.join([choice(string.ascii_letters + string.digits) for i in range(32)])