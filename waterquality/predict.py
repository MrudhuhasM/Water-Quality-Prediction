import os

import joblib
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def load_pipeline() -> object:
    """
    Load the pipeline.

    Returns:
        object: Loaded pipeline.
    """
    save_path = os.getenv("MODEL_PATH")
    model_name = os.getenv("MODEL_NAME")
    model_path = os.path.join(save_path, model_name)
    pipeline = joblib.load(model_path)
    return pipeline


def make_prediction(data):
    """
    Make a prediction using a pre-trained model.

    Args:
        data (dict): A dictionary containing the data to be used for prediction.
    """
    data = pd.DataFrame(data, index=[0])
    pipeline = load_pipeline()
    prediction = pipeline.predict(data).astype(int)
    categories = ["No", "Yes"]
    return categories[prediction[0]]
