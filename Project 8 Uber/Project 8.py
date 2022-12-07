# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 10:05:58 2022

@author: anato
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static
import sklearn
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from yellowbrick.cluster import KElbowVisualizer
from sklearn import metrics



uber = pd.read_csv(r"C:\Users\anato\Documents\IRONHACK\IronFrandre\Project 8 Uber\uberjun14.csv")
uber.isna().sum()
uber['Base'].value_counts()
sampled = uber
sampled = sampled.sample(n = 10000, random_state = 18, axis = 0)

sampled['Dates'] = pd.to_datetime(sampled['Date/Time']).dt.date
sampled['Time'] = pd.to_datetime(sampled['Date/Time']).dt.time

firstindex  = sampled.pop("Dates")
sampled.insert(0, 'Dates', firstindex)
secondindex = sampled.pop("Time")
sampled.insert(1, 'Time', secondindex)

sampled['day'] = pd.to_datetime(sampled['Date/Time']).dt.day
sampled['minute'] = pd.to_datetime(sampled['Date/Time']).dt.minute
sampled['hour'] = pd.to_datetime(sampled['Date/Time']).dt.hour
sampled['day_of_week'] = day = pd.to_datetime(sampled['Date/Time']).dt.day_of_week

st.title('Project 8 : Unsupervised ML')

day_select = st.sidebar.multiselect('Select the days', range(1, 31))
if day_select != [] :
    sampled = sampled.loc[sampled['day'].isin(day_select)]

hour_select = st.sidebar.multiselect('Select the hours', range(24))
if hour_select != [] :
    sampled = sampled.loc[sampled['hour'].isin(hour_select)]
    
def dayinweekencode(s) :
    if s == 'Monday' :
        return 0
    elif s == 'Tuesday' :
        return 1
    elif s == 'Wednesday' :
        return 2
    elif s == 'Thursday' :
        return 3
    elif s == 'Friday' :
        return 4
    elif s == 'Saturday' :
        return 5
    elif s == 'Sunday' :
        return 6

