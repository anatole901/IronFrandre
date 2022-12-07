# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
data = pd.read_excel(r'C:\Users\anato\IRONHACK\IronFrandre\Labs\Module 1\example_data_cleaning.xlsx')
data.drop(labels = ['Department', 'Unnamed: 7', 'Unnamed: 8'], axis = 1, inplace = True)
data.drop(labels = 30, axis = 0, inplace = True)
data.at[28, 'BirthYear'] = 1967
data.at[29, 'BirthYear'] = 1999
data.at[16, 'BirthYear'] = 1967
data['BirthYear'] = data['BirthYear'].apply(int)
data.at[15, 'Profession'] = 'bdm'
data.at[16, 'Profession'] = 'bdm'
data['Profession'] = data['Profession'].apply(lambda x : x.lower())
data.at[1, 'Amount'] = 55250
data.at[26, 'Profession'] = 'student'
data.at[27, 'Profession'] = 'student'
data.at[21, 'Profession'] = 'student'
