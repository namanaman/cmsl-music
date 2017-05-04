import numpy as np
import pandas as pd
import csv

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model
from sklearn.svm import LinearSVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import RFE

def getData(modelType, filename):
    df = pd.read_csv(filepath_or_buffer=filename, delimiter=",", header=None)
    data = df.values

    if modelType == 'regression':
        y_data = data[1:,2] # Song year
    elif modelType == 'classifier':
        y_data = data[1:,3] # Popularity label

    x_data = np.delete(data, [0,1,2,3], axis=1)
    x_data = np.delete(x_data, [0], axis=0)
    #x_data = data[1:,[4, 56, 73]]

    return x_data, y_data

def model(modelType, filename):
    X, y = getData(modelType, filename)

    if modelType == 'regression':
        mod = LinearSVC(C=0.01, penalty="l1", dual=False)
    elif modelType == 'classifier':
        #selector = SelectKBest(f_classif, k=8)
        #X = selector.fit_transform(X, y)
        #print(selector.get_support(indices=True))
        mod = GaussianNB()

    scores = cross_val_score(mod, X, y, cv=10)
    return scores.mean(), scores.std() * 2

if __name__ == "__main__":
    #mean, std = model('regression', 'datasets/liwc_decade.csv')
    mean, std = model('classifier', 'datasets/liwc_all.csv')
    #mean, std = model('classifier', 'datasets/liwc_rihanna.csv')
    #mean, std = model('classifier', 'datasets/liwc_drake.csv')

    print("Score: %0.2f (+/- %0.2f)" % (mean, std * 2))
