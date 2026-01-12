from core.decision_rules import threshold_v1

DECISION_POLICIES = {
    "threshold_v1": threshold_v1,
}

def run_decision(state_df, policy):
    return DECISION_POLICIES[policy](state_df)