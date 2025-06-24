Documentación del Despliegue de un Modelo de Machine Learning en Producción usando AWS EC2, Docker y FastAPI

🌐 **Descripción General**

Este documento describe paso a paso el proceso de despliegue de un modelo de Machine Learning en un entorno de producción usando:

Una instancia EC2 de AWS

Docker y Docker Compose

FastAPI como framework web

PostgreSQL como base de datos

🚀 **Tecnologías Utilizadas**



🏢 **Arquitectura**

La aplicación se estructura en múltiples servicios Docker:

web: contiene la aplicación FastAPI y el modelo entrenado

db: base de datos PostgreSQL

adminer: UI para acceder a la base de datos 

grafana: visualización de métricas 
