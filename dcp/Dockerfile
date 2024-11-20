# Usa la imagen base slim
FROM python:3.12-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Actualiza los paquetes e instala las dependencias necesarias para pycairo y matplotlib
RUN apt-get update && apt-get install -y \
    build-essential \         
    libcairo2-dev \                 
    libfreetype6-dev \       
    libpng-dev \         
    pkg-config \              
    && rm -rf /var/lib/apt/lists/*  

# Copia el archivo de requisitos e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto
COPY . .

# Expone el puerto 8000 para el servidor de desarrollo de Django
EXPOSE 8000

# Establece una variable de entorno para evitar buffering en Python
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar el servidor de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
