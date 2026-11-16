"""Métricas, matrizes de confusão e utilitários de avaliação compartilhados.

Todos os modelos (scikit-learn e PyTorch) são avaliados pelas mesmas funções,
com a classe positiva sempre igual a 1 (com diabetes).
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    fbeta_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)

METRIC_ORDER = ["acurácia", "precisão", "recall", "especificidade", "f1", "roc_auc"]


def compute_metrics(y_true, y_pred, y_score=None) -> dict:
    """Calcula as métricas do projeto para a classe positiva 1.

    `y_score` é a probabilidade prevista da classe 1 (necessária só para a ROC-AUC).
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    metrics = {
        "acurácia": accuracy_score(y_true, y_pred),
        "precisão": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label=1),
        "especificidade": tn / (tn + fp),
        "f1": f1_score(y_true, y_pred, pos_label=1),
        "roc_auc": roc_auc_score(y_true, y_score) if y_score is not None else np.nan,
    }
    metrics.update({"VN": int(tn), "FP": int(fp), "FN": int(fn), "VP": int(tp)})
    return metrics


def bootstrap_ci(y_true, y_pred, y_score, n_boot: int = 2000, seed: int = 42, alpha: float = 0.05) -> pd.DataFrame:
    """Intervalos de confiança (percentil) por bootstrap do conjunto de teste.

    Reamostra as pacientes do teste com reposição e recalcula as métricas, para
    mostrar quanto o resultado poderia variar com outro conjunto de teste do
    mesmo tamanho.
    """
    rng = np.random.default_rng(seed)
    y_true, y_pred, y_score = map(np.asarray, (y_true, y_pred, y_score))
    samples = []
    n = len(y_true)
    while len(samples) < n_boot:
        idx = rng.integers(0, n, n)
        if y_true[idx].min() == y_true[idx].max():   # precisa das duas classes
            continue
        m = compute_metrics(y_true[idx], y_pred[idx], y_score[idx])
        samples.append([m[k] for k in METRIC_ORDER])
    samples = np.array(samples)
    return pd.DataFrame({
        "ic_inferior": np.quantile(samples, alpha / 2, axis=0),
        "ic_superior": np.quantile(samples, 1 - alpha / 2, axis=0),
    }, index=METRIC_ORDER)


def best_threshold_fbeta(y_true, y_score, beta: float = 2.0) -> float:
    """Limiar de decisão que maximiza o F-beta (beta=2 dá ao recall peso 2x).

    Deve ser chamado com probabilidades de validação (ou out-of-fold), nunca
    com as do conjunto de teste.
    """
    precision, recall, thresholds = precision_recall_curve(y_true, y_score)
    precision, recall = precision[:-1], recall[:-1]   # o último ponto não tem limiar
    denom = beta**2 * precision + recall
    fbeta = np.divide((1 + beta**2) * precision * recall, denom, out=np.zeros_like(denom), where=denom > 0)
    return float(thresholds[np.argmax(fbeta)])


def plot_confusion_matrix(ax, y_true, y_pred, title: str) -> None:
    """Desenha uma matriz de confusão com contagens e percentuais por linha."""
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    row_pct = cm / cm.sum(axis=1, keepdims=True)
    ax.imshow(row_pct, cmap="Blues", vmin=0, vmax=1)
    names = [["VN", "FP"], ["FN", "VP"]]
    for i in range(2):
        for j in range(2):
            color = "#ffffff" if row_pct[i, j] > 0.55 else "#0b0b0b"
            ax.text(j, i, f"{names[i][j]}\n{cm[i, j]}\n({row_pct[i, j]:.0%})",
                    ha="center", va="center", fontsize=9, color=color)
    ax.set_xticks([0, 1], ["Prev. 0", "Prev. 1"])
    ax.set_yticks([0, 1], ["Real 0", "Real 1"])
    ax.set_title(title, fontsize=10)
    ax.grid(False)


def f2_score(y_true, y_pred) -> float:
    """Atalho para o F2 (recall com peso 2x em relação à precisão)."""
    return fbeta_score(y_true, y_pred, beta=2, pos_label=1)
