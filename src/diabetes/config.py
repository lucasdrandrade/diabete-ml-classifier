"""Project-wide constants: paths, column roles and the random seed.

Every notebook and script imports from here so that the experiment
conditions (seed, split ratio, column lists) are defined in exactly one place.
"""

from pathlib import Path

# --- Paths -----------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "diabetes_pt.csv"
SPLITS_DIR = PROJECT_ROOT / "data" / "splits"
FIGURES_DIR = PROJECT_ROOT / "results" / "figures"
TABLES_DIR = PROJECT_ROOT / "results" / "tables"

# --- Reproducibility -------------------------------------------------------
RANDOM_SEED = 42
TEST_SIZE = 0.20

# --- Column roles ----------------------------------------------------------
# Names are kept exactly as in the CSV, including the original misspellings
# ("Gavidez", "Espesura_da_Pele").
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

# Columns where a value of 0 is physiologically impossible and therefore
# encodes a missing measurement. "Gavidez" is excluded: zero pregnancies is
# a legitimate value.
ZERO_AS_MISSING = [
    "Glicose",
    "PressaoArterial",
    "Espesura_da_Pele",
    "Insulina",
    "IMC",
]
