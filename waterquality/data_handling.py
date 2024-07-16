"""
This module contains functions for handling data.
"""

import os

import joblib
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

from waterquality import config

load_dotenv()


def load_data(file_name: str) -> pd.DataFrame:
    """
    Load data from a CSV file.

    Parameters
    ----------
    file_name : str
        The name of the CSV file to load.

    Returns
    -------
    pd.DataFrame
        The data loaded from the CSV file.
    """
    data_path = os.getenv("DATA_PATH")
    file_path = os.path.join(data_path, file_name)
    data = pd.read_csv(file_path)
    data["ammonia"] = pd.to_numeric(data["ammonia"], errors="coerce")
    data["is_safe"] = pd.to_numeric(data["is_safe"], errors="coerce")
    data.dropna(inplace=True)
    return data


def split_data(data: pd.DataFrame, subseet: str = "train") -> tuple:
    """
    Split data into training and testing subsets.

    Args:
        data (pd.DataFrame): Data to split.
        subseet (str, optional): Subset to return. Defaults to 'train'.

    Returns:
        tuple: Training and testing subsets.
    """
    taregt_col = config.TARGET_COL
    X_train, X_test, y_train, y_test = train_test_split(
        data.drop(taregt_col, axis=1), data[taregt_col], test_size=0.2, random_state=0
    )
    if subseet == "test":
        return X_test, y_test
    return X_train, y_train


def save_pipeline(pipeline: object) -> None:
    """
    Save the pipeline.

    Args:
        pipeline (object): Pipeline to save.
    """
    save_path = os.getenv("MODEL_PATH")
    os.makedirs(save_path, exist_ok=True)
    model_name = os.getenv("MODEL_NAME")
    model_path = os.path.join(save_path, model_name)
    joblib.dump(pipeline, model_path)
    print(f"Pipeline saved at {model_path}")
