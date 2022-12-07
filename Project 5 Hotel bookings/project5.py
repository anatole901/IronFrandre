# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 09:30:07 2022

@author: anato
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
from math import pi

booking = pd.read_csv(r"C:\Users\anato\Documents\IRONHACK\IronFrandre\Project 5 Hotel bookings\hotel_booking.csv")
booking.info()
booking.isna().sum()
booking.drop(['company', 'is_canceled', 'phone-number', 'credit_card'], axis = 1, inplace = True)
booking.loc[booking['country'].isna(), 'country'] = 'PRT'
booking.at[48515, 'adr'] = 540
booking.loc[(booking['market_segment'] == 'Direct') & (booking['distribution_channel'] == 'Corporate'), ['market_segment', 'distribution_channel']] = ['Corporate', 'Direct']
booking.loc[(booking['market_segment'] == 'Direct') & (booking['distribution_channel'] == 'Undefined'), 'distribution_channel'] = 'Direct'
booking.loc[booking['distribution_channel'] == 'Undefined', 'distribution_channel'] = 'TA/TO'
booking.loc[booking['market_segment'] == 'Undefined', 'market_segment'] = 'Online TA'
booking.loc[booking['meal'] == 'Undefined', 'meal'] = 'BB'
booking.loc[(booking['adults'] + booking['children']) == 0, 'adults'] = 2

freq_clients = pd.DataFrame(booking['email'].value_counts())
occasionnal = list(freq_clients.loc[freq_clients['email'] == 1].index)
regular = list(freq_clients.loc[freq_clients['email'] != 1].index)

st.title('Project 5 : Streamlit dashboard')
st.text("""Hotel bookings
François-Régis André
Monday October 14th 2022

This dashboard will present some statistics about the bookings of an hotel
group present mostly in Europe. The covered time period is 2015 to 2017.""")
st.header("Parameters")
st.text("""First, select the parameters that will define what data you want to show.
Please keep in mind that if you do not fill a field, then all available data
for that field will be used. Select your parameters on the side of the screen.""")
years = st.sidebar.multiselect('Select the years', [2015, 2016, 2017])
if years != [] :
    booking = booking.loc[booking['arrival_date_year'].isin(years)]
all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
months = st.sidebar.multiselect('Select the months', all_months)
if months != [] :
    booking = booking.loc[booking['arrival_date_month'].isin(months)]
meal = st.sidebar.multiselect('Select the option for meals', ['BB', 'HB', 'FB', 'SC'])
if meal != [] :
    booking = booking.loc[booking['meal'].isin(meal)]
customer_type = st.sidebar.multiselect('Select the customer type', ['Transient', 'Transient-Party', 'Group', 'Contract'])
if customer_type != [] :
    booking = booking.loc[booking['customer_type'].isin(customer_type)]
hotel = st.sidebar.multiselect('Select the location of the hotel', ['City Hotel', 'Resort Hotel'])
if len(hotel) == 1 :
    booking = booking.loc[booking['hotel'] == hotel[0]]
freq = st.sidebar.multiselect('Select regular or occasionnal clients', ['Regular', 'Occasionnal'])
if freq == ['Regular'] :
    booking = booking.loc[booking['email'].isin(list(regular))]
elif freq == ['Occasionnal']:
    booking = booking.loc[booking['email'].isin(list(occasionnal))]
success = st.sidebar.multiselect('Choose the status of the sale', ['Successful', 'Unsuccessful'])
if success == ['Successful'] :
    booking = booking.loc[booking['reservation_status'] == 'Check-Out']
elif success == ['Unsuccessful']:
    booking = booking.loc[booking['reservation_status'].isin(['Canceled', 'No-Show'])]


st.header('Global statistics')
amount = pd.DataFrame(booking['adr'] * (booking['stays_in_week_nights'] + booking['stays_in_week_nights']))
st.text(f"""For the data we considered, the average amount spent for a booking is
€{int(amount[0].mean())} and the median is €{int(amount[0].median())}. For non-free bookings,
the mean is €{int(amount.loc[amount[0] > 0, 0].mean())} and the median is €{int(amount.loc[amount[0] > 0, 0].median())}.
The average cost by night is €{int(booking['adr'].mean())} and the median is €{int(booking['adr'].median())}.
For non-free bookings, the mean is €{int(booking.loc[booking['adr'] > 0, 'adr'].mean())} and the median is €{int(booking.loc[booking['adr'] > 0, 'adr'].median())}.""")



fig2, ax2 = plt.subplots()
chart2 = booking.groupby(by = 'reservation_status', as_index = False).count().sort_values(by = 'name')
ax2.pie(chart2['name'], labels = chart2['reservation_status'], autopct='%1.1f%%')
plt.title('Booking status proportion')
if success != ['Successful'] :
    st.pyplot(fig2)
    
fig6, ax6 = plt.subplots()
chart6 = booking.groupby(by = 'meal', as_index = False).count()
ax6.pie(chart6['name'], labels = chart6['meal'], autopct='%1.1f%%')
plt.title('Proportion of the different options for meal')
if len(meal) != 1 :
    st.pyplot(fig6)
    
