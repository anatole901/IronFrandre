# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:05:11 2022

@author: anato
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder

data = pd.read_excel(r'C:\Users\anato\IRONHACK\IronFrandre\Project 3 Data cleaning\9 - Superstore.xls')
data.info()
data.loc[data['Customer Name'].isna()]
missing_name_ID = list(data.loc[data['Customer Name'].isna(), 'Customer ID'].unique())
data.loc[data['Customer ID'].isin(missing_name_ID), ['Customer ID', 'Customer Name']]
for customer in missing_name_ID :
    name_customer = data.loc[(data['Customer ID'] == customer) & (data['Customer Name'].notna()), 'Customer Name'].mode()
    data.loc[data['Customer ID'] == customer, 'Customer Name'] = str(name_customer)
data.info()

missing_segment_ID = list(data.loc[data['Segment'].isna(), 'Customer ID'].unique())
data.loc[data['Customer ID'].isin(missing_segment_ID), ['Customer ID', 'Segment']]
for customer in missing_segment_ID :
    customer_segment = data.loc[(data['Customer ID'] == customer) & (data['Segment'].notna()), 'Segment'].mode()
    data.loc[(data['Customer ID'] == customer) & (data['Segment'].isna()), 'Segment'] = str(customer_segment)
data.info()

missing_city_state = list(data.loc[data['City'].isna(), 'State'].unique())
data.loc[data['State'].isin(missing_city_state), ['City', 'State']]
for state in missing_city_state :
    new_city = data.loc[(data['State'] == state) & (data['City'].notna()), 'City'].mode()
    data.loc[(data['State'] == state) & (data['City'].isna()), 'City'] = str(new_city)
data.info()
    
average_amount_to_profit = (data.loc[(data['Sales'].notna()) & (data['Profit'] != 0), 'Sales'] / data.loc[(data['Sales'].notna()) & (data['Profit'] != 0), 'Profit'].apply(abs)).mean()
data.loc[data['Sales'].isna(), 'Sales'] = abs(data.loc[data['Sales'].isna(), 'Profit']) * average_amount_to_profit
data.info()

data.loc[(data['Quantity'] > 15) | (data['Discount'] > 1), ['Row ID', 'Quantity', 'Discount']]
data.loc[data['Row ID'] == 1434, 'Quantity'] = 14
data.loc[data['Row ID'] == 1434, 'Discount'] = 0.5
data.loc[data['Row ID'] == 1712, 'Discount'] = 0.2

data.drop('Country', axis = 1, inplace = True)

data['Ship Mode Encoded'] = LabelEncoder().fit_transform(data['Ship Mode'])
data['Region Encoded'] = LabelEncoder().fit_transform(data['Region'])
data[['Row ID', 'Ship Mode', 'Ship Mode Encoded']].head(20)

data.to_csv(r'C:\Users\anato\IRONHACK\IronFrandre\Project 3 Data cleaning\Superstore.csv')
