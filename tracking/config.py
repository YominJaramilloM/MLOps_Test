# config.py
# path with data processed
DATA_PATH = 'https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv'
# version of the data
VERSION = 1
# parameters for the model
PARAMETERS_MODEL = {
    "n_estimators": 100,
    "max_depth": 10,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "random_state": 42
}
# tags for mlflow tracking

DEVELOPER_NAME = "Yomin J"
MODEL_NAME = "RandomForestRegressor"