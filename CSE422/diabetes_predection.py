# -*- coding: utf-8 -*-
"""diabetes_predection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1J1ZNPtXXVi7gO8aE_PBzEdYcf13t8zfO
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import seaborn as sns
from matplotlib import pyplot as plt

"""Data collection and analysis"""

data = pd.read_csv('diabetes_data.csv')
data.head()

#checking for null values
data.info()

"""Data Preprocessing"""

#dropping unnecessary columns
data = data.drop(['Education','Income','NoDocbcCost','AnyHealthcare','CholCheck'], axis=1)
data.info()

#visualizing correlation
plt.figure(figsize=(15,6))
sns.heatmap(data.corr(),annot=True, cmap='YlGnBu')

"""Bar chart of the features"""

#splitting data into male and female (male=1, female=0)
male_data = data[data['Sex']==1]
female_data = data[data['Sex']==0]

#dropping the 'sex' column from both datasets
male_data = male_data.drop(['Sex'],axis=1)
female_data = female_data.drop(['Sex'],axis=1)

print(male_data.shape)
print(female_data.shape)

#male correlation
plt.figure(figsize=(15,6))
sns.heatmap(male_data.corr(),annot=True, cmap='YlGnBu')

#female correlation
plt.figure(figsize=(15,6))
sns.heatmap(female_data.corr(), annot=True, cmap='Reds')

"""checking the values of outcome:\
<br>0 = No diabetes\
    1 = pre-diabetes\
    2 = Diabetes
