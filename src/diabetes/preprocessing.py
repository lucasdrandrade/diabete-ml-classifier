"""Pipeline de pré-processamento decidido na EDA (notebook 01, §10)."""

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

from diabetes.config import FEATURES, ZERO_AS_MISSING

_ZERO_COLS_IDX = [FEATURES.index(c) for c in ZERO_AS_MISSING]


def _zeros_to_nan_array(X):
    """Versão para arrays de `zeros_to_nan`, usada dentro do Pipeline."""
    X = np.asarray(X, dtype=float).copy()
    cols = X[:, _ZERO_COLS_IDX]
    cols[cols == 0] = np.nan
    X[:, _ZERO_COLS_IDX] = cols
    return X


def build_preprocessor() -> Pipeline:
    """Zeros -> NaN, imputação pela mediana e padronização (z-score).

    A primeira etapa é sem estado e não tem efeito em dados que já chegam com
    NaN (como os CSVs de data/splits), mas mantém o pipeline correto para
    registros brutos. A mediana e a média/desvio-padrão são aprendidos apenas
    nos dados passados para `fit`, ou seja, somente no treino.
    """
    return Pipeline([
        ("zeros_para_nan", FunctionTransformer(_zeros_to_nan_array)),
        ("imputacao", SimpleImputer(strategy="median")),
        ("padronizacao", StandardScaler()),
    ])
