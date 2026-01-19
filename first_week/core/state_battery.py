import numpy as np
import pandas as pd

def compute_trend(series, window=3):
    return series.diff().rolling(window, min_periods=1).mean()


def extract_battery_state(df, window=None):
    """
    window:
      - None  : 기존 방식 (init_capacity 기준)
      - int   : warm-up window 이후부터 state 계산
    """
    df = df.sort_values(["battery_id", "cycle"]).copy()

    df["obs_value"] = df["QD"]
    df["entity_id"] = df["battery_id"]
    df["t"] = df["cycle"]

    df["state_value"] = np.nan

    if window is None:
        # 기존 방식
        df["init_capacity"] = (
            df.groupby("battery_id")["QD"]
              .transform(lambda x: x.iloc[0])
        )
        df["state_value"] = df["QD"] / df["init_capacity"]

    else:
        # warm-up 이후 rolling baseline
        for bid, g in df.groupby("battery_id"):
            idx = g.index
            for i in range(window, len(idx)):
                baseline = g.loc[idx[i-window:i-1], "QD"].mean()
                if baseline == 0 or np.isnan(baseline):
                    continue
                df.loc[idx[i], "state_value"] = baseline / df.loc[idx[i], "QD"]

    df["state_valid"] = df["state_value"].notna()

    df["trend_value"] = (
        df.groupby("battery_id")["state_value"]
          .transform(lambda x: compute_trend(x))
    )
    df.loc[~df["state_valid"], "trend_value"] = np.nan

    df["event_flag"] = 0
    df.loc[df["state_valid"], "event_flag"] = (
        df.loc[df["state_valid"], "state_value"] < 0.8
    ).astype(int)

    return df[
        [
            "entity_id",
            "t",
            "obs_value",
            "state_value",
            "trend_value",
            "event_flag",
            "state_valid",
        ]
    ]