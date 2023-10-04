# Usa una imagen base de Python
FROM python:3.12

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias de la aplicación
RUN pip install -r requirements.txt

# Copia el contenido de la aplicación al directorio de trabajo
COPY . /app

# Expone el puerto en el que la aplicación Flask va a escuchar
EXPOSE 80

# Define el comando que se ejecutará cuando se inicie el contenedor
CMD ["python", "app.py"]
