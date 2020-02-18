import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
plt.style.use('fivethirtyeight')
import seaborn as sns
import re

##################################################################
############################ Part I ##############################
##################################################################

# Importing the raw data as Orders
raw_orders = pd.read_csv('../data/Orders.csv')
raw_returns = pd.read_csv('../data/Returns.csv')

# Visually exploring the data/columns
pd.options.display.max_columns = None
raw_orders.head()
raw_orders.dtypes

orders = raw_orders.copy()

######################
# Problem 1
######################

orders['Sales'] = pd.to_numeric(orders['Sales'].str.replace('[$|,]', ""))
orders['Profit'] = pd.to_numeric(orders['Profit'].str.replace('[$|,]', ""))

######################
# Problem 2
######################
## 1. Is there any seasonal trend of inventory in the company?

# Isolate order month into its own column as a proxy for seasons
orders['Order.Date'] = pd.to_datetime(orders['Order.Date'])
orders['Order.Month'] = pd.DatetimeIndex(orders['Order.Date']).month
# Group dataframe by month
orders.groupby('Order.Month').sum()['Quantity'].plot.bar()
# There seems to be a spike in inventory at the beginning of the summer, as well as in the 
# fall and early winter. There's a fall in inventory in the new year and in mid-summer.

## 2. Is the seasonal trend the same for different categories?
for cat, group in orders.groupby(['Category']):
    categories = group.groupby(['Order.Month'])['Quantity'].sum()
    categories.plot(y=orders['Quantity'], label=cat, legend=True)
# The inventory trend seems to be the same across categories, although the scale in 
# number of orders is totally different (there are far more office supplies ordered than 
# any other category, for example). However, the trend is more pronounced for Office
# Supplies.


######################
# Problem 3
######################

# Merge Returns and Orders dataset
returns = raw_returns.copy()
returns.rename(columns={"Order ID": "Order.ID"}, inplace = True)
orders_returns = pd.merge(orders, returns[['Order.ID','Returned']], how = "left", on = "Order.ID", )
orders_returns['Returned'].fillna('0', inplace = True)
orders_returns['Returned'].replace('Yes', 1, inplace = True)
orders_returns['Returned'].replace('No', 0, inplace = True)
orders_returns['Order.Year'] = pd.DatetimeIndex(orders['Order.Date']).year

## 1. How much profit did we lose due to returns each year?
orders_returns.loc[orders_returns['Returned']=='Yes'].groupby('Order.Year')['Profit'].sum()

# 2012    $17,477.26 lost due to returns
# 2013    $9269.89 lost due to returns
# 2014    $17,510.63 lost due to returns
# 2015    $17,112.97 lost due to returns

## 2. How many customers returned more than once? more than 5 times?
temp = orders_returns.loc[orders_returns['Returned']==1].groupby('Customer.ID')[['Customer.ID']].count()
len(temp[temp['Customer.ID']>1])
# 547 customers returned more than once
len(temp[temp['Customer.ID']>5])
# 46 customers returned more than five times

## 3. Which regions are more likely to return orders?
temp2 = orders_returns.groupby('Region').agg({'Returned':'sum', 'Order.ID':'count'})
temp2['Proportion'] = temp2['Returned']/temp2['Order.ID']*100
temp2.sort_values('Proportion', ascending = False)
# Western US, Eastern Asia, Southern Euriope, Southern Africa, and the Southern US
# all have return rates of over 5% of total orders.

## 4. Which categories (sub-categories) of products are more likely to be returned?
temp3 = orders_returns.groupby(['Category','Sub.Category']).agg({'Returned':'sum', 'Order.ID':'count'})
temp3['Proportion'] = temp3['Returned']/temp3['Order.ID']*100
temp3.sort_values(['Category','Proportion'], ascending = False)
# Within Technology, Accessories have the highest return rate (4.49%).
# Within Office Supplies, Labels have the highest return rate (5.27%).
# Within Furniture, Tables have the highest return rate (4.76%).
temp4 = orders_returns.groupby(['Category']).agg({'Returned':'sum', 'Order.ID':'count'})
temp4['Proportion'] = temp4['Returned']/temp4['Order.ID']*100
temp4.sort_values(['Category','Proportion'], ascending = False)
# Overall, Technology has the highest return rate, at 4.39%


##################################################################
############################ Part II #############################
##################################################################

######################
# Problem 4
######################

## Step 1: 
df = orders_returns.copy()
df['Returned'].replace(1, "Yes", inplace = True)
df['Returned'].replace(0, "No", inplace = True)

## Step 2:
df['Ship.Date'] = pd.to_datetime(df['Ship.Date'])
df['Process.Time'] = (df['Ship.Date']-df['Order.Date']).dt.days

# Step 3:
df = pd.merge(df, returned_products, on = "Product.ID", how = "left").rename(columns = {"Returned_y": "Returned.Count"}).fillna(0)

######################
# Problem 5
######################
reg_df = df['Order.ID']


