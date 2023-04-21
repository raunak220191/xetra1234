import pandas as pd

# create a sample DataFrame
cab = pd.DataFrame({
    'Driver ID': ['D001', 'D002', 'D003'],
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [30, 25, 40],
    'City': ['New York', 'San Francisco', 'Los Angeles']
})

# convert the DataFrame to a dictionary
data_dict = cab.to_dict(orient='records')

# create a new dictionary to store the JSON data
json_data = {}

# loop through each row of the data_dict
for i, row in enumerate(data_dict):
    # loop through each column of the row
    for col in row:
        # check if the column is already in the json_data dictionary
        if col not in json_data:
            json_data[col] = []
        
        # append the value of the column to the corresponding list
        json_data[col].append(row[col])
        
# convert the json_data dictionary to a JSON string
import json
json_string = json.dumps(json_data)

# print the resulting JSON string
print(json_string)
