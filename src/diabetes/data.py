"""Carregamento do dataset e criação da divisão treino/teste compartilhada."""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from diabetes.config import (
    FEATURES,
    RANDOM_SEED,
    RAW_DATA_PATH,
    SPLITS_DIR,
    TARGET,
    TEST_SIZE,
    ZERO_AS_MISSING,
)

TRAIN_PATH = SPLITS_DIR / "treino.csv"
TEST_PATH = SPLITS_DIR / "teste.csv"


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


def make_splits() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cria a divisão 80/20 estratificada (semente fixa) e grava os CSVs.

    Os zeros impossíveis já saem como células vazias, para que o Python e o
    Orange recebam exatamente os mesmos dados de entrada.
    """
    df = zeros_to_nan(load_raw())
    train, test = train_test_split(
        df, test_size=TEST_SIZE, stratify=df[TARGET], random_state=RANDOM_SEED
    )
    SPLITS_DIR.mkdir(parents=True, exist_ok=True)
    train.to_csv(TRAIN_PATH, index=False)
    test.to_csv(TEST_PATH, index=False)
    return train, test


def load_splits() -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """Lê os CSVs de treino e teste e devolve X_train, y_train, X_test, y_test."""
    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(TEST_PATH)
    return train[FEATURES], train[TARGET], test[FEATURES], test[TARGET]
