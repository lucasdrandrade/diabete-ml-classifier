"""Constantes do projeto: caminhos, papéis das colunas e semente aleatória.

Todos os notebooks e scripts importam deste módulo, para que as condições do
experimento (semente, proporção do split, listas de colunas) sejam definidas
em um único lugar.
"""

from pathlib import Path

# --- Caminhos --------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "diabetes_pt.csv"
SPLITS_DIR = PROJECT_ROOT / "data" / "splits"
FIGURES_DIR = PROJECT_ROOT / "results" / "figures"
TABLES_DIR = PROJECT_ROOT / "results" / "tables"

# --- Reprodutibilidade -----------------------------------------------------
RANDOM_SEED = 42
TEST_SIZE = 0.20

# --- Papéis das colunas ----------------------------------------------------
# Os nomes são mantidos exatamente como no CSV, incluindo os erros de grafia
# originais ("Gavidez", "Espesura_da_Pele").
TARGET = "Resultado"
FEATURES = [
    "Gavidez",
    "Glicose",
    "PressaoArterial",
    "Espesura_da_Pele",
    "Insulina",
    "IMC",
    "Diabetes_Hereditaria",
    "Idade",
]

# Colunas em que o valor 0 é fisiologicamente impossível e, portanto,
# representa uma medição ausente. "Gavidez" fica de fora: zero gestações é
# um valor legítimo.
ZERO_AS_MISSING = [
    "Glicose",
    "PressaoArterial",
    "Espesura_da_Pele",
    "Insulina",
    "IMC",
]
