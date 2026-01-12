import numpy as np
import pandas as pd

def compute_trend(series, window=3):
    return series.diff().rolling(window, min_periods=1).mean()

def extract_battery_state(df):
    df = df.sort_values(["battery_id", "cycle"]).copy()

    df["init_capacity"] = (
        df.groupby("battery_id")["QD"]
          .transform(lambda x: x.iloc[0])
    )

    df["state_value"] = df["QD"] / df["init_capacity"]

    df["trend_value"] = (
        df.groupby("battery_id")["state_value"]
          .transform(lambda x: compute_trend(x))
    )

    df["event_flag"] = (df["state_value"] < 0.8).astype(int)

    df["obs_value"] = df["QD"]
    df["entity_id"] = df["battery_id"]
    df["t"] = df["cycle"]

    return df[[
        "entity_id",
        "t",
        "obs_value",
        "state_value",
        "trend_value",
        "event_flag"
    ]]