from .state_battery import extract_battery_state
from .state_ehr import extract_ehr_state

STATE_RECIPES = {
    "battery_soh_v1": extract_battery_state,
    "ehr_baseline_v1": extract_ehr_state,
}

def build_state(df, recipe, domain):
    if recipe not in STATE_RECIPES:
        raise ValueError(f"Unknown state recipe: {recipe}")
    return STATE_RECIPES[recipe](df)