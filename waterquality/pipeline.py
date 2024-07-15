"""
This module contains the function to create a pipeline object.
"""

import os

from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from waterquality.data_handling import load_data, save_pipeline, split_data

load_dotenv()


def create_pipeline() -> Pipeline:
    """
    Create a pipeline object.

    Returns:
        Pipeline: A pipeline object.
    """
    data_file = os.getenv("DATA_FILE_NAME")
    data = load_data(data_file)
    X_train, y_train = split_data(data)

    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(random_state=0)),
        ]
    )

    pipeline.fit(X_train, y_train)
    save_pipeline(pipeline)


if __name__ == "__main__":
    create_pipeline()
    print("Pipeline created and saved successfully.")
