FROM python:3.11-slim

# Instalar OpenSSL para generar certificados
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generar certificados SSL si no existen
RUN if [ ! -f ssl/cert.pem ]; then python3 generate_ssl.py; fi

EXPOSE 5000

CMD ["python3", "app.py"]