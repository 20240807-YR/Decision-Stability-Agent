import numpy as np


def threshold_v1(state_df, threshold=0.8):
    """
    Decision rule:
    - state_valid == True 인 구간만 판단
    - warm-up / invalid 구간은 무조건 0
    """

    decision = np.zeros(len(state_df), dtype=int)

    if "state_valid" not in state_df.columns:
        raise ValueError("state_df must contain 'state_valid' column")

    valid_mask = state_df["state_valid"] == True

    decision[valid_mask] = (
        state_df.loc[valid_mask, "state_value"] < threshold
    ).astype(int)

    return decision


DECISION_POLICIES = {
    "threshold_v1": threshold_v1,
}


def run_decision(state_df, policy, **kwargs):
    if policy not in DECISION_POLICIES:
        raise ValueError(f"Unknown decision policy: {policy}")

    return DECISION_POLICIES[policy](state_df, **kwargs)