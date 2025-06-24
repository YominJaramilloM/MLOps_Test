# Standard library imports
import warnings
# Third party imports
import pandas as pd
import mlflow
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from prefect import flow, task
# Local application imports
from config import *
from utils import save_pickle, save_model
import joblib

warnings.filterwarnings("ignore")

@task(
    name="Load Boston Housing Dataset",
    tags=["data_loading"],
    description="Load Boston Housing dataset from github",
)
def get_data(path) -> dict:
    """This function loads the boston Housing dataset from sklearn and returns it as a dictionary."""
    data = pd.read_csv(path).values
    return {"data": data[:, :-1], "target": data[:, -1]}

@task(
    name="Split Data",
    tags=["data_processing", "data_splitting"],
    description="Split dataset into train, validation and test sets",
)
def split_data(dataset: dict) -> tuple:
    """This function splits the dataset into train and test sets."""
    X_train, X_test, y_train, y_test = train_test_split(dataset["data"], dataset["target"], test_size=0.2, random_state=42)
    #X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.5, random_state=42)
    return X_train, X_test, y_train, y_test

@task(
    name="Data Scaling",
    tags=["data_processing", "data_scaling"],
    description="Scale the dataset using MinMaxScaler",
)
def scale_data(X_train, X_test, y_train, y_test):
    """This function scales the dataset using MinMaxScaler and save them."""
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    #X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, 'scaler.pkl')
    save_pickle((X_train, y_train), "train")
    #save_pickle((X_val, y_val), "val")
    save_pickle((X_test, y_test), "test")
    return X_train_scaled, X_test_scaled, scaler

@task(
    retries=3,
    retry_delay_seconds=2,
    name="Train  model",
    tags=["train", "RandomForestRegressor"],
)
def training(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    params: dict,
    model_name: str,
):
    with mlflow.start_run(run_name=model_name):
        mlflow.set_tag("developer", DEVELOPER_NAME)
        mlflow.set_tag("model_name", MODEL_NAME)
        mlflow.log_params(params)
        model = RandomForestRegressor(**params)
        model.fit(X_train, y_train)
        y_train_pred = model.predict(X_train)
        y_val_pred = model.predict(X_test)

        mse_train = round(mean_squared_error(y_train, y_train_pred), 2)
        mse_val = round(mean_squared_error(y_test, y_val_pred), 2)
        r2_train = round(r2_score(y_train, y_train_pred), 2)
        r2_val = round(r2_score(y_test, y_val_pred), 2)
        print("Mean Squared Error Train:", mse_train)
        print("Mean Squared Error Validation:", mse_val)
        print("R2 Score Train:", r2_train)
        print("R2 Score Validation:", r2_val)
        mlflow.log_metric("mse_train", mse_train)
        mlflow.log_metric("mse_val", mse_val)
        mlflow.log_metric("r2_train", r2_train)
        mlflow.log_metric("r2_val", r2_val)

        mlflow.sklearn.log_model(model, f"model_{MODEL_NAME}")
        # save model
        save_model(model, "model_rfr")
        print("Model saved successfully.")
        return [mse_train, mse_val, r2_train, r2_val]

@flow(
    retries=3,
    retry_delay_seconds=2,
    name="Boston Housing Regressor",
)
def boston_housing_regressor():
    """This function orchestrates the whole flow"""
    # Set the experiment name for MLflow
    mlflow.set_experiment("Boston Housing Regressor")
    dataset = get_data(DATA_PATH)
    X_train, X_test, y_train, y_test = split_data(dataset)
    X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test, y_train, y_test)
    params = PARAMETERS_MODEL
    model_name = MODEL_NAME
    training(X_train_scaled, X_test_scaled, y_train, y_test, params, model_name)
    

boston_housing_regressor()