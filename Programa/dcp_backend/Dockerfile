# Usa una imagen base oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de dependencias
COPY requirements.txt /app/

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Copia el código del proyecto al contenedor
COPY . /app/

# Expone el puerto 8000 para acceder a Django
EXPOSE 8000

# Comando para iniciar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
