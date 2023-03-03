# Script para transcrição de áudios e videos, usando biblioteca Openai-Whisper

import os
import whisper
import pandas as pd

import sqlite3

import PySimpleGUI as sg

import tkinter

def transcreve_pasta(pasta, nome_saida, modelo):
    # Carrega o modelo 'base'. Para carregar outros modelos mais precisos substitua por 'small' ou 'large'
    # O tempo de execução será maior a depender do modelo
    # Mais info: https://github.com/openai/whisper
    model = whisper.load_model(modelo)
    
    i = 1
    quantidade = len(os.listdir(pasta))

    for nome_arquivo in os.listdir(pasta):
        try:
            if nome_arquivo.endswith(".opus"):
                print(f"Transcrevendo {i} de {quantidade}")
            
                result =  model.transcribe(os.path.join(pasta,nome_arquivo))
            
                dic_transcricao = {'arquivo'     : [nome_arquivo],
                                   'transcricao' : [result['text']]}
            
                df = pd.DataFrame(dic_transcricao)

                # estabelece conexão com o banco de dados SQLite
                conn = sqlite3.connect(f'/Users/andreluiz/projetos/leia/saidas/{nome_saida}.db')

                # escreve o DataFrame na tabela SQLite usando o método to_sql()
                df.to_sql(name='tb_transcricoes', con=conn, if_exists='append', index=False)

                # fecha a conexão com o banco de dados
                conn.close()
            
                print(f"Banco de dados gravado com sucesso!")
            
                i=i+1
        except Exception as e:
            print(f"Algo deu errado", e)

def exporta_csv(nome_saida):
    # estabelece conexão com o banco de dados SQLite
    conn = sqlite3.connect(f'/Users/andreluiz/projetos/leia/saidas/{nome_saida}.db')

    query = 'SELECT * FROM tb_transcricoes'

    df = pd.read_sql(query, conn)

    df.to_csv(f'/Users/andreluiz/projetos/leia/saidas/{nome_saida}.csv', sep=';', encoding='utf-8', index=False)

    print("Arquivo CSV Gerado")

def criar_gui():
    # implemetar interface GUI para carregar e transcrever os arquivos
    sg.theme('LightBrown')  # Definindo o tema da interface

    # Criando o layout da interface
    layout = [[sg.Text('Digite o caminho da pasta:')],
              [sg.Input(key='-FOLDER-', enable_events=True), sg.FolderBrowse()],
              [sg.Text('Selecione o tipo de saída:')],
              [sg.Radio('Arquivo TXT', 'RADIO1', key='-TXT-', default=True),
               sg.Radio('Planilha Excel', 'RADIO1', key='-EXCEL-'),
               sg.Radio('PDF', 'RADIO1', key='-PDF-')],
              [sg.Button('Transcrever'), sg.Button('Cancelar')]]

    # Criando a janela
    window = sg.Window('Transcrição de Pasta', layout)

    # Loop principal da interface
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancelar':  # Se a janela for fechada ou o botão 'Cancelar' for pressionado
            break
        if event == 'Transcrever':  # Se o botão 'Transcrever' for pressionado
            folder_path = values['-FOLDER-']
            txt_output = values['-TXT-']
            excel_output = values['-EXCEL-']
            pdf_output = values['-PDF-']
            # Implementar a lógica de transcrição aqui
            # Dependendo do tipo de saída selecionado, a saída deve ser salva em um arquivo TXT, Excel ou PDF
            sg.popup('Transcrição concluída!')

    window.close()  # Fechando a janela


def main():
    #pasta = input("Informe o caminho da pasta com os arquivos a serem transcritos (.opus): ")
    #nome_saida = input("Informe um nome para o banco de dados de saida: ")
    pasta = '/Users/andreluiz/projetos/leia/entradas/audios'
    nome_saida = 'oper_432'
    modelo = 'base'
    #transcreve_pasta(pasta, nome_saida, modelo)
    #criar_gui()
    #exporta_csv(nome_saida)
    tkinter.Tcl().eval('info patchlevel')
    

if __name__ == '__main__':
    main()
