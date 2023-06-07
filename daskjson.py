import os
import dask.dataframe as dd
import pandas as pd

# Specify the directory path
directory_path = "path_to_directory"

# Get the list of JSON files in the directory
json_files = [file for file in os.listdir(directory_path) if file.endswith(".json")]

# Create an empty DataFrame schema
df_schema = pd.DataFrame(columns=["file_name", "page_name", "content"])

# Create a Dask DataFrame
df = dd.from_pandas(df_schema, npartitions=1)

# Iterate through the JSON files and read their contents into the DataFrame
for i, file in enumerate(json_files):
    file_name = os.path.basename(directory_path)
    page_name = str(i + 1)
    file_path = os.path.join(directory_path, file)
    json_data = pd.read_json(file_path)
    
    # Add a new row to the DataFrame
    df = df.append({"file_name": file_name, "page_name": page_name, "content": json_data}, ignore_index=True)

# Compute the Dask DataFrame to get the final result
df = df.compute()
