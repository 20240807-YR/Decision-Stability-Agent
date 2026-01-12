import yaml
import pandas as pd
from pathlib import Path

CONFIG_PATH = Path("../configs/experiments.yaml")

def load_experiment(experiment_id):
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    exp = config["experiments"][experiment_id]

    df = pd.read_csv(exp["csv_path"])

    return {
        "experiment_id": experiment_id,
        "domain": exp["domain"],
        "df": df,
        "entity_id_hint": exp["entity_id_hint"],
        "time_hint": exp["time_hint"],
        "state_recipe": exp["state_recipe"],
        "decision_policy": exp["decision_policy"],
        "guardrail_policy": exp["guardrail_policy"],
        "llm_profile": exp["llm_profile"],
    }