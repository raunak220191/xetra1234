
import pandas as pd
import json

# create a sample DataFrame
cab = pd.DataFrame({
    'Driver ID': ['D001', 'D002', 'D003'],
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [30, 25, 40],
    'City': ['New York', 'San Francisco', 'Los Angeles']
})

# create a new column in the DataFrame to store the JSON data
new_col_name = 'JSON Data'
cab[new_col_name] = pd.Series()

# loop through each row of the DataFrame
for i, row in cab.iterrows():
    # create a new dictionary to store the JSON data for the current row
    json_data = {}
    # loop through each column of the DataFrame
    for col in cab.columns:
        # add the value of the current column for the current row to the json_data dictionary
        json_data[col] = row[col]
    # convert the json_data dictionary to a JSON string and add it as a new value in the new column
    cab.at[i, new_col_name] = json.dumps(json_data)

# print the updated DataFrame
print(cab)
