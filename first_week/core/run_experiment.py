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

    decision_df = run_decision(
        state_df,
        policy=exp["decision_policy"]
    )

    guarded_df = apply_guardrail(
        decision_df,
        policy=exp["guardrail_policy"]
    )

    return {
        "experiment_id": experiment_id,
        "domain": exp["domain"],
        "state": state_df,
        "decision": decision_df,
        "guarded": guarded_df,
    }