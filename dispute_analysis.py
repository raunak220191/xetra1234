import pandas as pd
import numpy as np
import os
import warnings
import datetime

# suppress any warnings (optional)
warnings.filterwarnings('ignore')

# --- Input Data ---
input_file = os.path.join('input', 'IT Input.xlsx')
# pandas 0.23.0 supports sheet_name; if you were on < 0.21 use sheetname='Input'
df = pd.read_excel(input_file, sheet_name='Input')
print("Original dimensions of input file:", df.shape)

# --- Key & Prep ---
# build your composite key
df['Key1'] = df['Mnemonic'] + '-' + df['CSA Type'] + '-' + df['Margin Call Issuer']
# absolute value of age
df['Cumulative Age'] = df['Cumulative Age'].abs()
# capture only resolved amounts
df['Resolved'] = np.where(df['Status'] == 'Resolved', df['in mm$'], 0)

# --- Aggregation (pandas 0.23 style) ---
grp = df.groupby('Key1')

total_disp    = grp['in mm$'].sum()
highest_disp  = grp['in mm$'].max()
avg_disp_amt  = grp['in mm$'].mean()
avg_disp_age  = grp['Cumulative Age'].mean()
count_disp    = grp['Cumulative Age'].count()
avg_resolved  = grp['Resolved'].mean()

# stitch them together
data_output = pd.concat([
    total_disp,
    highest_disp,
    avg_disp_amt,
    avg_disp_age,
    count_disp,
    avg_resolved
], axis=1)

data_output.columns = [
    'Total_Disp_Val',
    'Highest_Disp_Val',
    'Avg_Disp_Amt',
    'Avg_Disp_Age',
    'No_of_times_occured',
    'Avg_Resolved_Dispute_Amt'
]

# round to 2 decimals
data_output = data_output.round(2)

# bring Key1 back as a column
data_output = data_output.reset_index()

print("After data processing dimensions of output:", data_output.shape)
print(data_output.head())

# --- Write Output ---
# ensure output folder exists
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

current_time = datetime.datetime.now().strftime("%d-%b-%Y %H:%M")
output_path = os.path.join(output_dir, f'dispute_summary_{current_time}.xlsx')

data_output.to_excel(output_path, index=False)
print("Wrote:", output_path)