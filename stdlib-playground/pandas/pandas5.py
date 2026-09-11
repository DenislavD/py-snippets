# Jupiter Lab: date work, textual data

# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all" # prints all results in cells

# conda install pandas

import pandas as pd
import numpy as np
from pathlib import Path
filepath = Path(__file__).parent / 'z_orders.csv'

# dates. Normally OrderDate: str
df = pd.read_csv(filepath, parse_dates=['OrderDate'])
# Alternatively:
df['OrderDate'] = pd.to_datetime(df['OrderDate'])

df.Category.unique()
df.info()

df.iloc[-1, 6] += pd.Timedelta(days=365*2+60) # add 2 years 2 mo
df.iloc[-1, 6]

date_ = df['OrderDate'] # Series
date_.min(), date_.max()
date_.min() - date_.max()

df['Month'] = df.OrderDate.dt.strftime('%Y-%m') # .dt operator !!
df.tail(3)

df.index
df.set_index('Month', inplace=True) # works only the 1st time
df.index

df.set_index('OrderDate', inplace=True)
df.index.month.unique()

df['2026-01-01':'2026-12-31'] # string parses to datetime, so index works!

# resampling aggregates by date index - SUPERCOOL
monthly_avg = df.resample('MS')['Price'].mean().dropna()
monthly_avg


# string manipulations
df['Product'].str.split(' ').str.get(1).dropna().head()

df[df.CustomerName.str.lower().str.contains('an')]['CustomerName']

df.CustomerName.str.len().max() # or .idxmax()

df['Shipped'].head()
df['Shipped'] = df['Shipped'].replace({'Yes': 1, 'No': 0})
df['Shipped']

# see also str. count(), .endswith(), .get(1), .index(): searches for substring,
# strip()

s = pd.Series([ ["lion", "elephant", "zebra"], ['1', '2',' 3'] ])
s = s.str.join('-') # [lion-elephant-zebra, 1-2- 3]

s.str[:2] # [li, 1-] # or .slice(start, stop, end) , also slice_replace()