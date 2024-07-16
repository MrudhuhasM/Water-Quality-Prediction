import pandas as pd
from dotenv import load_dotenv

from waterquality.data_handling import load_pipeline

load_dotenv()


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
