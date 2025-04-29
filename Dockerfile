# Use uma imagem base com o Python instalado
FROM python:3.11-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt /app/

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o código da aplicação para o diretório de trabalho
COPY . /app/

# Execute o script
CMD ["python", "push.py"]
