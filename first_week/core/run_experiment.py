from .experiment_loader import load_experiment
from .state_registry import build_state
from .decision_registry import run_decision
from .guardrail_registry import apply_guardrail


def run_experiment(experiment_id):
    exp = load_experiment(experiment_id)

    state_df = build_state(
        df=exp["df"],
        recipe=exp["state_recipe"],
        domain=exp["domain"],
    )

    decision_raw = run_decision(
        state_df=state_df,
        policy=exp["decision_policy"],
    )

    decision_df = state_df.copy()
    decision_df["decision_raw"] = decision_raw

    guarded_df = apply_guardrail(
        decision_df=decision_df,
        policy=exp["guardrail_policy"],
    )

    return guarded_df


if __name__ == "__main__":
    out = run_experiment("battery_main_long")
    print(out.head())