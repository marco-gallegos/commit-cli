# Usar una imagen base de Python 3.9
FROM python:3.9

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias de la aplicación
RUN pip install -r requirements.txt

# Copiar el contenido de la aplicación al contenedor
#COPY . .

# Exponer el puerto en el que se ejecutará la aplicación (si es necesario)
# EXPOSE 8000

# Comando para ejecutar la aplicación
#CMD ["python", "app.py"]
