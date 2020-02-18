%matplotlib inline
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
plt.style.use('ggplot')

orders = pd.read_csv('../data/Orders.csv')
returns = pd.read_csv('../data/Returns.csv')

#1
orders.Profit = orders.Profit.str.replace('[$|,]','')
orders.Profit = pd.to_numeric(orders.Profit)
orders.Sales = orders.Sales.str.replace('[$|,]','')
orders.Sales = pd.to_numeric(orders.Sales)

orders['Order.Date'] = pd.to_datetime(orders['Order.Date'])
orders['Order.Month'] = pd.DatetimeIndex(orders['Order.Date']).month
orders['Order.Year'] = pd.DatetimeIndex(orders['Order.Date']).year

#2.1
orders.groupby(['Order.Month']).agg('sum')['Quantity'].plot.bar()
#2.2
orders.groupby(['Order.Month','Category']).sum()['Quantity'].unstack(1).plot(subplots=True)
for cat, group in orders.groupby(['Category']):
    categories = group.groupby(['Order.Month'])['Quantity'].sum()
    categories.plot(y=orders['Quantity'], label=cat, legend=True)
plt.style.use('fivethirtyeight')

#3.1
returned=pd.merge(orders, returns, left_on = 'Order.ID', right_on = "Order ID", how='inner')
returned.groupby(['Order.Year']).sum()['Profit']
# Order.Year Profit
# 2012   17477.260
# 2013    9269.890
# 2014   17510.630
# 2015   17112.970

#3.2
return_count = returned.groupby('Customer.ID').count()[['Order.ID']].rename(columns={'Order.ID':'Return.Count'})
return_count[return_count['Return.Count']>1].count()  #547 customers have returned more than once.
return_count[return_count['Return.Count']>5].count()  #46 customers have returned more than 5 times.

#3.3
merged=pd.merge(orders, returns, left_on = 'Order.ID', right_on = "Order ID", how='left')
merged['Returned'].fillna('No', inplace = True)

a=merged.loc[merged['Returned']=='Yes'].groupby(['Region_x','Returned'])[['Order.ID']].count().rename(columns={"Order.ID":"Count"})
b=merged.groupby(['Region_x'])[['Order.ID']].count().rename(columns={"Order.ID":"Total.Count"})
comb=pd.merge(a,b,on='Region_x')
comb['Return.Prop']=comb['Count']/comb['Total.Count']
comb.sort_values(by='Return.Prop',ascending=False)
# 	Count	Total.Count	Return.Prop
# Region_x			
# Western US	177	3203	0.055
# Eastern Asia	131	2374	0.055
# Southern Europe	112	2113	0.053
# Southern Africa	25	478	0.052
# Southern US	83	1620	0.051
# Eastern US	134	2848	0.047
# Southeastern Asia	140	3129	0.045
# South America	133	2988	0.045
# Western Asia	108	2440	0.044
# Oceania	154	3487	0.044
# Central America	248	5616	0.044
# Southern Asia	111	2655	0.042
# Central Asia	9	217	0.041
# Western Africa	60	1460	0.041
# Caribbean	69	1690	0.041
# North Africa	51	1278	0.040
# Western Europe	233	5883	0.040
# Canada	15	384	0.039
# Northern Europe	76	2204	0.034
# Central US	74	2323	0.032
# Eastern Europe	42	1529	0.027
# Central Africa	17	643	0.026
# Eastern Africa	18	728	0.025

#3.4
a=merged.loc[merged['Returned']=='Yes'].groupby(['Category','Returned'])[['Order.ID']].count().rename(columns={"Order.ID":"Count"})
b=merged.groupby(['Category'])[['Order.ID']].count().rename(columns={"Order.ID":"Total.Count"})
comb=pd.merge(a,b,on='Category')
comb['Return.Prop']=comb['Count']/comb['Total.Count']
comb.sort_values(by='Return.Prop', ascending=False)

# 	Count	Total.Count	Return.Prop
# Category			
# Technology	445	10141	0.044
# Furniture	427	9860	0.043
# Office Supplies	1348	31289	0.043

# 4.1 already done above with 'Returned' column.

# 4.2
merged['Ship.Date']=pd.to_datetime(merged['Ship.Date'])
merged['Order.Date']=pd.to_datetime(merged['Order.Date'])
merged['Process.Time']=(merged['Ship.Date']-merged['Order.Date']).dt.days

#4.3
returned_prod=merged.loc[merged['Returned']=='Yes'].groupby('Product.ID').count()[['Order.ID']]
pd.merge(merged,returned_prod,on='Product.ID',how='left').rename(columns=({'Order.ID_y':'Prod.Return.Count'})).fillna(0)

