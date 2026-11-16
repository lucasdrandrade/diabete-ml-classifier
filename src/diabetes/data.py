"""Dataset loading helpers."""

import numpy as np
import pandas as pd

from diabetes.config import RAW_DATA_PATH, ZERO_AS_MISSING


def load_raw() -> pd.DataFrame:
    """Load the original CSV without any modification."""
    return pd.read_csv(RAW_DATA_PATH)


def zeros_to_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy where impossible zeros are replaced by NaN.

    This step is stateless (it learns nothing from the data), so applying it
    before the train/test split does not cause leakage.
    """
    out = df.copy()
    out[ZERO_AS_MISSING] = out[ZERO_AS_MISSING].replace(0, np.nan)
    return out
