import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from app.db import engine, create_db_and_tables, PredictionsClients
from app.utils import data_preprocessing
from sqlmodel import Session, select
from enum import Enum
import os
from typing import List
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="FastAPI, Docker, and grafana", lifespan=lifespan)

# define data structure for each input 
class userIn(BaseModel):
    client_name: str
    input: List[float]

# define data structure for request 
class ProcessDataRequestModel(BaseModel):
    sentences: list[userIn]

#entrypoint
@app.post("/predict")
async def read_root(data: ProcessDataRequestModel):

    session = Session(engine)
    
    model_path = os.path.join(BASE_DIR, '..', 'tracking', 'models', 'model_rfr.pkl')
    model = joblib.load(os.path.abspath(model_path))

    preds_list = []

    for sentence in data.sentences: 
        X = np.array([sentence.input])  # convierte a array 2D
        processed_data = data_preprocessing(X)
        pred = model.predict(processed_data)


        # create object with predictions
        prediction_Client = PredictionsClients(
            client_name=sentence.client_name,
            prediction=float(pred[0])
        )
        

        preds_list.append({
            "client_name": sentence.client_name,
            "prediction": float(pred[0])
        })
        
        print('ESTO ES PREDS_LIST:', preds_list)

        session.add(prediction_Client)

    session.commit() # bulk
    session.close()

    return JSONResponse(content={"predictions": preds_list})




