# basic info and access, filter
import pandas as pd # installed globally on local

# A DataFrame is a 2-dimensional DS with 0-based index, label (headers), rows and cols.
df = pd.DataFrame({
    'Name': ['Jodi', 'Cary', 'Bardo'],
    'Age': [16, 230, 666],
    'Gender': ['f', 'f', 'm'],
})

print(df)
print(type(df['Age'])) # <class 'pandas.Series'>
print(df['Age']) # A Series is a column.
print(type(df['Age'][1]), df['Age'][1] + 1) # <class 'numpy.int64'>

print(f"Max age: {df['Age'].max()}")
print(df.describe())

# pd.read_ (csv, excel, sql, json, parquet, …)
params = pd.read_csv(r'D:\Programming\python\Learning\libraries\z_params.csv')
print(params.head(5)) # head = first n, tail = last
# print(params.dtypes)

# pd.to_ (excel, ..) - store the data
# params.to_excel('params.xlsx', sheet_name='Params', index=False) # no header row

print(params.info()) # non-null count, also includes data type, RAM!

ids = params['ID']
print(type(ids), ids.shape) # Series with 1-tuple shape

ids_names = params[['ID', 'Display Name', 'Price per Unit High']]
print(ids_names.head(15)) # [:15]
print(type(ids_names), ids_names.shape) # DataFrame with no. of rows/cols tuple, uses NymPy's darray I guess

# comparison filter
filter_series = ids_names['Price per Unit High'] < 30 # -> Series(True, False, False..)
high_prices = ids_names[filter_series] # we can use the above to filter like in SUMPRODUCT
print(high_prices)

# remove blanks filter
with_prices = ids_names[ids_names['Price per Unit High'].notna()]
print(with_prices)

# combined
filter_ = (params['ID'] == '01.01.05.01') | (params['ID'] == '01.01.08.01')
filter_ = params['ID'].isin(['01.01.05.01', '01.01.09.01']) # alternative
selected_params = ids_names[filter_]
print(selected_params)
