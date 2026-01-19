from pathlib import Path
import yaml
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]   # first_week/
CONFIG_PATH = BASE_DIR / "configs" / "experiments.yaml"

# state_type → 실제 recipe 매핑
STATE_TYPE_TO_RECIPE = {
    "battery": "battery_soh_v1",
    "ehr": "ehr_baseline_v1",
}


def load_experiment(experiment_id):
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    if experiment_id not in config["experiments"]:
        raise ValueError(f"Unknown experiment_id: {experiment_id}")

    exp = config["experiments"][experiment_id]

    # CSV 로드
    csv_path = BASE_DIR / exp["csv_path"]
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)

    # state_recipe 결정
    state_recipe = exp.get("state_recipe")
    if state_recipe is None:
        state_type = exp.get("state_type")
        if state_type is None:
            raise ValueError(
                f"Experiment '{experiment_id}' must define either "
                f"'state_recipe' or 'state_type'"
            )
        if state_type not in STATE_TYPE_TO_RECIPE:
            raise ValueError(f"Unknown state_type: {state_type}")
        state_recipe = STATE_TYPE_TO_RECIPE[state_type]

    return {
    "experiment_id": experiment_id,
    "domain": exp["domain"],
    "df": df,
    "state_recipe": exp.get("state_recipe"),
    "state_window": exp.get("state_window"),
    "decision_policy": exp["decision_policy"],
    "decision_threshold": exp.get("decision_threshold"),  # ← 추가
    "guardrail_policy": exp["guardrail_policy"],
}