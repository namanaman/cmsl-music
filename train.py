import numpy as np
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import VarianceThreshold
from sklearn import linear_model

def getData(fileType):
    df = pd.read_csv(filepath_or_buffer='datasets/liwc_decade.csv', delimiter=",", header=None)
    data = df.values

    if fileType == 'decade':
        y_data = data[1:,2]
    else:
        y_data = data[1:,3]

    x_data = np.delete(data, [0,1,2,3], axis=1)
    x_data = np.delete(x_data, [0], axis=0)
    return x_data, y_data

def train(fileType):
    X, y = getData(fileType)
    #X = SelectKBest(f_classif, k=10).fit_transform(X, y)
    #X = VarianceThreshold(threshold=0.95).fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    if fileType == 'decade':
        clf = linear_model.LinearRegression()
    else:
        clf = GaussianNB()
        
    clf.fit(X_train, y_train)
    train_accuracy = clf.score(X_train, y_train)
    test_accuracy = clf.score(X_test, y_test)
    print("Training accuracy: {}".format(train_accuracy))
    print("Testing accuracy: {}".format(test_accuracy))

train('decade')
