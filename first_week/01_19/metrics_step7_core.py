import pandas as pd
from typing import Dict


REQUIRED_COLUMNS = {
    "entity_id",
    "t",
    "state_valid",
    "event_flag",
    "decision_raw",
    "decision_final",
}


def _validate_columns(df: pd.DataFrame):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"[metrics] Missing required columns: {missing}")


def _toggle_rate(series: pd.Series) -> float:
    if len(series) <= 1:
        return 0.0
    return (series != series.shift(1)).sum() / (len(series) - 1)


def _false_intervention_rate(
    df: pd.DataFrame,
    decision_col: str,
) -> float:
    """
    False Intervention (battery 기준):
    event_flag == 0 인데 decision == 1
    """
    mask = df["state_valid"] & (df["event_flag"] == 0)
    denom = mask.sum()
    if denom == 0:
        return 0.0
    num = ((df[decision_col] == 1) & mask).sum()
    return num / denom


def _stabilization_rate(
    df: pd.DataFrame,
    decision_col: str,
    window: int = 3,
) -> float:
    """
    Stabilization:
    event_flag == 1 이후 window step 동안 decision == 1 유지
    """
    df = df.sort_values("t").reset_index(drop=True)

    event_indices = df.index[df["event_flag"] == 1].tolist()
    if not event_indices:
        return 0.0

    success = 0
    for idx in event_indices:
        end = idx + window
        if end >= len(df):
            continue
        window_decisions = df.loc[idx:end - 1, decision_col]
        if (window_decisions == 1).all():
            success += 1

    return success / len(event_indices)


def compute_metrics_summary(
    decision_df: pd.DataFrame,
    experiment_id: str,
    domain: str,
) -> Dict:
    """
    Step 7-1 Metrics Summary
    Contract:
      required columns only, decision encoded as 0/1
    """
    _validate_columns(decision_df)

    df = decision_df.copy()

    n_rows_total = len(df)
    n_rows_valid = int(df["state_valid"].sum())

    metrics = {
        "experiment_id": experiment_id,
        "domain": domain,
        "n_rows_total": n_rows_total,
        "n_rows_valid": n_rows_valid,
        # Toggle
        "toggle_rate_raw": _toggle_rate(df["decision_raw"]),
        "toggle_rate_final": _toggle_rate(df["decision_final"]),
        # False intervention
        "false_intervention_rate_raw": _false_intervention_rate(
            df, "decision_raw"
        ),
        "false_intervention_rate_final": _false_intervention_rate(
            df, "decision_final"
        ),
        # Stabilization
        "stabilization_rate_raw": _stabilization_rate(
            df, "decision_raw"
        ),
        "stabilization_rate_final": _stabilization_rate(
            df, "decision_final"
        ),
    }

    return metrics