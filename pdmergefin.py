import pandas as pd
import json

# create a sample DataFrame
cab = pd.DataFrame({
    'Driver ID': ['D001', 'D002', 'D003'],
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [30, 25, 40],
    'City': ['New York', 'San Francisco', 'Los Angeles']
})

# create a new row in the DataFrame to store the JSON data
new_row = pd.Series()

# loop through each column of the DataFrame
for col in cab.columns:
    # create a new list to store the values for the current column
    col_values = []
    # loop through each row of the DataFrame
    for i, row in cab.iterrows():
        # add the value of the current column for the current row to the col_values list
        col_values.append(row[col])
    # convert the col_values list to a JSON string and add it as a new value in the new_row Series
    new_row[col] = json.dumps(col_values)

# append the new_row Series to the cab DataFrame
cab = cab.append(new_row, ignore_index=True)

# print the updated DataFrame
print(cab)
