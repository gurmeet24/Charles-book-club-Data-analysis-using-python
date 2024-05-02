# -*- coding: utf-8 -*-
"""AIES_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uu3yAOexDisoCnCPcksKLw-W_yyL_zF1
"""

import pandas as pd
import numpy as np

from google.colab import files


uploaded = files.upload()

df=pd.read_csv('CharlesBookClub.csv')

df.head(), df.columns

import pandas as pd

# Assuming the data is loaded into a DataFrame named df

# Total purchases for each category
total_purchases = df[['ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'GeogBks']].sum()
print("Total purchases for each category:")
print(total_purchases)

# Total purchases for each category by gender
total_purchases_gender = df.groupby('Gender')[['ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'GeogBks']].sum()
print("\nTotal purchases for each category by gender:")
print(total_purchases_gender)

# Total purchases for each category by gender and Florence purchase
total_purchases_gender_florence = df.groupby(['Gender', 'Yes_Florence'])[['ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'GeogBks']].sum()
print("\nTotal purchases for each category by gender and Florence purchase:")
print(total_purchases_gender_florence)

# Average number of purchases
average_purchases = df[['ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'GeogBks']].mean()
print("\nAverage number of purchases:")
print(average_purchases)

import pandas as pd

# Load the data from CSV into a DataFrame
df = pd.read_csv("CharlesBookClub.csv")

# Perform analysis

# Total purchases for each category
total_purchases = df[['ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'GeogBks']].sum()

# Total purchases for each category by gender
total_purchases_gender = df.groupby('Gender')[['ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'GeogBks']].sum()

# Total purchases for each category by gender and Florence purchase
total_purchases_gender_florence = df.groupby(['Gender', 'Yes_Florence'])[['ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'GeogBks']].sum()

# Average number of purchases
average_purchases = df[['ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'GeogBks']].mean()

# Display the results
print("Total purchases for each category:")
print(total_purchases)
print("\nTotal purchases for each category by gender:")
print(total_purchases_gender)
print("\nTotal purchases for each category by gender and Florence purchase:")
print(total_purchases_gender_florence)
print("\nAverage number of purchases:")
print(average_purchases)



import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score

# Load the data
df = pd.read_csv("CharlesBookClub.csv")

# Data preprocessing
df['Gender'] = df['Gender'].astype(str)

# Partition the data into training (60%) and validation (40%)
train, validation = train_test_split(df, test_size=0.4, random_state=1)

# Response rate for the training data customers taken as a whole
response_rate_training = train['Florence'].mean()
print("Response rate for the training data customers taken as a whole:", response_rate_training)

# Response rate for each combination of RFM categories
rfm_combinations = ['R', 'F', 'M']
for r in range(1, 5):
    for f in range(1, 4):
        for m in range(1, 6):
            subset = train[(train['R'] == r) & (train['F'] == f) & (train['M'] == m)]
            response_rate = subset['Florence'].mean()
            print(f"RFM combination: R{r}F{f}M{m}, Response rate: {response_rate}")

# "Above-average" RFM combinations identified in part 1
above_average_combinations = []
for r in range(1, 5):
    for f in range(1, 4):
        for m in range(1, 6):
            subset = train[(train['R'] == r) & (train['F'] == f) & (train['M'] == m)]
            response_rate = subset['Florence'].mean()
            if response_rate > response_rate_training:
                above_average_combinations.append((r, f, m))

# Compute the response rate in the validation data using above-average combinations
response_rate_validation = validation[validation.apply(lambda row: (row['R'], row['F'], row['M']) in above_average_combinations, axis=1)]['Florence'].mean()
print("Response rate in the validation data using above-average combinations:", response_rate_validation)

# Segmentation into three segments
segment1 = []
segment2 = []
segment3 = []
for r in range(1, 5):
    for f in range(1, 4):
        for m in range(1, 6):
            subset = train[(train['R'] == r) & (train['F'] == f) & (train['M'] == m)]
            response_rate = subset['Florence'].mean()
            if response_rate > 2 * response_rate_training:
                segment1.append((r, f, m))
            elif response_rate > response_rate_training:
                segment2.append((r, f, m))
            else:
                segment3.append((r, f, m))

# Lift curve
lift_curve_data = [
    (len(segment1), validation[validation.apply(lambda row: (row['R'], row['F'], row['M']) in segment1, axis=1)]['Florence'].sum()),
    (len(segment1) + len(segment2), validation[validation.apply(lambda row: (row['R'], row['F'], row['M']) in segment1 + segment2, axis=1)]['Florence'].sum()),
    (len(validation), validation['Florence'].sum())
]

x = [point[0] for point in lift_curve_data]
y = [point[1] for point in lift_curve_data]

plt.plot(x, y, marker='o')
plt.xlabel('Number of customers in the validation dataset')
plt.ylabel('Cumulative number of buyers in the validation dataset')
plt.title('Lift Curve')
plt.show()

print(train.columns)

# Question 4: k-Nearest Neighbors

# Normalize the data
scaler = StandardScaler()

from sklearn.preprocessing import StandardScaler

# Normalize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(train[['R', 'F', 'M', 'FirstPurch', 'Related Purchase']])
X_validation = scaler.transform(validation[['R', 'F', 'M', 'FirstPurch', 'Related Purchase']])


# Define a function to calculate lift curve
def plot_lift_curve(y_true, y_score, title):
    fpr, tpr, _ = roc_curve(y_true, y_score)
    plt.plot(fpr, tpr, marker='o')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.show()

# Find the best k
best_score = 0
best_k = None
for k in range(1, 12):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, train['Florence'])
    score = knn.score(X_validation, validation['Florence'])
    if score > best_score:
        best_score = score
        best_k = k

print("Best k for k-NN:", best_k)

# Compute the lift curve for the best k model
knn_best = KNeighborsClassifier(n_neighbors=best_k)
knn_best.fit(X_train, train['Florence'])
plot_lift_curve(validation['Florence'], knn_best.predict_proba(X_validation)[:, 1], "k-NN Lift Curve")

# Question 5: k-NN prediction algorithm
# Use the best k for prediction
y_pred_proba = knn_best.predict_proba(X_validation)[:, 1]
expected_lift = np.mean(y_pred_proba)
print("Expected lift for an equal number of customers from the validation dataset:", expected_lift)

# Question 6: Logistic Regression
# Construct logistic regression models

# Full set of predictors
log_reg_full = LogisticRegression()
log_reg_full.fit(X_train, train['Florence'])

# Subset of predictors that you judge to be the best
log_reg_best_subset = LogisticRegression()
log_reg_best_subset.fit(X_train[:, :3], train['Florence'])

# Only the R, F, and M variables
log_reg_rfm = LogisticRegression()
log_reg_rfm.fit(X_train[:, :3], train['Florence'])

# Create cumulative gains chart
def plot_cumulative_gains(model, X, y_true, title):
    y_pred_proba = model.predict_proba(X)[:, 1]
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    plt.plot(fpr, tpr, marker='o')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.show()

plot_cumulative_gains(log_reg_full, X_validation, validation['Florence'], "Logistic Regression Full Set of Predictors")
plot_cumulative_gains(log_reg_best_subset, X_validation[:, :3], validation['Florence'], "Logistic Regression Best Subset")
plot_cumulative_gains(log_reg_rfm, X_validation[:, :3], validation['Florence'], "Logistic Regression R, F, M Variables")

# Question 7: Target customers based on a 30% likelihood of a purchase
cutoff = 0.3
target_customers = validation[log_reg_full.predict_proba(X_validation)[:, 1] > cutoff]
number_of_buyers = target_customers['Florence'].sum()
print("Number of buyers in the set targeted with a 30% likelihood of a purchase:", number_of_buyers)

# Calculate the overall response rate in the validation dataset
overall_response_rate_validation = validation['Florence'].mean()

# Assume 50% of the customers are selected for the campaign
proportion_selected = 0.5

# Calculate the expected lift
expected_lift = (overall_response_rate_validation * proportion_selected) / overall_response_rate_validation

print("Expected lift for an equal number of customers from the validation dataset:", expected_lift)

import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score




predictor_var = ['Gender', 'M', 'R', 'F', 'FirstPurch', 'ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'ItalCook', 'ItalAtlas', 'ItalArt']
outcome_var = 'Florence'


X_train, X_test, y_train, y_test = train_test_split(df[predictor_var], df[outcome_var], test_size=0.33, random_state=42)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train_scaled, y_train)


logreg_acc = accuracy_score(y_test, logreg.predict(X_test_scaled))
print("Logistic Regression Accuracy:", logreg_acc)


rf = RandomForestClassifier(random_state=42)
rf.fit(X_train_scaled, y_train)


rf_acc = accuracy_score(y_test, rf.predict(X_test_scaled))
print("Random Forest Accuracy:", rf_acc)

import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import SVC
from sklearn.decomposition import PCA




predictor_var = ['Gender', 'M', 'R', 'F', 'FirstPurch', 'ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'ItalCook', 'ItalAtlas', 'ItalArt']
outcome_var = 'Florence'


X_train, X_test, y_train, y_test = train_test_split(df[predictor_var], df[outcome_var], test_size=0.33, random_state=42)


logreg_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('logreg', LogisticRegression(max_iter=1000))
])

rf_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('rf', RandomForestClassifier(random_state=42))
])

svm_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=0.95)),
    ('svm', SVC())
])


models = [('Logistic Regression', logreg_pipe),
          ('Random Forest', rf_pipe),
          ('SVM', svm_pipe)]

for name, model in models:
    scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"{name} Mean Accuracy: {np.mean(scores)}")


voting_clf = VotingClassifier(estimators=models, voting='hard')
voting_clf.fit(X_train, y_train)
voting_accuracy = accuracy_score(y_test, voting_clf.predict(X_test))
print(f"Voting Classifier Accuracy: {voting_accuracy}")


param_grid = {
    'rf__n_estimators': [100, 200, 300],
    'rf__max_depth': [None, 10, 20, 30]
}

rf_grid = GridSearchCV(rf_pipe, param_grid, cv=5)
rf_grid.fit(X_train, y_train)
best_rf_accuracy = accuracy_score(y_test, rf_grid.best_estimator_.predict(X_test))
print(f"Best Random Forest Accuracy: {best_rf_accuracy}")


feat_selector = SelectFromModel(RandomForestClassifier(random_state=42))
X_train_selected = feat_selector.fit_transform(X_train, y_train)
X_test_selected = feat_selector.transform(X_test)


logreg_selected = LogisticRegression(max_iter=1000)
logreg_selected.fit(X_train_selected, y_train)
selected_feats_accuracy = accuracy_score(y_test, logreg_selected.predict(X_test_selected))
print(f"Logistic Regression with Selected Features Accuracy: {selected_feats_accuracy}")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("CharlesBookClub.csv")

# Define predictors and target variable
predictors = ['Gender', 'M', 'R', 'F', 'FirstPurch', 'ChildBks', 'YouthBks', 'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'ItalCook', 'ItalAtlas', 'ItalArt']
target = 'Florence'

# Split data into train and validation sets
X_train, X_validation, y_train, y_validation = train_test_split(df[predictors], df[target], test_size=0.4, random_state=42)

# Full set of predictors
log_reg_full = LogisticRegression()
log_reg_full.fit(X_train, y_train)

# Subset of predictors that you judge to be the best
log_reg_best_subset = LogisticRegression()
log_reg_best_subset.fit(X_train[['R', 'F', 'M']], y_train)

# Only the R, F, and M variables
log_reg_rfm = LogisticRegression()
log_reg_rfm.fit(X_train[['R', 'F', 'M']], y_train)

# Define a function to plot lift curve
def plot_lift_curve(y_true, y_score, title):
    fpr, tpr, _ = roc_curve(y_true, y_score)
    plt.plot(fpr, tpr, marker='o')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.show()

# Plot lift curve for logistic regression models
plot_lift_curve(y_validation, log_reg_full.predict_proba(X_validation)[:, 1], "Logistic Regression Full Set of Predictors")
plot_lift_curve(y_validation, log_reg_best_subset.predict_proba(X_validation[['R', 'F', 'M']])[:, 1], "Logistic Regression Best Subset")
plot_lift_curve(y_validation, log_reg_rfm.predict_proba(X_validation[['R', 'F', 'M']])[:, 1], "Logistic Regression R, F, M Variables")

from sklearn.neighbors import KNeighborsClassifier  # Import KNeighborsClassifier

# Define best_k (assuming it was previously defined)
best_k = 5  # for example

# Define k-NN model
knn_best = KNeighborsClassifier(n_neighbors=best_k)
knn_best.fit(X_train, y_train)

# Evaluate model performance
def evaluate_model_performance(model, X, y_true):
    y_pred = model.predict(X)
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    return accuracy, precision, recall, f1

# Evaluate k-NN model performance
knn_accuracy, knn_precision, knn_recall, knn_f1 = evaluate_model_performance(knn_best, X_validation, y_validation)
print("k-NN Model Performance:")
print(f"Accuracy: {knn_accuracy:.4f}")
print(f"Precision: {knn_precision:.4f}")
print(f"Recall: {knn_recall:.4f}")
print(f"F1-score: {knn_f1:.4f}")
print()

# Evaluate logistic regression model performance
log_reg_full_accuracy, log_reg_full_precision, log_reg_full_recall, log_reg_full_f1 = evaluate_model_performance(log_reg_full, X_validation, y_validation)
print("Logistic Regression (Full Set) Model Performance:")
print(f"Accuracy: {log_reg_full_accuracy:.4f}")
print(f"Precision: {log_reg_full_precision:.4f}")
print(f"Recall: {log_reg_full_recall:.4f}")
print(f"F1-score: {log_reg_full_f1:.4f}")
print()

log_reg_best_subset_accuracy, log_reg_best_subset_precision, log_reg_best_subset_recall, log_reg_best_subset_f1 = evaluate_model_performance(log_reg_best_subset, X_validation[['R', 'F', 'M']], y_validation)
print("Logistic Regression (Best Subset) Model Performance:")
print(f"Accuracy: {log_reg_best_subset_accuracy:.4f}")
print(f"Precision: {log_reg_best_subset_precision:.4f}")
print(f"Recall: {log_reg_best_subset_recall:.4f}")
print(f"F1-score: {log_reg_best_subset_f1:.4f}")
print()

log_reg_rfm_accuracy, log_reg_rfm_precision, log_reg_rfm_recall, log_reg_rfm_f1 = evaluate_model_performance(log_reg_rfm, X_validation[['R', 'F', 'M']], y_validation)
print("Logistic Regression (RFM Variables) Model Performance:")
print(f"Accuracy: {log_reg_rfm_accuracy:.4f}")
print(f"Precision: {log_reg_rfm_precision:.4f}")
print(f"Recall: {log_reg_rfm_recall:.4f}")
print(f"F1-score: {log_reg_rfm_f1:.4f}")
print()

# Analyze predictions for different segments (e.g., RFM combinations)
# You can define specific segments and analyze predictions for each segment here

from sklearn.preprocessing import StandardScaler

# Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train[['R', 'F', 'M']])
X_validation_scaled = scaler.transform(X_validation[['R', 'F', 'M']])

# Define logistic regression models with balanced class weights and increased max_iter
log_reg_full_balanced_scaled = LogisticRegression(class_weight='balanced', max_iter=1000)
log_reg_rfm_balanced_scaled = LogisticRegression(class_weight='balanced', max_iter=1000)

# Fit the models
log_reg_full_balanced_scaled.fit(X_train_scaled, y_train)
log_reg_rfm_balanced_scaled.fit(X_train_scaled, y_train)

# Evaluate model performance
log_reg_full_accuracy_scaled, log_reg_full_precision_scaled, log_reg_full_recall_scaled, log_reg_full_f1_scaled = evaluate_model_performance(log_reg_full_balanced_scaled, X_validation_scaled, y_validation)
log_reg_rfm_accuracy_scaled, log_reg_rfm_precision_scaled, log_reg_rfm_recall_scaled, log_reg_rfm_f1_scaled = evaluate_model_performance(log_reg_rfm_balanced_scaled, X_validation_scaled, y_validation)

print("Logistic Regression (Full Set) Model Performance with Balanced Class Weights and Scaled Data:")
print(f"Accuracy: {log_reg_full_accuracy_scaled:.4f}")
print(f"Precision: {log_reg_full_precision_scaled:.4f}")
print(f"Recall: {log_reg_full_recall_scaled:.4f}")
print(f"F1-score: {log_reg_full_f1_scaled:.4f}")
print()

print("Logistic Regression (RFM Variables) Model Performance with Balanced Class Weights and Scaled Data:")
print(f"Accuracy: {log_reg_rfm_accuracy_scaled:.4f}")
print(f"Precision: {log_reg_rfm_precision_scaled:.4f}")
print(f"Recall: {log_reg_rfm_recall_scaled:.4f}")
print(f"F1-score: {log_reg_rfm_f1_scaled:.4f}")
print()

# Tune model hyperparameters with scaled data
param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100]}  # Example grid of hyperparameters to tune

log_reg_rfm_tuned_scaled = LogisticRegression(class_weight='balanced', max_iter=1000)
grid_search_scaled = GridSearchCV(log_reg_rfm_tuned_scaled, param_grid, cv=5, scoring='f1')
grid_search_scaled.fit(X_train_scaled, y_train)
best_params_scaled = grid_search_scaled.best_params_
best_log_reg_rfm_scaled = grid_search_scaled.best_estimator_

# Evaluate the best tuned model with scaled data
log_reg_rfm_tuned_accuracy_scaled, log_reg_rfm_tuned_precision_scaled, log_reg_rfm_tuned_recall_scaled, log_reg_rfm_tuned_f1_scaled = evaluate_model_performance(best_log_reg_rfm_scaled, X_validation_scaled, y_validation)
print("Tuned Logistic Regression (RFM Variables) Model Performance with Balanced Class Weights and Scaled Data:")
print(f"Best Parameters: {best_params_scaled}")
print(f"Accuracy: {log_reg_rfm_tuned_accuracy_scaled:.4f}")
print(f"Precision: {log_reg_rfm_tuned_precision_scaled:.4f}")
print(f"Recall: {log_reg_rfm_tuned_recall_scaled:.4f}")
print(f"F1-score: {log_reg_rfm_tuned_f1_scaled:.4f}")
print()

from sklearn.model_selection import train_test_split

# Setting the seed for reproducibility
seed = 1

# Partition the data into training (60%) and validation (40%) sets
train_df, validation_df = train_test_split(df, test_size=0.4, random_state=seed)

# Checking the size of the training and validation datasets
train_df.shape, validation_df.shape

overall_response_rate_train = train_df['Florence'].mean()
overall_response_rate_train

rfm_response_rates_train = train_df.groupby(['Rcode', 'Fcode', 'Mcode'])['Florence'].mean().reset_index()


rfm_above_average = rfm_response_rates_train[rfm_response_rates_train['Florence'] > overall_response_rate_train]


rfm_above_average

rfm_filter = rfm_above_average[['Rcode', 'Fcode', 'Mcode']]


validation_filtered = validation_df.merge(rfm_filter, on=['Rcode', 'Fcode', 'Mcode'], how='inner')


response_rate_validation = validation_filtered['Florence'].mean()
response_rate_validation

twice_overall_rate = 2 * overall_response_rate_train

# Segment 1
segment_1 = rfm_response_rates_train[rfm_response_rates_train['Florence'] > twice_overall_rate]

# Segment 2
segment_2 = rfm_response_rates_train[(rfm_response_rates_train['Florence'] > overall_response_rate_train) &
                                     (rfm_response_rates_train['Florence'] <= twice_overall_rate)]

# Segment 3
segment_3 = rfm_response_rates_train[rfm_response_rates_train['Florence'] <= overall_response_rate_train]

# Count the number of entries in each segment
len(segment_1), len(segment_2), len(segment_3)

import matplotlib.pyplot as plt

def calculate_cumulative_response(df, segment):
    segment_df = df.merge(segment[['Rcode', 'Fcode', 'Mcode']], on=['Rcode', 'Fcode', 'Mcode'], how='inner')
    buyers = segment_df['Florence'].sum()
    total = len(segment_df)
    return total, buyers


total_1, buyers_1 = calculate_cumulative_response(validation_df, segment_1)
total_2, buyers_2 = calculate_cumulative_response(validation_df, segment_2)
total_3, buyers_3 = calculate_cumulative_response(validation_df, segment_3)


cumulative_totals = [total_1, total_1 + total_2, total_1 + total_2 + total_3]
cumulative_buyers = [buyers_1, buyers_1 + buyers_2, buyers_1 + buyers_2 + buyers_3]


plt.figure(figsize=(10, 6))
plt.plot(cumulative_totals, cumulative_buyers, marker='o', linestyle='-', color='b')
plt.title('Lift Curve')
plt.xlabel('Number of Customers')
plt.ylabel('Cumulative Number of Buyers')
plt.grid(True)
plt.show()

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


predictors = ['R', 'F', 'M', 'FirstPurch', 'Related Purchase']
scaler = StandardScaler()

train_features = scaler.fit_transform(train_df[predictors])
validation_features = scaler.transform(validation_df[predictors])


train_target = train_df['Florence']
validation_target = validation_df['Florence']


def apply_knn(k_values, train_features, train_target, validation_features, validation_target):
    accuracies = []
    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(train_features, train_target)
        predictions = knn.predict(validation_features)
        accuracy = accuracy_score(validation_target, predictions)
        accuracies.append(accuracy)
    return accuracies

# for k = 1 to 11
k_values = range(1, 12)
knn_accuracies = apply_knn(k_values, train_features, train_target, validation_features, validation_target)


plt.figure(figsize=(10, 6))
plt.plot(k_values, knn_accuracies, marker='o', linestyle='-', color='b')
plt.title('k-NN Accuracy for Different k Values')
plt.xlabel('k Value')
plt.ylabel('Accuracy')
plt.xticks(k_values)
plt.grid(True)
plt.show()

best_k = k_values[knn_accuracies.index(max(knn_accuracies))]
best_accuracy = max(knn_accuracies)

best_k, best_accuracy

knn_best = KNeighborsClassifier(n_neighbors=best_k)
knn_best.fit(train_features, train_target)
predictions_best_k = knn_best.predict(validation_features)


predicted_probabilities = knn_best.predict_proba(validation_features)[:, 1]


validation_results = validation_df.copy()
validation_results['predicted_probability'] = predicted_probabilities
validation_results['predicted_purchase'] = predictions_best_k


validation_results_sorted = validation_results.sort_values(by='predicted_probability', ascending=False)


cumulative_gains = validation_results_sorted['Florence'].cumsum()
cumulative_total = range(1, len(validation_results_sorted) + 1)


plt.figure(figsize=(10, 6))
plt.plot(cumulative_total, cumulative_gains, marker='o', linestyle='-', color='b')
plt.title('Lift Curve for k-NN Model (k=10)')
plt.xlabel('Number of Customers Targeted')
plt.ylabel('Cumulative Number of Buyers')
plt.grid(True)
plt.show()

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


full_predictors = ['Gender', 'M', 'R', 'F', 'FirstPurch', 'ChildBks', 'YouthBks',
                   'CookBks', 'DoItYBks', 'RefBks', 'ArtBks', 'GeogBks',
                   'ItalCook', 'ItalAtlas', 'ItalArt', 'Related Purchase']


subset_predictors = ['R', 'F', 'M', 'ArtBks', 'RefBks', 'Related Purchase']


rfm_predictors = ['R', 'F', 'M']


def fit_logistic_regression(features, target):
    model = LogisticRegression(max_iter=1000, random_state=1)
    model.fit(features, target)
    return model


model_full = fit_logistic_regression(train_df[full_predictors], train_target)
model_subset = fit_logistic_regression(train_df[subset_predictors], train_target)
model_rfm = fit_logistic_regression(train_df[rfm_predictors], train_target)


auc_full = roc_auc_score(validation_target, model_full.predict_proba(validation_df[full_predictors])[:, 1])
auc_subset = roc_auc_score(validation_target, model_subset.predict_proba(validation_df[subset_predictors])[:, 1])
auc_rfm = roc_auc_score(validation_target, model_rfm.predict_proba(validation_df[rfm_predictors])[:, 1])

auc_full, auc_subset, auc_rfm

import numpy as np


def cumulative_gains(model, features, actual):
    probabilities = model.predict_proba(features)[:, 1]
    indices = np.argsort(probabilities)[::-1]
    sorted_actual = actual.values[indices]
    gains = np.cumsum(sorted_actual)
    percentages = gains / sum(actual)
    return percentages


cumulative_gains_full = cumulative_gains(model_full, validation_df[full_predictors], validation_target)
cumulative_gains_subset = cumulative_gains(model_subset, validation_df[subset_predictors], validation_target)
cumulative_gains_rfm = cumulative_gains(model_rfm, validation_df[rfm_predictors], validation_target)


random_gains = np.cumsum(np.sort(validation_target.values)[::-1]) / sum(validation_target)


percentages = np.linspace(0, 1, len(validation_target))


plt.figure(figsize=(10, 6))
plt.plot(percentages, cumulative_gains_full, label='Full Model', color='blue')
plt.plot(percentages, cumulative_gains_subset, label='Subset Model', color='green')
plt.plot(percentages, cumulative_gains_rfm, label='RFM Model', color='red')
plt.plot(percentages, random_gains, label='Random Selection', color='black', linestyle='--')
plt.title('Cumulative Gains Chart')
plt.xlabel('Percentage of Customers Targeted')
plt.ylabel('Cumulative Gain')
plt.legend()
plt.grid(True)
plt.show()

purchase_probabilities_full = model_full.predict_proba(validation_df[full_predictors])[:, 1]


predictions_df = validation_df.copy()
predictions_df['purchase_probability'] = purchase_probabilities_full
predictions_df['actual_purchase'] = validation_target


predictions_df[['purchase_probability', 'actual_purchase']].head()

targeted_customers = predictions_df[predictions_df['purchase_probability'] >= 0.3]


targeted_count = targeted_customers.shape[0]
targeted_count

actual_purchases = targeted_customers['actual_purchase'].sum()
actual_purchases

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Define a function to evaluate model performance
def evaluate_model_performance(model, X, y_true):
    y_pred = model.predict(X)
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    return accuracy, precision, recall, f1

# Evaluate logistic regression model performance with balanced class weights
log_reg_full_balanced = LogisticRegression(class_weight='balanced')
log_reg_full_balanced.fit(X_train, y_train)
log_reg_full_accuracy_balanced, log_reg_full_precision_balanced, log_reg_full_recall_balanced, log_reg_full_f1_balanced = evaluate_model_performance(log_reg_full_balanced, X_validation, y_validation)
print("Logistic Regression (Full Set) Model Performance with Balanced Class Weights:")
print(f"Accuracy: {log_reg_full_accuracy_balanced:.4f}")
print(f"Precision: {log_reg_full_precision_balanced:.4f}")
print(f"Recall: {log_reg_full_recall_balanced:.4f}")
print(f"F1-score: {log_reg_full_f1_balanced:.4f}")
print()

# Revisit feature selection and use RFM variables
log_reg_rfm_balanced = LogisticRegression(class_weight='balanced')
log_reg_rfm_balanced.fit(X_train[['R', 'F', 'M']], y_train)
log_reg_rfm_accuracy_balanced, log_reg_rfm_precision_balanced, log_reg_rfm_recall_balanced, log_reg_rfm_f1_balanced = evaluate_model_performance(log_reg_rfm_balanced, X_validation[['R', 'F', 'M']], y_validation)
print("Logistic Regression (RFM Variables) Model Performance with Balanced Class Weights:")
print(f"Accuracy: {log_reg_rfm_accuracy_balanced:.4f}")
print(f"Precision: {log_reg_rfm_precision_balanced:.4f}")
print(f"Recall: {log_reg_rfm_recall_balanced:.4f}")
print(f"F1-score: {log_reg_rfm_f1_balanced:.4f}")
print()

# Tune model hyperparameters
from sklearn.model_selection import GridSearchCV

param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100]}  # Example grid of hyperparameters to tune

log_reg_rfm_tuned = LogisticRegression(class_weight='balanced')
grid_search = GridSearchCV(log_reg_rfm_tuned, param_grid, cv=5, scoring='f1')
grid_search.fit(X_train[['R', 'F', 'M']], y_train)
best_params = grid_search.best_params_
best_log_reg_rfm = grid_search.best_estimator_

# Evaluate the best tuned model
log_reg_rfm_tuned_accuracy, log_reg_rfm_tuned_precision, log_reg_rfm_tuned_recall, log_reg_rfm_tuned_f1 = evaluate_model_performance(best_log_reg_rfm, X_validation[['R', 'F', 'M']], y_validation)
print("Tuned Logistic Regression (RFM Variables) Model Performance with Balanced Class Weights:")
print(f"Best Parameters: {best_params}")
print(f"Accuracy: {log_reg_rfm_tuned_accuracy:.4f}")
print(f"Precision: {log_reg_rfm_tuned_precision:.4f}")
print(f"Recall: {log_reg_rfm_tuned_recall:.4f}")
print(f"F1-score: {log_reg_rfm_tuned_f1:.4f}")
print()