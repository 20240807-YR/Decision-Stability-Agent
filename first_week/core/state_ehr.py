import numpy as np
import pandas as pd

def compute_trend(series, window=3):
    return series.diff().rolling(window, min_periods=1).mean()

def extract_ehr_state(df):
    df = df.sort_values(["patient_id", "day"]).copy()
    df = df.rename(columns={"day": "t"})

    df["baseline"] = (
        df.groupby("patient_id")["heart_rate"]
          .transform(lambda x: x.iloc[:5].mean())
    )

    df["state_value"] = (
        (df["heart_rate"] - df["baseline"]).abs()
        / df["baseline"]
    )

    df["trend_value"] = (
        df.groupby("patient_id")["state_value"]
          .transform(lambda x: compute_trend(x))
    )

    df["event_flag"] = (df["state_value"] > 0.3).astype(int)

    df["obs_value"] = df["heart_rate"]
    df["entity_id"] = df["patient_id"]

    return df[[
        "entity_id",
        "t",
        "obs_value",
        "state_value",
        "trend_value",
        "event_flag"
    ]]