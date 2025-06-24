import os
import pickle

def save_pickle(data, filename) -> None:
    """
    This function saves the data in a pickle file. Args:
        data (object): data to save, filename (str): filename
    Returns:
        None
    """
    filepath = os.path.join("data_processed", f"{filename}.pkl")
    with open(filepath, 'wb') as file:
        pickle.dump(data, file)

def save_model(model, filename) -> None:
    """
    This function saves the data in a pickle file. Args:
        data (object): data to save, filename (str): filename
    Returns:
        None
    """
    filepath = os.path.join("models", f"{filename}.pkl")
    with open(filepath, 'wb') as file:
        pickle.dump(model, file)