from .decision_rules import threshold_v1

DECISION_POLICIES = {
    "threshold_v1": threshold_v1,
}

def run_decision(state_df, policy):
    if policy not in DECISION_POLICIES:
        raise ValueError(f"Unknown decision policy: {policy}")
    return DECISION_POLICIES[policy](state_df)