"""This module is for text processing for model prediction."""
import os
import joblib
import numpy as np



def data_preprocessing(X_new):
    """Preprocess the input data for model prediction."""  
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #scaler = joblib.load('../tracking/scaler.pkl')
    scaler_path = os.path.join(BASE_DIR, 'tracking', 'scaler.pkl')
    scaler = joblib.load(scaler_path)
    # Aplicar transformación
    X_scaled = scaler.transform(X_new)
    return X_scaled

