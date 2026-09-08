# str.func, ~ negation, drops, pd.concat, pd.merge (SQL-like)
import pandas as pd
df = pd.read_csv('z_orders.csv')

print('\nFirst 5:\n', df[:5])
print('\nFirst row:\n', list( df.iloc[0] )) # first row

cust_with_a = df[ df['CustomerName'].str.startswith('A') ]
print('\nName starting with A:\n', cust_with_a.head())

cust_not_in = df[ ~df['Country'].isin(['USA', 'Canada']) ] # ~ = negation
print('\nNot USA or Canada:\n', cust_not_in.head())

print('\nAnna only:\n', df[df['CustomerName'] == 'Anna Ivanova'])

# deletions
df = df.drop(0) # drops row 0
df = df.drop(2, axis=0) # Drop row with index 2
df = df[df['CustomerName'] != 'Alice Wong'] # Drop rows where name == Alice Wong
df = df.drop('Shipped', axis=1) # Drop 'Shipped' column

print('\nAll (with some deleted):\n', df)


# insertions / concatenate
new_record = dict(OrderID=1111, CustomerName='Dadi', Product='PC', Category='Electronics',
    Quantity=0, Price=2400, OrderDate='2026-09-08', Shipped='No', Country='Bulgaria')

print('Shape:', df.shape)
df2 = pd.DataFrame(new_record, [39]) # scalar values dict, not column:list values, needs Index
# keys is optional, provides hierarchical row index
df = pd.concat([df, df2], keys=['Initial', 'New'])
print('Shape:', df.shape, '# adds the Shipped column too with NaN (passes isna)\n')
print(df.tail(3), '\n')

# turns the hierarchical Initial/New index to a plain column. If no level: resets ALL
df = df.reset_index(level=0) 
print(df.tail(3))


# merge / vlookup / SQL joins
continents = {
    'CustomerName': ['Anna Ivanova', 'Dadi', 'Carlos Santos'],
    'Continent': ['North America', 'Europe', 'Africa'],
}
continents_df = pd.DataFrame(continents)
print(continents_df)

# use left_on= and right_on= if the connecting column name is different
merged = pd.merge(df, continents_df, how='left', on='CustomerName')
print('\nMerged:\n', merged.tail())








