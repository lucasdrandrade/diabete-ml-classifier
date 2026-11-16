"""Funções de carregamento do dataset."""

import numpy as np
import pandas as pd

from diabetes.config import RAW_DATA_PATH, ZERO_AS_MISSING


def load_raw() -> pd.DataFrame:
    """Carrega o CSV original, sem nenhuma modificação."""
    return pd.read_csv(RAW_DATA_PATH)


def zeros_to_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna uma cópia em que os zeros impossíveis viram NaN.

    Esta etapa não aprende nada com os dados (é "stateless"), então aplicá-la
    antes da divisão treino/teste não causa vazamento de dados.
    """
    out = df.copy()
    out[ZERO_AS_MISSING] = out[ZERO_AS_MISSING].replace(0, np.nan)
    return out
