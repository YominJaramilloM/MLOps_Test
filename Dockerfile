# pull the official docker image with python version
FROM python:3.11.1-slim
# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar archivos del proyecto
COPY . .

# dar permisos de ejecución al script de pre-inicio
RUN chmod +x /app/app/prestart.sh

# comando de ejecución del contenedor
CMD ["/app/app/prestart.sh", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]