fig9, ax9 = plt.subplots()
temp9 = booking[['name', 'reserved_room_type', 'assigned_room_type']]
temp9.loc[temp9['reserved_room_type'] == temp9['assigned_room_type'], 'is_room_better'] = 2
temp9.loc[temp9['reserved_room_type'] < temp9['assigned_room_type'], 'is_room_better'] = 3
temp9.loc[temp9['reserved_room_type'] > temp9['assigned_room_type'], 'is_room_better'] = 1
chart9 = temp9.groupby(by = 'is_room_better').count().sort_values(by = 'is_room_better')
ax9.pie(chart9['name'], labels = ['Better', 'Same', 'Worse'], autopct='%1.1f%%')
plt.title('Quality of assigned room vs reserved room')
st.pyplot(fig9)

st.header('Repartitions of the bookings')

fig3, ax3 = plt.subplots(figsize = (12, 9))
chart3 = booking.groupby(by = 'arrival_date_month').count()
x3 = [m for m in all_months if m in months] if months != [] else all_months
y3 = [int(chart3.at[x, 'name']) for x in x3]
ax3.bar(range(len(x3)), y3, tick_label = x3)
plt.title('Number of bookings by month')
st.pyplot(fig3)

fig10, ax10 = plt.subplots()
chart10 = booking.groupby(by = 'country', as_index = False).count().sort_values(by = 'name', ascending = False).head(10)
ax10.bar(range(10), chart10['name'], tick_label = chart10['country'])
plt.title('Location of the bookings')
st.pyplot(fig10)

fig5, ax5 = plt.subplots()
chart5 = booking[['name', 'stays_in_weekend_nights', 'stays_in_week_nights']]
chart5['nights'] = chart5['stays_in_week_nights'] + chart5['stays_in_weekend_nights']
plt.title('Distribution of the duration')
sns.violinplot(chart5['nights'].apply(lambda x : min(20, x)))
st.pyplot(fig5)

fig4 = plt.figure()
ax4 = fig4.add_subplot(projection='3d')
temp4 = booking[['name', 'adults', 'children', 'babies']]
temp4['kids'] = temp4['children'] + temp4['babies']
chart4 = temp4.groupby(by = [temp4['adults'], temp4['kids']], as_index = False).count()
ax4.set_xlabel('Number of adults')
ax4.set_ylabel('Number of children')
ax4.set_zlabel('Number of bookings')
plt.title('Number of bookings by the number of adults and children')
ax4.scatter(chart4['adults'], chart4['kids'], chart4['name'])
st.pyplot(fig4)



st.header('Distribution channel')

fig1, ax1 = plt.subplots()
chart1 = booking.groupby(by = ['market_segment', 'distribution_channel'], as_index = False).count().sort_values(by = 'name', ascending = False)
other_slice1 = chart1.iloc[5:].sum()['name']
ax1.pie(list(chart1.head(5)['name'])+[other_slice1], labels = list(chart1.head(5)['market_segment'] + '\n' + chart1.head(5)['distribution_channel'])+['Other'], autopct='%1.1f%%')
plt.title('The five most frequent distribution channels')
st.pyplot(fig1)

fig7 = plt.figure()
ax7 = fig7.add_subplot(polar = True)
temp7 = booking[['name', 'market_segment', 'distribution_channel']]
temp7['amount'] = booking['adr'] * (booking['stays_in_weekend_nights'] + booking['stays_in_week_nights'])
chart7 = temp7.groupby(by = ['market_segment', 'distribution_channel'], as_index = False).agg('mean')
y7 = list(chart7['amount'])
y7.append(y7[0])
N7 = chart7.shape[0]
angles = [n / float(N7) * 2 * pi for n in range(N7)]
angles += angles[:1]
plt.xticks(angles[:-1], chart7['market_segment'] + '\n' + chart7['distribution_channel'], color='grey', size=8)
ax7.plot(angles, y7, linewidth=1, linestyle='solid')
plt.title('Average amount by distribution channel')
st.pyplot(fig7)

fig8 = plt.figure()
ax8 = fig8.add_subplot(polar = True)
temp8 = booking[['name', 'market_segment', 'distribution_channel']]
temp8['duration'] = booking['stays_in_weekend_nights'] + booking['stays_in_week_nights']
chart8 = temp8.groupby(by = ['market_segment', 'distribution_channel'], as_index = False).agg('mean')
y8 = list(chart8['duration'])
y8.append(y8[0])
N8 = chart8.shape[0]
angles = [n / float(N8) * 2 * pi for n in range(N8)]
angles += angles[:1]
plt.xticks(angles[:-1], chart8['market_segment'] + '\n' + chart8['distribution_channel'], color='grey', size=8)
ax8.plot(angles, y8, linewidth=1, linestyle='solid')
plt.title('Average duration by distribution channel')
st.pyplot(fig8)