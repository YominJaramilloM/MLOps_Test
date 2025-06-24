from prefect import task, flow
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd


@task(
    name="Load Boston Housing Dataset",
    tags=["data_loading"],
    description="Load Boston Housing dataset from sklearn",
)
def get_data(path) -> dict:
    """This function loads the boston Housing dataset from sklearn and returns it as a dictionary."""
    data = pd.read_csv(path).values
    return {"data": data[:, :-1], "target": data[:, -1]}

@task(
    name="Split Data",
    tags=["data_processing"],
    description="Split dataset into train and test sets",
)
def split_data(dataset: dict) -> tuple:
    """This function splits the dataset into train and test sets."""
    X_train, X_test, y_train, y_test = train_test_split(
        dataset["data"], dataset["target"], test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test

@task(
    name="Train Model",
    tags=["model_training"],
    description="Train RandomForestClassifier model",
)
def train_model(X_train: list, X_test: list, y_train: list, y_test: list) -> str:
    """This function trains a RandomForestClassifier model and returns the accuracy."""
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    r2 = model.score(X_test, y_test)
    print("el r2_score es de: ", r2)
    return f"Model trained with r2_score: {r2:.2f}"


@flow(retries=3, retry_delay_seconds=5, log_prints=True)
def bostonHousingRegressor():
    """This function orchestrates the whole flow"""
    dataset = get_data('https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv')
    print(dataset["data"])
    X_train, X_test, y_train, y_test = split_data(dataset)
    train_model(X_train, X_test, y_train, y_test)


bostonHousingRegressor()
