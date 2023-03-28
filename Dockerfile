FROM python:3.10.10-slim

# Instala o FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    python -m pip install --upgrade pip &&\
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Cria o diretório de trabalho
WORKDIR /leia

# Clona o repositório do git hub
RUN git clone https://github.com/andrecorumba/leia.git .

# Instala as dependências
RUN pip install -r requirements.txt

# Copia o arquivo secret-token.txt para dentro do container na pasta /app
COPY secret-token.txt /leia

# Expõe a porta do Streamlit
EXPOSE 8501

# Informa ao Docker como testar um contêiner para verificar se ele ainda está funcionando. Seu contêiner precisa ouvir a porta 8501 (padrão) do Streamlit:
HEALTHCHECK CMD curl --fail http://0.0.0.0:8501/_stcore/health

# Define o comando para executar o Streamlit
ENTRYPOINT ["streamlit", "run", "app/app_docker.py", "--server.port=8501", "--server.address=0.0.0.0"]