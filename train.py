import numpy as np
import pandas as pd
import csv

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import cross_val_score

def getData(modelType, filename):
    df = pd.read_csv(filepath_or_buffer=filename, delimiter=",", header=None)
    data = df.values

    if modelType == 'regression':
        y_data = data[1:,2] # Song year
    elif modelType == 'classifier':
        y_data = data[1:,3] # Popularity label

    x_data = np.delete(data, [0,1,2,3], axis=1)
    x_data = np.delete(x_data, [0], axis=0)

    #x_data = data[1:,[4]] #WC only

    return x_data, y_data

def model(modelType, filename):
    X, y = getData(modelType, filename)
    #X = SelectKBest(f_classif, k=10).fit_transform(X, y)
    #X = VarianceThreshold(threshold=0.95).fit_transform(X)

    if modelType == 'regression':
        clf = linear_model.LinearRegression()
    elif modelType == 'classifier':
        #clf = GaussianNB()
        clf = SVC(kernel='linear')

    scores = cross_val_score(clf, X, y, cv=10)
    return scores.mean(), scores.std() * 2

if __name__ == "__main__":
    #Regression
    #mean, std = model('regression', 'datasets/liwc_decade.csv')

    #Classification
    mean, std = model('classifier', 'datasets/liwc_all.csv')
    #mean, std = model('regression', 'datasets/liwc_rihanna.csv')
    #mean, std = model('regression', 'datasets/liwc_drake.csv')

    print("Score: %0.2f (+/- %0.2f)" % (mean, std * 2))
