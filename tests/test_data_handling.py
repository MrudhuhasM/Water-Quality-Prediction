"""
Test the data_handling module.
"""

import pandas as pd

from waterquality.config import FEATURES, TARGET_COL
from waterquality.data_handling import load_data


def test_load_data():
    data = load_data("data.csv")
    assert isinstance(data, pd.DataFrame)
    assert data.columns.tolist() == FEATURES + [TARGET_COL]
