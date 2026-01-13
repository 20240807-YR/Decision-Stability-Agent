def stability_v1(decision_df, min_hold=3):
    df = decision_df.sort_values(["entity_id", "t"]).copy()

    final = []
    last = None
    streak = 0

    for d in df["decision_raw"].tolist():
        if last is None:
            last = d
            streak = 1
            final.append(d)
            continue

        if d == last:
            streak += 1
            final.append(d)
        else:
            if streak >= min_hold:
                last = d
                streak = 1
                final.append(d)
            else:
                final.append(last)
                streak += 1

    df["decision_final"] = final
    return df


GUARDRAIL_POLICIES = {
    "stability_v1": stability_v1,
}

def apply_guardrail(decision_df, policy):
    if policy not in GUARDRAIL_POLICIES:
        raise ValueError(f"Unknown guardrail policy: {policy}")
    return GUARDRAIL_POLICIES[policy](decision_df)