in_week = st.sidebar.multiselect('Select the days in the week', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
if in_week != [] :
    sampled = sampled.loc[sampled['day_of_week'].isin(map(dayinweekencode, in_week))]
    
if sampled.shape[0] > 2000 :
    sampled = sampled.sample(n = 2000, random_state = 18, axis = 0)

sampled['day_norm'] = sampled['day']/30
sampled['day_of_week_norm'] = sampled['day_of_week']/6
sampled['hour_norm'] = (sampled['hour'] * 60 + sampled['minute']) / (24 * 60)
latmax = sampled['Lat'].max()
latmin = sampled['Lat'].min()
sampled['Latnorm'] = (sampled['Lat'] - latmin)/(latmax-latmin)
longmax = sampled['Lon'].max()
longmin = sampled['Lon'].min()
sampled['Longnorm'] = (sampled['Lon'] - longmin)/(longmax-longmin)

x = sampled[['Longnorm', 'Latnorm']]


model = KMeans()
visualizer = KElbowVisualizer(estimator = model, k = (2,10))
visualizer.fit(x)
kmean_nb_clusters = visualizer.elbow_value_

kmeans = KMeans(n_clusters=kmean_nb_clusters)
kmeans.fit(x)
sampled['k_mean_labels'] = kmeans.predict(x)

fig1 = plt.figure(figsize = (20, 10))
plt.scatter(x = sampled['Lat'], y = sampled['Lon'], c = sampled['k_mean_labels'])
#st.pyplot(fig1)

def color_from_int(n) :
    if n == -1 :
        return "black"
    elif n == 0 :
        return "red"
    elif n == 1 :
        return "green"
    elif n == 2 :
        return "darkblue"
    elif n == 3 :
        return "pink"
    elif n == 4 :
        return "orange"
    elif n == 5 :
        return "beige"
    elif n == 6 :
        return "lightgreen"
        
        
        
m = folium.Map(location=[sampled['Lat'].mean(), sampled['Lon'].mean()], zoom_start = 10, tiles = 'Stamen Toner')
for i in sampled.index :
    folium.Circle(
    radius=10,
    location=[sampled.at[i, 'Lat'], sampled.at[i, 'Lon']],
    color=color_from_int(sampled.at[i, 'k_mean_labels']),
).add_to(m)
folium_static(m)
#m.save(r"C:\Users\anato\Documents\IRONHACK\IronFrandre\Project 8 Uber\mymap.html")

model2 = AgglomerativeClustering(affinity='euclidean', linkage='ward')
visualizer2 = KElbowVisualizer(estimator = model2, k = (2,10))
visualizer2.fit(x)
aggc_nb_clusters = visualizer2.elbow_value_

aggc = AgglomerativeClustering(n_clusters = aggc_nb_clusters, affinity='euclidean', linkage='ward')
sampled['aggc_labels'] = aggc.fit_predict(x)

m2 = folium.Map(location=[sampled['Lat'].mean(), sampled['Lon'].mean()], zoom_start = 10, tiles = 'Stamen Toner')
for i in sampled.index :
    folium.Circle(
    radius=10,
    location=[sampled.at[i, 'Lat'], sampled.at[i, 'Lon']],
    color=color_from_int(sampled.at[i, 'aggc_labels']),
).add_to(m2)
folium_static(m2)
#m2.save(r"C:\Users\anato\Documents\IRONHACK\IronFrandre\Project 8 Uber\mapaggc.html")

dbscan = DBSCAN(eps=0.01, min_samples=10)
dbscan.fit(x)
sampled['dbscanlabel'] = dbscan.labels_


m3 = folium.Map(location=[sampled['Lat'].mean(), sampled['Lon'].mean()], zoom_start = 10, tiles = 'Stamen Toner')
for i in sampled.index :
    folium.Circle(
    radius=5,
    location=[sampled.at[i, 'Lat'], sampled.at[i, 'Lon']],
    color=color_from_int(sampled.at[i, 'dbscanlabel']),
).add_to(m3)
folium_static(m3)
#m3.save(r"C:\Users\anato\Documents\IRONHACK\IronFrandre\Project 8 Uber\mapdbscan.html")


hours = range(24)
heats_hour = pd.DataFrame(data = 0, columns = map(str, range(kmean_nb_clusters)), index = hours)
for i in range(kmean_nb_clusters) :
    for h in hours :
        heats_hour.at[h, str(i)] = sampled.loc[(sampled['hour'] == h) & (sampled['k_mean_labels'] == i)].shape[0]
fig2 = plt.figure(figsize = (20, 8))
plt.imshow(heats_hour, cmap='hot', interpolation='nearest')
plt.xticks(ticks = range(kmean_nb_clusters))
plt.yticks(ticks = hours)
plt.show()

days = range(1, 31)
heats_day = pd.DataFrame(data = 0, columns = map(str, range(kmean_nb_clusters)), index = days)
for i in range(kmean_nb_clusters) :
    for d in days :
        heats_day.at[d, str(i)] = sampled.loc[(sampled['day'] == d) & (sampled['k_mean_labels'] == i)].shape[0]
fig3 = plt.figure(figsize = (20, 8))
plt.imshow(heats_day, cmap='hot', interpolation='nearest')
plt.xticks(ticks = range(kmean_nb_clusters))
plt.yticks(ticks = range(30), labels = days)
plt.show()

days_of_week = range(7)
heats_day_of_week = pd.DataFrame(data = 0, columns = map(str, range(kmean_nb_clusters)), index = days_of_week)
for i in range(kmean_nb_clusters) :
    for d in days_of_week :
        heats_day_of_week.at[d, str(i)] = sampled.loc[(sampled['day_of_week'] == d) & (sampled['k_mean_labels'] == i)].shape[0]
fig4 = plt.figure(figsize = (20, 8))
plt.imshow(heats_day_of_week, cmap='hot', interpolation='nearest')
plt.xticks(ticks = range(kmean_nb_clusters))
plt.yticks(ticks = days_of_week, labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.show()

st.markdown("Comparaison between the models : Silhouette scores.")
st.metric("Silhouette score of Kmean", metrics.silhouette_score(x, sampled['k_mean_labels'], metric="sqeuclidean"))
st.metric("Silhouette score of Agglomerative clustering", metrics.silhouette_score(x, sampled['aggc_labels'], metric="sqeuclidean"))
st.metric("Silhouette score of DBSCAN", metrics.silhouette_score(x, sampled['dbscanlabel'], metric="sqeuclidean"))