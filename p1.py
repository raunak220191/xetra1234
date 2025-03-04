##NA removal bulk
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(0)
    else:
        # For non-numeric types, treat them as strings and fill with an empty string.
        df[col] = df[col].fillna("")
