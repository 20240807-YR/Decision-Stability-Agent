def threshold_v1(state_df, threshold=0.8):
    return (state_df["state_value"] < threshold).astype(int)