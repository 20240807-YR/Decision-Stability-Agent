from pathlib import Path
import yaml
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]   # first_week/
CONFIG_PATH = BASE_DIR / "configs" / "experiments.yaml"

def load_experiment(experiment_id):
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    exp = config["experiments"][experiment_id]

    csv_path = BASE_DIR / exp["csv_path"]   # 🔥 이 줄이 핵심
    df = pd.read_csv(csv_path)

    return {
        "experiment_id": experiment_id,
        "domain": exp["domain"],
        "df": df,
        "state_recipe": exp["state_recipe"],
        "decision_policy": exp["decision_policy"],
        "guardrail_policy": exp["guardrail_policy"],
    }