# CLAUDE.md

This file guides Claude Code (claude.ai/code) when it works in this repository.

## Project status

This is an academic ML project: compare supervised classifiers that predict diabetes, implemented in both Python (scikit-learn) and Orange Data Mining, plus a PyTorch neural network built up step by step as a learning exercise. The work goes in phases, and the user approves each phase before the next one starts: (1) plan, (2) EDA, (3) sklearn and PyTorch, (4) Orange, (5) comparison, (6) PDF report and README.

Done so far: Phase 2 (EDA).

**Language: every deliverable is in Brazilian Portuguese.** That covers notebook text, figure titles and labels, table column names, file names of outputs, code comments and docstrings, the README and the report. Python identifiers stay in English. Use correct accents.

**Orange:** the user uses the standalone Orange Data Mining desktop app, not the Python package. The `.ows` workflow is built for that app.

## Environment and commands

- Windows, using the **global** Microsoft Store Python 3.12. The user does not want a virtual environment.
- JupyterLab cannot be installed: the Store Python hits the Windows long-path limit. Notebooks are run headless and viewed in VS Code.
- Install dependencies: `python -m pip install -r requirements.txt`
- Run a notebook: `python -m nbconvert --to notebook --execute --inplace notebooks/01_eda.ipynb`. Use `python -m nbconvert`, because `jupyter nbconvert` is not on PATH.
- Notebooks import project code by putting `../src` on `sys.path`. There is no installed package.

## Layout

- `data/raw/diabetes_pt.csv` is the original data and must never be modified. `data/splits/` will hold the shared train/test CSVs, which Orange also loads.
- `src/diabetes/` holds the shared code:
  - `config.py`: seed 42, 20% test size, column lists, the `ZERO_AS_MISSING` columns.
  - `data.py`: `load_raw`, `zeros_to_nan`.
  - `plotting.py`: class colors (class 0 blue `#2a78d6`, class 1 orange `#eb6834`), Portuguese class labels, `apply_style`, `save_fig`.- `notebooks/` contains `01_eda.ipynb`. Phase 3 will add the sklearn and PyTorch notebooks.
- `results/figures/` holds PNGs for the report and `results/tables/` holds CSVs, both written by the notebooks.

## Methodological rules (agreed with the user)

- Use one stratified 80/20 split with `random_state=42`. The test set is used only for the final evaluation. Every model selection decision is made with cross-validation on the training set.
- Preprocessing, decided in `01_eda.ipynb` §10:
  - Convert zeros to NaN in the 5 `ZERO_AS_MISSING` columns.
  - Impute with the median, fitted on the training data.
  - Standardize with a z-score, fitted on the training data, for **all** models.
  - Keep all 8 features and all outliers.
  - Add no missing-value indicator columns and do no resampling.
  - Fitted steps always run inside an sklearn `Pipeline`.
- Python and Orange must use the same split files and the same explicit hyperparameters, with the target class set to 1 for metrics.
- Never invent results. Every number in docs or the report must come from an executed output.

## Dataset: `data/raw/diabetes_pt.csv`

This is the Pima Indians Diabetes dataset (768 rows, 9 columns, comma-separated, with a header row) with the column names translated into Portuguese. The column names are used exactly as written, including the original misspellings `Gavidez` and `Espesura_da_Pele`. Do not "fix" them in the CSV.

| Column | Meaning | Type |
|---|---|---|
| `Gavidez` | Number of pregnancies (Gravidez) | int |
| `Glicose` | Plasma glucose concentration (2h OGTT) | int |
| `PressaoArterial` | Diastolic blood pressure (mm Hg) | int |
| `Espesura_da_Pele` | Triceps skinfold thickness (mm) | int |
| `Insulina` | 2-hour serum insulin (mu U/ml) | int |
| `IMC` | Body mass index (BMI) | float |
| `Diabetes_Hereditaria` | Diabetes pedigree function | float |
| `Idade` | Age (years) | int |
| `Resultado` | **Target**: 1 = diabetic, 0 = not | int |

Data-quality notes that matter for modeling:
- **No NaNs, but there are hidden missing values stored as `0`.** A zero is physiologically impossible in `Glicose` (5 rows), `PressaoArterial` (35), `Espesura_da_Pele` (227), `Insulina` (374) and `IMC` (11). Treat these zeros as missing and impute them, for example with the median. Fit the imputation on the training split only. A zero in `Gavidez` is a valid value.
- **The classes are imbalanced:** 500 negatives and 268 positives (about 35% positive). Use stratified splits. Report recall, precision, F1 and ROC-AUC alongside accuracy. For a medical screening model, recall on the positive class is usually the priority.
