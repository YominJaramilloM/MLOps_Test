# 🏡 SalvaHealth - ML para Boston Housing con MLflow, Prefect y Docker

Este repositorio contiene el desarrollo de un pipeline de entrenamiento, versionamiento y despliegue de modelos de Machine Learning aplicados al conjunto de datos **Boston Housing** (https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv). 

El proyecto fue diseñado con una arquitectura modular, seguimiento de experimentos, ejecución orquestada y despliegue dockerizado.

---

## 🚀 Arquitectura del Proyecto

```bash
SALVAHEALTH/
│
├── tracking/                    # Lógica de entrenamiento y orquestación
│   ├── BostonHousingRegressor  # Script principal de entrenamiento
│   ├── main.py                 # Pipeline orquestado con Prefect
│   ├── config.py               # Parámetros generales
│   ├── utils.py                # Funciones auxiliares
│   ├── scaler.pkl              # Scaler serializado
│   └── mlruns/                 # Carpeta generada por MLflow (experimentos)
│
├── app/                        # Lógica de API y configuración para docker
│   ├── main.py                 # FastAPI app para predicción
│   ├── config.py               # Variables de entorno
│   ├── db.py                   # Conexión con base de datos
│   ├── prestart.sh             # Script para esperas previas al arranque
│
├── Dockerfile                  # Imagen base de la API
├── docker-compose.yml          # Orquestación de servicios Docker
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

📦 Entrenamiento del Modelo
Los archivos principales para el entrenamiento del modelo son:

tracking/BostonHousingRegressor: contiene la lógica del modelo y pruebas iniciales.

tracking/main.py: define el pipeline automático usando Prefect y ejecuta los experimentos.

🧪 **Seguimiento de experimentos**
El seguimiento y versionado de experimentos se realiza mediante MLflow. Puedes lanzar la interfaz gráfica con:

mlflow ui
O si estás utilizando una base de datos SQLite como backend:
mlflow ui --backend-store-uri sqlite:///mlflow.db
![MLflow UI](images/mlFlowUI.PNG)

La carpeta mlruns/ almacena los experimentos realizados.

⚙️ **Ejecución automática (pipeline)**
El archivo tracking/main.py orquesta todo el flujo de trabajo automáticamente con Prefect. Este pipeline:
Despues de correr el flujo puede revisar el proceso de ejecucion con los log setiados en la UI de prefect mediante:

prefect server start
![Ejecución de Prefect](images/PrefectFlow.PNG)
Preprocesa los datos.

Entrena varios modelos.

Evalúa los resultados.

Registra los experimentos en MLflow.

Selecciona el mejor modelo.
![Ejecución de Prefect](images/ModelFlowsExecutionPrefect.PNG)

🐳 **Dockerización y despliegue**
La carpeta app/ contiene la configuración necesaria para dockerizar y probar localmente la API de predicción. Para levantar todo el entorno con Docker:

sudo docker-compose up --build
Esto levantará:

La API FastAPI con el modelo entrenado.

La conexión a la base de datos.

La exposición de la API para pruebas con Postman.
![Prueba local con Postman](images/PostmanModelTestLocal.PNG)
📍 Despliegue en AWS
Este proyecto fue desplegado en una instancia EC2 de  AWS  con IP publica: http://3.129.194.31:5004/predict
Para mayor detalle del setting de la instancia de EC2 revise el ![Readme de despliegue en prod](app/README.md)

📬 Contacto
Desarrollado por Yomin Jaramillo M
Para preguntas o soporte, abre un issue o contáctame por yominjaramillo@outlook.com.
