# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 09:39:39 2022

@author: anato
"""
#import usefull libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from pandas.plotting import parallel_coordinates
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score

#exploratory data analysis
bankrupt = pd.read_csv(r"C:\Users\anato\Documents\IRONHACK\IronFrandre\Project 7 Bankruptcy\bankrupt.csv")
bankrupt.info()
bankrupt.isna().sum()
bankrupt.duplicated().sum()
bankrupt.columns
bankrupt[' Net Income Flag'].value_counts()
bankrupt[' Liability-Assets Flag'].value_counts()
(bankrupt[' Net Value Per Share (B)'] != bankrupt[' Net Value Per Share (C)']).sum()
y = bankrupt['Bankrupt?']
X = bankrupt.drop(columns = 'Bankrupt?', axis = 1)

#Splitting and oversampling/undersampling the data
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5, stratify = y)
X_resampled, y_resampled = SMOTE().fit_resample(x_train, y_train)
rus = RandomUnderSampler(random_state=7)
X_undersampled, y_undersampled = rus.fit_resample(x_train, y_train)

y_resampled.value_counts()
y_undersampled.value_counts()

def ext_trees_model(X_m, y_m, nb_feat) :
    #Feature selection for extra trees model
    extratrees = RFE(estimator=ExtraTreesClassifier(),n_features_to_select = nb_feat, step = 1)
    mod_extratrees = extratrees.fit(X_m, y_m)
    features_XT = list(X_m.columns[mod_extratrees.get_support()])
    #Running the extra trees model
    etc = ExtraTreesClassifier()
    etc.fit(X_m[features_XT], y_m)
    y_XT = etc.predict(x_test[features_XT])
    print(classification_report(y_test, y_XT), sep = "\n")
    print(confusion_matrix(y_test, y_XT))
    return metrics.precision_score(y_test, y_XT), metrics.recall_score(y_test, y_XT), metrics.roc_auc_score(y_test, y_XT)
    
ext_trees_model(X_undersampled, y_undersampled, 5)

def rand_forest_model(X_m, y_m, nb_feat) :
    #Feature selection for random forest model
    rfe_selector = RFE(estimator=RandomForestClassifier(),n_features_to_select = nb_feat, step = 1)
    mod_forest=rfe_selector.fit(X_m, y_m)
    features_RF = list(X_m.columns[mod_forest.get_support()])
    #Running the random forest model
    rfc = RandomForestClassifier()
    rfc.fit(X_m[features_RF], y_m)
    y_RF = rfc.predict(x_test[features_RF])
    print(classification_report(y_test, y_RF), sep = "\n")
    print(confusion_matrix(y_test, y_RF))
    return metrics.precision_score(y_test, y_RF), metrics.recall_score(y_test, y_RF), metrics.roc_auc_score(y_test, y_RF)
    
rand_forest_model(X_undersampled, y_undersampled, 17)

def dec_tree_model(X_m, y_m, nb_feat) :
    #Feature selection for decision tree model
    dte_selector = RFE(estimator=DecisionTreeClassifier(),n_features_to_select = nb_feat, step = 1)
    mod_tree=dte_selector.fit(X_m, y_m)
    features_DT = list(X_m.columns[mod_tree.get_support()])
    #Running the decision tree model
    dtc = DecisionTreeClassifier()
    dtc.fit(X_m[features_DT], y_m)
    y_DT = dtc.predict(x_test[features_DT])
    print(classification_report(y_test, y_DT), sep = "\n")
    print(confusion_matrix(y_test, y_DT))
    return metrics.precision_score(y_test, y_DT), metrics.recall_score(y_test, y_DT), metrics.roc_auc_score(y_test, y_DT)

dec_tree_model(X_undersampled, y_undersampled, 17)

l = []
for i in range(2, 21) :
    l.append(ext_trees_model(X_resampled, y_resampled, i))
l = [(0.1891891891891892, 0.7636363636363637, 0.8272727272727273),
 (0.19047619047619047, 0.7272727272727273, 0.8121212121212121),
 (0.20855614973262032, 0.7090909090909091, 0.8096969696969696),
 (0.22043010752688172, 0.7454545454545455, 0.8287878787878789),
 (0.21910112359550563, 0.7090909090909091, 0.8124242424242424),
 (0.24074074074074073, 0.7090909090909091, 0.8172727272727273),
 (0.25161290322580643, 0.7090909090909091, 0.8193939393939393),
 (0.2468354430379747, 0.7090909090909091, 0.8184848484848484),
 (0.2805755395683453, 0.7090909090909091, 0.8242424242424242),
 (0.2896551724137931, 0.7636363636363637, 0.8506060606060606),
 (0.29927007299270075, 0.7454545454545455, 0.8436363636363637),
 (0.2898550724637681, 0.7272727272727273, 0.8339393939393939),
 (0.3125, 0.7272727272727273, 0.836969696969697),
 (0.31007751937984496, 0.7272727272727273, 0.8366666666666667),
 (0.3103448275862069, 0.6545454545454545, 0.8030303030303031),
 (0.3333333333333333, 0.7090909090909091, 0.8309090909090909),
 (0.3211009174311927, 0.6363636363636364, 0.7957575757575758),
 (0.33980582524271846, 0.6363636363636364, 0.7975757575757575),
 (0.3486238532110092, 0.6909090909090909, 0.823939393939394)]

plt.bar(range(2, 21), [t[1] for t in l])
plt.xlabel('Number of features')
plt.ylabel('Recall score')
plt.title('Evolution of the recall score by the number of features')
plt.show()

plt.bar(range(2, 21), [t[0] for t in l])
plt.xlabel('Number of features')
plt.ylabel('Precision score score')
plt.title('Evolution of the precision score by the number of features')
plt.show()