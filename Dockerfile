# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de requisitos e o código-fonte
COPY requirements.txt .
COPY app.py .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Flask usará
EXPOSE 3434

# Comando para iniciar a aplicação
CMD ["streamlit run app.py"]
