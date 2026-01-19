from .state_battery import extract_battery_state
from .state_ehr import extract_ehr_state


STATE_RECIPES = {
    "battery_soh_v1": extract_battery_state,
    "ehr_baseline_v1": extract_ehr_state,
}


def build_state(df, recipe, domain=None, window=None):
    """
    Parameters
    ----------
    df : pd.DataFrame
        raw input dataframe
    recipe : str
        state recipe key (from experiments.yaml)
    domain : str, optional
        kept for compatibility / logging (not used for branching)
    window : int, optional
        warm-up / rolling window parameter
    """

    if recipe not in STATE_RECIPES:
        raise ValueError(f"Unknown state recipe: {recipe}")

    extractor = STATE_RECIPES[recipe]

    # window 인자를 받는 extractor만 window 전달
    if window is not None:
        return extractor(df, window=window)

    return extractor(df)