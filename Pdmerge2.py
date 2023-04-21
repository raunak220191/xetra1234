import pandas as pd

# create a sample DataFrame
cab = pd.DataFrame({
    'Driver ID': ['D001', 'D002', 'D003'],
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [30, 25, 40],
    'City': ['New York', 'San Francisco', 'Los Angeles']
})

# create a list to store the JSON data
json_data = []

# loop through each row of the DataFrame
for i, row in cab.iterrows():
    # create a new dictionary for the current row
    row_dict = {}
    # loop through each column of the row
    for col in cab.columns:
        # add the column name and value to the row_dict dictionary
        row_dict[col] = row[col]
    # append the row_dict dictionary to the json_data list
    json_data.append(row_dict)

# convert the json_data list to a JSON string
import json
json_string = json.dumps(json_data)

# print the resulting JSON string
print(json_string)
