import numpy as np
import pandas as pd


def compute_trend(series, window=3):
    return series.diff().rolling(window, min_periods=1).mean()


def extract_ehr_state(df, window=None, baseline_window=5):
    """
    window:
      - None  : 기존 방식 (baseline 고정)
      - int   : warm-up 구간 명시 (rolling baseline)
    """
    df = df.sort_values(["patient_id", "day"]).copy()
    df = df.rename(columns={"day": "t"})

    df["obs_value"] = df["heart_rate"]
    df["entity_id"] = df["patient_id"]

    df["state_value"] = np.nan

    if window is None:
        df["baseline"] = (
            df.groupby("patient_id")["heart_rate"]
              .transform(lambda x: x.iloc[:baseline_window].mean())
        )

        df["state_value"] = (
            (df["heart_rate"] - df["baseline"]).abs()
            / df["baseline"]
        )

    else:
        for pid, g in df.groupby("patient_id"):
            idx = g.index
            for i in range(window, len(idx)):
                baseline = g.loc[idx[i-window:i-1], "heart_rate"].mean()
                if baseline == 0 or np.isnan(baseline):
                    continue
                df.loc[idx[i], "state_value"] = (
                    abs(df.loc[idx[i], "heart_rate"] - baseline) / baseline
                )

    df["state_valid"] = df["state_value"].notna()

    df["trend_value"] = (
        df.groupby("patient_id")["state_value"]
          .transform(lambda x: compute_trend(x))
    )
    df.loc[~df["state_valid"], "trend_value"] = np.nan

    df["event_flag"] = 0
    df.loc[df["state_valid"], "event_flag"] = (
        df.loc[df["state_valid"], "state_value"] > 0.3
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