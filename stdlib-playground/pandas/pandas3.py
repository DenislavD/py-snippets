# sort, pivot, pivot_table, melt(unpivot)
import pandas as pd
import numpy as np
params = pd.read_csv(r'D:\Programming\python\Learning\libraries\z_params.csv',
    index_col='Row')

sorted_one = params.sort_values(by='Price per Unit High', ascending=False)
print(sorted_one[['ID', 'Display Name', 'Price per Unit High']].head())

sorted_two = params.sort_values(by=['Price per Unit High', 'Row'])
print(sorted_two[['ID', 'Display Name', 'Price per Unit High']].head())


# filter for AGGREGATION rows only
params['bracket'] = params.ID.apply(lambda x: x[:5]) # first 5 chars
agg_data = params[params['Calc Type'] == 'AGGREGATION']

# get 3 measurements (head) for each bracket
datatype_subset = agg_data.sort_index().groupby(['bracket']).head(3)
print('\n3 for each:\n', datatype_subset[['ID', 'Display Name', 'Calc Type', 'bracket']])


# pivot - restructuring only
pivot = params.pivot(columns='Calc Type', values='Display Name').sample(10)
print('\npivot:\n', pivot) # by default the rows are the index
# pivot_table (+ aggregation)
pivot2 = params.pivot_table(columns='Calc Type', index='bracket', 
    values='Price per Unit High', aggfunc='mean', margins=True) # adds 'All' column
print('\npivot_table with aggfunc and total:\n', pivot2)


# wide to long (unpivot)
flattened = pivot.reset_index() # index 'Row' becomes a column (ungroups)
print('\nInitial pivot:\n', pivot)
print('\nFlattened:\n', flattened)

unpivoted = flattened.melt(id_vars='Row', value_name='Display Name')
print('\nUnpivoted All:\n', unpivoted)
print('\nUnpivoted:\n', unpivoted[unpivoted['Display Name'].notna()])


