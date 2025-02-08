FROM python:3.8-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo requirements.txt
COPY requirements.txt .

# Actualizar pip e instalar las dependencias de Python
RUN pip install --upgrade pip && \
    pip install -U -r requirements.txt

# Copiar el resto del código
COPY . .

# Comando para ejecutar la aplicación
CMD ["python3", "main.py"]
