import pandas as pd


REQUIRED_COLUMNS = {
    "entity_id",
    "t",
    "state_valid",
    "event_flag",
    "decision_raw",
    "decision_final",
}


def validate_log_schema(df: pd.DataFrame):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"[metrics] Missing required columns: {missing}")



def compute_toggle_rate(df: pd.DataFrame, decision_col: str) -> float:
    series = df[decision_col]
    if len(series) <= 1:
        return 0.0
    return (series != series.shift(1)).sum() / (len(series) - 1)


def compute_false_intervention_rate(
    df: pd.DataFrame,
    decision_col: str,
    domain: str,
    config: dict | None = None,
) -> float:
    """
    decision == 1 (INTERVENE) but no real event
    battery: event_flag == 0
    ehr: state_value below threshold (proxy)
    """
    df = df[df["state_valid"]]

    if domain == "battery":
        mask = df["event_flag"] == 0

    elif domain == "ehr":
        if "state_value" not in df.columns:
            return 0.0
        threshold = config.get("ehr_threshold", 1.0) if config else 1.0
        mask = df["state_value"] < threshold

    else:
        raise ValueError(f"[metrics] Unknown domain: {domain}")

    denom = mask.sum()
    if denom == 0:
        return 0.0

    num = ((df[decision_col] == 1) & mask).sum()
    return num / denom

def compute_stabilization_rate(
    df: pd.DataFrame,
    decision_col: str,
    domain: str,
    config: dict | None = None,
) -> float:
    """
    After event_flag == 1,
    decision stays INTERVENE for window steps
    """
    window = config.get("stabilization_window", 3) if config else 3

    df = df.sort_values("t").reset_index(drop=True)
    event_indices = df.index[df["event_flag"] == 1].tolist()

    if not event_indices:
        return 0.0

    success = 0
    for idx in event_indices:
        end = idx + window
        if end >= len(df):
            continue
        if (df.loc[idx:end - 1, decision_col] == 1).all():
            success += 1

    return success / len(event_indices)

def compute_all_metrics(
    df: pd.DataFrame,
    experiment_meta: dict,
) -> dict:
    """
    experiment_meta required keys:
      - experiment_id
      - domain
    optional:
      - config (dict)
    """
    validate_log_schema(df)

    domain = experiment_meta["domain"]
    exp_id = experiment_meta["experiment_id"]
    config = experiment_meta.get("config", {})

    metrics = {
        "experiment_id": exp_id,
        "domain": domain,
        "n_rows_total": len(df),
        "n_rows_valid": int(df["state_valid"].sum()),
        "toggle_rate_raw": compute_toggle_rate(df, "decision_raw"),
        "toggle_rate_final": compute_toggle_rate(df, "decision_final"),
        "false_intervention_rate_raw": compute_false_intervention_rate(
            df, "decision_raw", domain, config
        ),
        "false_intervention_rate_final": compute_false_intervention_rate(
            df, "decision_final", domain, config
        ),
        "stabilization_rate_raw": compute_stabilization_rate(
            df, "decision_raw", domain, config
        ),
        "stabilization_rate_final": compute_stabilization_rate(
            df, "decision_final", domain, config
        ),
    }

    return metrics