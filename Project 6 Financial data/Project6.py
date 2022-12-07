# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 09:27:06 2022

@author: anato
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

financial = pd.read_csv(r"C:\Users\anato\Documents\IRONHACK\IronFrandre\Project 6 Financial data\cdp_financial_data.csv")

financial.isna().sum()

financial.info()

financial['Ticker'].unique().shape

test = financial['Revenue'] + financial['Cost of Revenue'] + financial['Operating Expenses'] - financial['Operating Income (Loss)']

test3 = financial['Operating Income (Loss)'] + financial['Depreciation & Amortization'] - financial['EBITDA']

correlation = financial[['EBITDA', 'Revenue', 'Cost of Revenue', 'Operating Income (Loss)', 'Operating Expenses', 'Depreciation & Amortization']].corr()

sns.heatmap(correlation, xticklabels=correlation.columns, yticklabels=correlation.columns)

rev_income_rel = financial['Revenue']/financial['Operating Income (Loss)']
costr_income_rel = financial['Cost of Revenue']/financial['Operating Income (Loss)']

ratio = rev_income_rel.median()
ratio2 = costr_income_rel.median()

financial.loc[financial['Cost of Revenue'].isna(), 'Cost of Revenue'] = financial.loc[financial['Cost of Revenue'].isna(), 'Operating Income (Loss)'] - financial.loc[financial['Cost of Revenue'].isna(), 'Revenue'] - financial.loc[financial['Cost of Revenue'].isna(), 'Operating Expenses']
financial.loc[financial['Depreciation & Amortization'].isna(), 'Depreciation & Amortization'] = financial.loc[financial['Depreciation & Amortization'].isna(), 'EBITDA'] - financial.loc[financial['Depreciation & Amortization'].isna(), 'Operating Income (Loss)']
financial.loc[financial['Operating Expenses'].isna(), 'Operating Expenses'] = financial.loc[financial['Operating Expenses'].isna(), 'Operating Income (Loss)'] - financial.loc[financial['Operating Expenses'].isna(), 'Revenue'] - financial.loc[financial['Operating Expenses'].isna(), 'Cost of Revenue']
financial.loc[financial['Revenue'].isna(), 'Revenue'] = financial.loc[financial['Revenue'].isna(), 'Operating Income (Loss)'] * ratio
financial.loc[financial['Cost of Revenue'].isna(), 'Cost of Revenue'] = financial.loc[financial['Cost of Revenue'].isna(), 'Operating Income (Loss)'] - financial.loc[financial['Cost of Revenue'].isna(), 'Revenue'] - financial.loc[financial['Cost of Revenue'].isna(), 'Operating Expenses']
financial.loc[financial['Cost of Revenue'].isna(), 'Cost of Revenue'] = financial.loc[financial['Cost of Revenue'].isna(), 'Operating Income (Loss)'] * ratio2
financial.loc[financial['Operating Expenses'].isna(), 'Operating Expenses'] = financial.loc[financial['Operating Expenses'].isna(), 'Operating Income (Loss)'] - financial.loc[financial['Operating Expenses'].isna(), 'Revenue'] - financial.loc[financial['Operating Expenses'].isna(), 'Cost of Revenue']
financial.loc[(financial['Revenue'] + financial['Cost of Revenue'] + financial['Operating Expenses'] - financial['Operating Income (Loss)'] != 0), 'Operating Expenses'] = financial.loc[(financial['Revenue'] + financial['Cost of Revenue'] + financial['Operating Expenses'] - financial['Operating Income (Loss)'] != 0), 'Operating Income (Loss)'] - financial.loc[(financial['Revenue'] + financial['Cost of Revenue'] + financial['Operating Expenses'] - financial['Operating Income (Loss)'] != 0), 'Revenue'] - financial.loc[(financial['Revenue'] + financial['Cost of Revenue'] + financial['Operating Expenses'] - financial['Operating Income (Loss)'] != 0), 'Cost of Revenue']

financial.drop(axis = 0, index = financial.loc[financial['Revenue'].isna()].index, inplace = True)


tickers = list(financial['Ticker'].unique())

for t in tickers :
    if financial.loc[(financial['Ticker'] == t) & (financial['organization'].notna()), 'organization'].shape[0] > 0 :
        name = financial.loc[(financial['Ticker'] == t) & (financial['organization'].notna()), 'organization'].mode()[0]
        financial.loc[(financial['Ticker'] == t) & (financial['organization'].isna()), 'organization'] = name
        
for t in tickers :
    if financial.loc[(financial['Ticker'] == t) & (financial['primary_questionnaire_sector'].notna()), 'primary_questionnaire_sector'].shape[0] > 0 :
        name = financial.loc[(financial['Ticker'] == t) & (financial['primary_questionnaire_sector'].notna()), 'primary_questionnaire_sector'].mode()[0]
        financial.loc[(financial['Ticker'] == t) & (financial['primary_questionnaire_sector'].isna()), 'primary_questionnaire_sector'] = name

for t in tickers :
    if financial.loc[(financial['Ticker'] == t) & (financial['primary_industry'].notna()), 'primary_industry'].shape[0] > 0 :
        name = financial.loc[(financial['Ticker'] == t) & (financial['primary_industry'].notna()), 'primary_industry'].mode()[0]
        financial.loc[(financial['Ticker'] == t) & (financial['primary_industry'].isna()), 'primary_industry'] = name

for t in tickers :
    if financial.loc[(financial['Ticker'] == t) & (financial['account_number'].notna()), 'account_number'].shape[0] > 0 :
        name = financial.loc[(financial['Ticker'] == t) & (financial['account_number'].notna()), 'account_number'].mode()[0]
        financial.loc[(financial['Ticker'] == t) & (financial['account_number'].isna()), 'account_number'] = name

for t in tickers :
    if financial.loc[(financial['Ticker'] == t) & (financial['authority_types'].notna()), 'authority_types'].shape[0] > 0 :
        name = financial.loc[(financial['Ticker'] == t) & (financial['authority_types'].notna()), 'authority_types'].mode()[0]
        financial.loc[(financial['Ticker'] == t) & (financial['organization'].isna()), 'authority_types'] = name

for t in tickers :
    if financial.loc[(financial['Ticker'] == t) & (financial['sectors'].notna()), 'sectors'].shape[0] > 0 :
        name = financial.loc[(financial['Ticker'] == t) & (financial['sectors'].notna()), 'sectors'].mode()[0]
        financial.loc[(financial['Ticker'] == t) & (financial['sectors'].isna()), 'sectors'] = name

