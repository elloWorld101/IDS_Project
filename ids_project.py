# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import seaborn as sns
import math
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from sklearn.neighbors import KNeighborsClassifier
from sklearn. linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

df=pd.read_csv('winequality-white.csv')

df.head()

df.quality.nunique()

df.info()

df.replace("?", -1, inplace=True)
df[df==-1].count()

df.describe()

df.drop_duplicates(inplace=True)
df.duplicated().sum()

df.plot(kind='box', subplots=True, layout=(4,4), sharex=False, sharey=False, figsize=(15,15))
plt.show()

df=pd.read_csv('winequality-white.csv')

# Identify numerical attributes (excluding 'alcohol')
numerical_attributes = df.select_dtypes(include=np.number).columns.tolist()
numerical_attributes.remove('alcohol')

# Remove outliers for each numerical attribute
for attribute in numerical_attributes:
    Q1 = df[attribute].quantile(0.25)
    Q3 = df[attribute].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df[attribute] >= lower_bound) & (df[attribute] <= upper_bound)]

df.plot(kind='box', subplots=True, layout=(4,4), sharex=False, sharey=False, figsize=(15,15))
plt.show()

X=df.drop('quality',axis=1)
X

y=df.quality
y

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

scalar = StandardScaler()
X_train = scalar.fit_transform(X_train)
X_test = scalar.transform(X_test)

plt.figure(figsize=(15,6))
plot=sns.heatmap(df.corr(),annot=True)
plt.show()
#maximum correlation we can see is 0.85, which is not significant enough for removal

#KNN

rms_val = [] #to store root mean square error values for different values of K
acc = []

for K in range(1 , 15):
    model = KNeighborsClassifier(n_neighbors = K)
    model.fit(X_train, y_train)  #fit the model
    y_pred=model.predict(X_test) #make prediction on test set
    error = np.sqrt(metrics.mean_squared_error(y_test, y_pred)) #calculate rmse
    rms_val.append(error) #store rmse values
    acc.append(metrics.accuracy_score(y_test, y_pred))
    print('Accuracy for K=', K, 'is:', f'{acc[K-1]:.2%}')

plt.figure(figsize=(12, 6))
plt.plot(range(1 , 15), rms_val, color='red', linestyle='dashed', marker='o', markerfacecolor='blue', markersize=10)
plt.title('Error Rate vs K Value')
plt.xlabel('K Value')
plt.ylabel('Mean Squared Error')
plt.show()

#SVM

from sklearn.metrics import confusion_matrix

#create an SVM model
svm_model = SVC(kernel='linear')

#train the model on the training data
svm_model.fit(X_train, y_train)

#make predictions on the test data
y_pred = svm_model.predict(X_test)

#printing accuracy
accuracy = metrics.accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:%}')

#calculate and print the confusion matrix
cm = confusion_matrix(y_test, y_pred)
svm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm,display_labels=['Quality 6','Quality 5','Quality 7','Quality 4'])
svm_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_pred))

#LR

lr = LogisticRegression()
lr.fit(X_train, y_train)
y_lr = lr.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_lr)
print(f'Accuracy: {accuracy:%}')
cm_lr = metrics.confusion_matrix(y_test, y_lr)
lr_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm_lr,display_labels=['Quality 6','Quality 5','Quality 7','Quality 4'])
lr_display.plot()
plt.show()

print(metrics.classification_report(y_test, y_lr))

#Naive Bayes

from sklearn.naive_bayes import GaussianNB

nb = GaussianNB()
nb.fit(X_train, y_train)
y_nb = model.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_nb)
print(f'Accuracy: {accuracy:%}')
cm_nb = metrics.confusion_matrix(y_test, y_nb)
nb_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm_nb,display_labels=['Quality 6','Quality 5','Quality 7','Quality 4'])
nb_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_nb))

#Decision Tree

dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)
y_dt = dt.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_dt)
print(f'Accuracy: {accuracy:%}')
cm_dt = metrics.confusion_matrix(y_test, y_dt)
dt_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm_dt,display_labels=['Quality 6','Quality 5','Quality 7','Quality 4'])
dt_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_dt))

#Random Forest

rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_rf = rf.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_rf)
print(f'Accuracy: {accuracy:%}')
cm_rf = metrics.confusion_matrix(y_test, y_rf)
rf_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm_rf,display_labels=['Quality 6','Quality 5','Quality 7','Quality 4'])
rf_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_rf))

#Plot comparisons between all models

lab = ['KNN', 'SVM', 'LR', 'NB', 'DT', 'RF']
accuracy = [66.58, 52.42, 55.44, 58.71, 67.89, 72.30]

plt.plot(lab, accuracy, color='blue', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10)
plt.title('Accuracy Comparison')
plt.xlabel('Models')
plt.ylabel('Accuracy')
plt.show()

# correlation matrix for attributes in df
df=pd.read_csv('winequality-white.csv')

# Identify numerical attributes
numerical_attributes = df.select_dtypes(include=np.number).columns.tolist()
numerical_attributes.remove('alcohol')

print(df.corr().to_string())

