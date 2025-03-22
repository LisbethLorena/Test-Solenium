# Usar la imagen oficial de Python
FROM python:3.10

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Definir la variable de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Comando por defecto para ejecutar Flask
CMD ["flask", "run"]