"""

data['Diabetes_012'].value_counts()

class_counts = data['Diabetes_012'].value_counts()

class_label_mapping = {
    0.0: 'No Diabetes',
    1.0: 'Prediabetes',
    2.0: 'Diabetes'
}

output_feature_mapped = data['Diabetes_012'].map(class_label_mapping)

# Calculate the frequency of each class
class_counts = output_feature_mapped.value_counts()

# Create a bar plot
plt.figure(figsize=(8, 6))
class_counts.plot(kind='bar')
plt.xlabel('')
plt.ylabel('Frequency')
plt.title('Distribution of Classes in Output Feature')
plt.xticks(rotation=0)
plt.show()

"""Data Splitting"""

male_x = male_data.drop(['Diabetes_012'], axis=1)
male_y = male_data['Diabetes_012']

female_x = female_data.drop(['Diabetes_012'], axis=1)
female_y = female_data['Diabetes_012']

"""Fixing imbanalce by random oversampling"""

from imblearn.over_sampling import RandomOverSampler
# Apply random oversampling
ros = RandomOverSampler(random_state=42)
male_x, male_y = ros.fit_resample(male_x, male_y)

"""Data Standardization"""

scaler = StandardScaler()

scaler.fit(male_x)
scaler.fit(female_x)

male_x_std = scaler.transform(male_x)
female_x_std = scaler.transform(female_x)
print('Male scaled values:')
print(male_x_std[0])

print('Female scaled values: ')
print(female_x_std[0])

"""Train-Test split"""

male_x_train, male_x_test, male_y_train, male_y_test = train_test_split(male_x_std, male_y, test_size=0.3, stratify=male_y, random_state=2)
#stratify splits data such that train and test has mixup of y outcomes

female_x_train, female_x_test, female_y_train, female_y_test = train_test_split(female_x_std, female_y, test_size=0.3, stratify=female_y, random_state=2)

"""Training k-nearest neighbors"""

from sklearn.neighbors import KNeighborsClassifier

knn_classifier_male = KNeighborsClassifier(n_neighbors=10)

#training knn using male data
knn_classifier_male.fit(male_x_train,male_y_train)

"""Accuracy Score of k-nearest neighbors"""

#checking accuracy of male train data
male_train_prediction = knn_classifier_male.predict(male_x_train)
training_accuracy = accuracy_score(male_train_prediction, male_y_train)
print(training_accuracy)
print(f'The accuracy of male train data using knn is: {round(training_accuracy*100, 3)} %')

#checking accuracy of male test data
male_test_predict_knn = knn_classifier_male.predict(male_x_test)
training_accuracy = accuracy_score(male_test_predict_knn, male_y_test)
print(training_accuracy)
print(f'The accuracy of male TEST data using knn is: {round(training_accuracy*100, 3)} %')

"""Training Random Forest"""

from sklearn.ensemble import RandomForestClassifier
forest_male = RandomForestClassifier()

forest_male.fit(male_x_train, male_y_train)

"""Accuracy Score of Random Forest"""

#checking accuracy of male train data
male_train_predict_forest = forest_male.predict(male_x_train)
training_accuracy = accuracy_score(male_train_predict_forest, male_y_train)
print(training_accuracy)
print(f'The accuracy of male TRAIN data using Random Forest is: {round(training_accuracy*100, 3)} %')

#checking accuracy of male test data
male_test_predict_forest = forest_male.predict(male_x_test)
training_accuracy = accuracy_score(male_test_predict_forest, male_y_test)
print(training_accuracy)
print(f'The accuracy of male TEST data using Random Forest is: {round(training_accuracy*100, 3)} %')

"""Training Naive Bayes"""

from sklearn.naive_bayes import GaussianNB

nb_classifier = GaussianNB()

nb_classifier.fit(male_x_train, male_y_train)

"""Accuracy Score of Naive Bayes Classifier"""

#checking accuracy of male train data
male_train_predict_nb = nb_classifier.predict(male_x_train)
training_accuracy = accuracy_score(male_train_predict_nb, male_y_train)
print(training_accuracy)
print(f'The accuracy of male TRAIN data using Naive Bayes is: {round(training_accuracy*100, 3)} %')

#checking accuracy of male test data

male_test_predict_nb = nb_classifier.predict(male_x_test)
training_accuracy = accuracy_score(male_test_predict_nb, male_y_test)
print(training_accuracy)
print(f'The accuracy of male TEST data using Naive Bayes is: {round(training_accuracy*100, 3)} %')

"""Confusion Matrix for knn Classifier"""

from sklearn.metrics import confusion_matrix

cm_knn = confusion_matrix(male_y_test, male_test_predict_knn)
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
sns.heatmap(cm_knn, annot=True, fmt="d", cmap="Blues", cbar=False)
plt.title("K-nearest neighbour Classifier Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

cm_forest = confusion_matrix(male_y_test, male_test_predict_forest)
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
sns.heatmap(cm_forest, annot=True, fmt="d", cmap="Blues", cbar=False)
plt.title("Random Forest Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

cm_nb = confusion_matrix(male_y_test, male_test_predict_nb)
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
sns.heatmap(cm_nb, annot=True, fmt="d", cmap="Blues", cbar=False)
plt.title("Naive Bayes Classifier Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

"""Bar Chart of 3 models"""

nb_y_pred = np.array(male_test_predict_nb, dtype=int)
knn_y_pred = np.array(male_test_predict_knn, dtype=int)
forest_y_pred = np.array(male_test_predict_forest, dtype=int)

nb_counts = np.bincount(nb_y_pred)
knn_counts = np.bincount(knn_y_pred)
forest_counts = np.bincount(forest_y_pred)

# Create an array of class labels
class_labels = ['No Diabetes', 'Prediabetes', 'Diabetes']

# Create bar charts for each model's predicted class distribution
plt.figure(figsize=(10, 6))

plt.bar(np.arange(len(class_labels)) - 0.2, nb_counts, width=0.2, align='center', label='Naive Bayes')
plt.bar(np.arange(len(class_labels)), knn_counts, width=0.2, align='center', label='knn Classifier')
plt.bar(np.arange(len(class_labels)) + 0.2, forest_counts, width=0.2, align='center', label='Random Forest')

plt.xticks(np.arange(len(class_labels)), class_labels)
plt.xlabel('Predicted Class')
plt.ylabel('Frequency')
plt.title('Predicted Class Distribution for Different Models')
plt.legend()

plt.show()

"""Precision and Recall of the models"""

from tabulate import tabulate
from sklearn.metrics import precision_score, recall_score

# Assuming male_y_test, male_test_predict_knn, male_test_predict_forest, and male_test_predict_nb are your variables

# Calculate precision and recall for Naive Bayes
nb_precision = precision_score(male_y_test, male_test_predict_nb, average=None, zero_division=0)
nb_recall = recall_score(male_y_test, male_test_predict_nb, average=None, zero_division=0)

# Calculate precision and recall for knn
knn_precision = precision_score(male_y_test, male_test_predict_knn, average=None, zero_division=0)
knn_recall = recall_score(male_y_test, male_test_predict_knn, average=None, zero_division=0)

# Calculate precision and recall for Random Forest
forest_precision = precision_score(male_y_test, male_test_predict_forest, average=None, zero_division=0)
forest_recall = recall_score(male_y_test, male_test_predict_forest, average=None, zero_division=0)

# Round the precision and recall values to 5 decimal places
nb_precision_rounded = [round(p, 5) for p in nb_precision]
nb_recall_rounded = [round(r, 5) for r in nb_recall]

knn_precision_rounded = [round(p, 5) for p in knn_precision]
knn_recall_rounded = [round(r, 5) for r in knn_recall]

forest_precision_rounded = [round(p, 5) for p in forest_precision]
forest_recall_rounded = [round(r, 5) for r in forest_recall]

# Create class labels
class_labels = ['No Diabetes', 'Prediabetes', 'Diabetes']

# Prepare data for tabulation for each model
data_nb = []
data_knn = []
data_forest = []
for label, nb_p, knn_p, forest_p, nb_r, knn_r, forest_r in zip(class_labels, nb_precision_rounded, knn_precision_rounded, forest_precision_rounded, nb_recall_rounded, knn_recall_rounded, forest_recall_rounded):
    data_nb.append([label, nb_p, nb_r])
    data_knn.append([label, knn_p, knn_r])
    data_forest.append([label, forest_p, forest_r])

# Table headers
headers = ["Class", "NB Precision", "NB Recall"]
headers_knn = ["Class", "knn Precision", "knn Recall"]
headers_forest = ["Class", "Forest Precision", "Forest Recall"]

# Display the tables for all three models
nb_table = tabulate(data_nb, headers, tablefmt="pretty")
knn_table = tabulate(data_knn, headers_knn, tablefmt="pretty")
forest_table = tabulate(data_forest, headers_forest, tablefmt="pretty")

print("Naive Bayes Precision and Recall:")
print(nb_table)

print("\nknn Precision and Recall:")
print(knn_table)

print("\nRandom Forest Precision and Recall:")
print(forest_table)

plt.figure(figsize=(10, 6))

class_labels = ['No Diabetes', 'Prediabetes', 'Diabetes']
x = np.arange(len(class_labels))
plt.bar(x - 0.2, nb_precision_rounded, width=0.2, align='center', label='Naive Bayes')
plt.bar(x, knn_precision_rounded, width=0.2, align='center', label='knn')
plt.bar(x + 0.2, forest_precision_rounded, width=0.2, align='center', label='Random Forest')

plt.xticks(x, class_labels)
plt.xlabel('Class')
plt.ylabel('Precision')
plt.title('Precision Comparison for Different Models')
plt.legend()

plt.show()

# Create bar charts for Recall
plt.figure(figsize=(10, 6))

plt.bar(x - 0.2, nb_recall_rounded, width=0.2, align='center', label='Naive Bayes')
plt.bar(x, knn_recall_rounded, width=0.2, align='center', label='knn')
plt.bar(x + 0.2, forest_recall_rounded, width=0.2, align='center', label='Random Forest')

plt.xticks(x, class_labels)
plt.xlabel('Class')
plt.ylabel('Recall')
plt.title('Recall Comparison for Different Models')
plt.legend()

plt.show()