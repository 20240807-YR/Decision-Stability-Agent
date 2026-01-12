from core.guardrails import stability_v1

GUARDRAIL_POLICIES = {
    "stability_v1": stability_v1,
}

def apply_guardrail(decision_df, policy):
    return GUARDRAIL_POLICIES[policy](decision_df)