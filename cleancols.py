import pandas as pd

def clean_column_names(df):
    # convert column names to lower case
    df.columns = df.columns.str.lower()
    
    # replace special characters with _
    df.columns = df.columns.str.replace('[^\w\s]', '_')
    
    # replace . and - with _
    df.columns = df.columns.str.replace('[.-]', '_')
    
    # find and rename duplicate columns
    counts = df.columns.value_counts()
    duplicates = list(counts[counts > 1].index)
    for dup_col in duplicates:
        indices = [i for i, col in enumerate(df.columns) if col == dup_col]
        for i, idx in enumerate(indices):
            if i == 0:
                df.columns.values[idx] = dup_col
            else:
                df.columns.values[idx] = dup_col + '_' + str(i)
    
    return df
