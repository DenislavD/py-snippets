# loc/iloc, np.where, assignment, cast, aggregation/groupby
import pandas as pd
import numpy as np
params = pd.read_csv(r'D:\Programming\python\Learning\libraries\z_params.csv')

# select both rows and columns in one go: loc/iloc
cheap_items = params.loc[params['Price per Unit High'] < 18, 'ID'] # ['ID', 'Display Name']
print('\nItems with cost < 18:\n', cheap_items)

rows_5_10_cols_1_2 = params.iloc[5:10, :2] # uses Slice objects
print('\nSpecific rows/cols:\n', rows_5_10_cols_1_2)

# assignment
params.loc[params['Price per Unit High'] < 18, 'ID'] = 'XX.XX'
print('Changed values:')
print(params.loc[params['ID'] == 'XX.XX', ['ID', 'Display Name']].sample(3)) # sample = random

print(params.columns, params.index) # RangeIndex(start=0, stop=564, step=1)

params['$$$'] = np.where(params['Price per Unit Mid'] > 200, 'YES', '')
print(params.tail(10))
print(params.loc[params['$$$'] == 'YES', ['ID', 'Display Name', 'Price per Unit Mid']])


params.rename(columns={ # dict or a Python function like columns=str.lower
    'Price per Unit High': 'ppu_1',
    'Price per Unit Mid': 'ppu_2',
    'Price per Unit Low': 'ppu_3',
}, inplace=True)
print(params.columns)
print(params[['Display Name', 'ppu_1', 'ppu_2', 'ppu_3']])


# cast
params = params.astype({'Row': float})
print(params.dtypes)

print('Mean High price:', params['ppu_1'].mean())
print(params[['ppu_1', 'ppu_2', 'ppu_3']].describe())

# aggregation: groupby (split-apply-combine pattern)
grouped_by_calctype = params[['Calc Type', 'ppu_1', 'ppu_2', 'ppu_3']].groupby('Calc Type').mean()
print('\nAGGREGATION:\n', grouped_by_calctype)
# or (nested with $$$ column as well)  # also .size()=all rows
grouped2 = params.groupby( ['Calc Type', '$$$'] )[ ['ppu_1', 'ppu_2', 'ppu_3'] ].count()
print('\ngrouped2:\n', grouped2)

print(params['Calc Type'].value_counts())
print(params.groupby('Calc Type')['Calc Type'].count()) # same
print(params[['Calc Type', '$$$']].groupby('Calc Type').count()) # same

