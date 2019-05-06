import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
#from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

X = pd.read_csv("dataSetOriginal/articles1.csv")
Y = pd.read_csv("dataSetOriginal/articles2.csv")
Z = pd.read_csv("dataSetOriginal/articles3.csv")
publication = []
content = []

for index, row in X.iterrows():
    if (row['publication'] == "New York Times" or row['publication'] == "Breitbart" or row['publication'] == "CNN" or row['publication'] == "Business Insider"):
        publication.append(row['publication'])
        content.append(row['content'])
#print(len(publication))

for index, row in Y.iterrows():
    if (row['publication'] == "New York Post" or row['publication'] == "Atlantic" or row['publication'] == "National Review" or row['publication'] == "Talking Points Memo"):
        publication.append(row['publication'])
        content.append(row['content'])
#print(len(publication))

for index, row in Z.iterrows():
    if (row['publication'] == "NPR" or row['publication'] == "Washington Post" or row['publication'] == "Reuters" or row['publication'] == "VOX"):
        publication.append(row['publication'])
        content.append(row['content'])

#print(len(publication))
            
#publication_train, publication_test = train_test_split(publication, test_size=0.33,train_size = 0.67, random_state=42)
#content_train, content_test = train_test_split(content, test_size=0.33,train_size = 0.67, random_state=42)

#print(len(publication_test))
rev_train, rev_test, labels_train, labels_test =  train_test_split(content, publication)

counter = CountVectorizer()
counter.fit(rev_train)

counts_train = counter.transform(rev_train)#transform the training data
counts_test = counter.transform(rev_test)#transform the testing data

#clf = MultinomialNB()
# clf = MLPClassifier(solver='adam' ,alpha=1e-7,hidden_layer_sizes=(4,),max_iter=32,random_state=9,power_t=1) # 64% accuracy

#train all classifier on the same datasets


KNN_classifier=KNeighborsClassifier()
LREG_classifier=LogisticRegression()
DT_classifier = DecisionTreeClassifier()

predictors=[('knn',KNN_classifier),('lreg',LREG_classifier),('dt',DT_classifier)]

VT=VotingClassifier(predictors)



#=======================================================================================
#build the parameter grid
KNN_grid = [{'n_neighbors': [1,3,5,7,9,11,13,15,17], 'weights':['uniform','distance']}]

#build a grid search to find the best parameters
gridsearchKNN = GridSearchCV(KNN_classifier, KNN_grid, cv=5)

#run the grid search
gridsearchKNN.fit(counts_train,labels_train)

#=======================================================================================

#build the parameter grid
DT_grid = [{'max_depth': [3,4,5,6,7,8,9,10,11,12],'criterion':['gini','entropy']}]

#build a grid search to find the best parameters
gridsearchDT  = GridSearchCV(DT_classifier, DT_grid, cv=5)

#run the grid search
gridsearchDT.fit(counts_train,labels_train)

#=======================================================================================

#build the parameter grid
LREG_grid = [ {'C':[0.5,1,1.5,2],'penalty':['l1','l2']}]

#build a grid search to find the best parameters
gridsearchLREG  = GridSearchCV(LREG_classifier, LREG_grid, cv=5)

#run the grid search
gridsearchLREG.fit(counts_train,labels_train)

#=======================================================================================

#clf.fit(counts_train,labels_train)

#VT.fit(counts_train,labels_train)


#use the VT classifier to predict
pred=VT.predict(counts_test)

#use hard voting to predict (majority voting)
#pred=clf.predict(counts_test)

#print accuracy
print (accuracy_score(pred,labels_test))
            
            
#print(type(rev_train))