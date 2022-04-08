# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 21:10:02 2022

@author: DELL
"""

### Multinomial Regression ####
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.model_selection import cross_val_score
#Importing Data
mode = pd.read_csv(r"C:\Users\DELL\Desktop\Project\df_emotional.csv")

mode['EmotionalScore'].replace('Expected', 0 , inplace=True)
mode['EmotionalScore'].replace('Borderline', 1 , inplace=True)
mode['EmotionalScore'].replace('Significant', 2 , inplace=True)

# Correlation values between each independent features
s=mode.corr()


###################### Feature Selection #########################
###Recursive Feature Elimination(RFE) and ExtraTreesClassifier are used


#ExtraTreesClassifier method gives importance of each attribute
from sklearn.ensemble import ExtraTreesClassifier
ml = ExtraTreesClassifier()
ml.fit(mode.iloc[:, :24], mode.iloc[:,-1:])
# display the relative importance of each attribute
print(ml.feature_importances_)

# Recursive Feature Elimination(RFE)
'''This method gives top N features that have importance 
by giving support as true if the feature is in top 4 else false
and also ranking as 1 if the feature is in top 4 else numbers will be given
according to priority.
'''
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

# create a base classifier used to evaluate a subset of attributes
C=10
ml2 =LogisticRegression(C=C, penalty='l2',solver='saga',multi_class='multinomial',max_iter=10000).fit(mode.iloc[:, :24], mode.iloc[:, -1:])

# create the RFE model and select 10 attributes
rfe = RFE(ml2, 1)
rfe = rfe.fit(mode.iloc[:, :24], mode.iloc[:,-1:])
# summarize the selection of the attributes
print(rfe.support_)
print(rfe.ranking_)
###############################################################################

mode.columns # column names
mode.drop(['PeopleInHome','age','breakfast','GadgetInWeek',"ConcentraionDays",'PlayOutside','SchoolCommunity','ChoicesOnThing','Family','Friends', 'Appearance', 'Life','IntouchWithFriends' , 'sleeptime'], axis=1, inplace=True)
d=mode.corr()

#mode.to_csv('df_emotional10.csv', index=False) #exporting cleaned dataframe

'''
Now we can drop the features which are not required and the proceed with
train test split and model building

'''
train, test = train_test_split(mode, test_size = 0.3)
train_X,train_y=train.iloc[:, :10], train.iloc[:,-1:]
test_X,test_y=test.iloc[:, :10], test.iloc[:,-1:]


##########################################APPROACH 1########################################################
#C=10
# ‘multinomial’ option is supported only by the ‘lbfgs’ and ‘newton-cg’ solvers
model = LogisticRegression(C=C, penalty='l2',solver='saga',multi_class='multinomial',max_iter=10000).fit(train.iloc[:, :24], train.iloc[:, -1:])

'''
cross_val_score is only useful to find at what value of k we get gud accuracy
#if we get gud accuracy at cv=5 then we have to write a code to divide the data in to
5 subsets and train the model 5 times to improve the performance
'''
score=cross_val_score(model,train.iloc[:, :10], train.iloc[:,-1:],cv=5,scoring = 'accuracy').mean()
print(score)


#X=mode.iloc[:, :24] #assigning all input variables to X dataframe
#y=mode.iloc[:,-1:] #assigning target variable to y dataframe
# k-fold cross validation

from sklearn.model_selection import KFold
scores = list()
C=10
kfold = KFold(n_splits=5, shuffle=True) #it means 5 folds
# enumerate splits
for train_ix, test_ix in kfold.split(train_X): 
    #in split function we have to mention input training data
	
	model = LogisticRegression(C=C, penalty='l2',solver='saga',multi_class='multinomial',max_iter=10000)
	model.fit(train_X.iloc[train_ix], train_y.iloc[train_ix])
	


test_predict = model.predict(test.iloc[:, :10]) # Test predictions

############F1-score##########
from sklearn.metrics import classification_report

target_names = ['class 0', 'class 1', 'class 2'] #labels which we ant to see in the gererated report
print(classification_report(test.iloc[:,-1:], test_predict, target_names=target_names))


# Test accuracy 
accuracy_score(test.iloc[:,-1:], test_predict)

train_predict = model.predict(train.iloc[:, :10]) # Train predictions 
# Train accuracy 
accuracy_score(train.iloc[:,-1:], train_predict) 


# saving the model
# importing pickle
import pickle
pickle.dump(model, open('model1.pkl', 'wb'))
mode.dtypes
###################################RANDOM FOREST##############################

from sklearn.ensemble import RandomForestClassifier

rf_clf = RandomForestClassifier(n_estimators=500, n_jobs=1, random_state=42)
#n_estimators means...500 randoms trees are generated based on subsample data...more the number..more the accuracy


rf_clf.fit(train_X, train_y)

z=rf_clf.predict(test_X)

from sklearn.metrics import accuracy_score, confusion_matrix

# Evaluation on Testing Data
confusion_matrix(test_y, rf_clf.predict(test_X))
accuracy_score(test_y, rf_clf.predict(test_X))

# Evaluation on Training Data
confusion_matrix(train_y, rf_clf.predict(train_X))
accuracy_score(train_y, rf_clf.predict(train_X))



######################################ONE vs REST Approach#################################################
from sklearn.metrics import roc_curve, auc
from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

X = mode.iloc[: , :10]
y= mode.iloc[: , -1:]
y = label_binarize(y, classes=[0,1,2])
n_classes = 3

# shuffle and split training and test sets
X_train, X_test, y_train, y_test =\
    train_test_split(X, y, test_size=0.33, random_state=0)

# classifier
clf = OneVsRestClassifier(LinearSVC(random_state=0))
##Fitting the model
clf.fit(X_train, y_train)

#Predicting the test
y_score=clf.decision_function(X_test)



# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Plot of a ROC curve for a specific class
for i in range(n_classes):
    plt.figure()
    plt.plot(fpr[i], tpr[i], label='ROC curve (area = %0.2f)' % roc_auc[i])
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

