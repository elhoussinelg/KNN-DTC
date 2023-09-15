import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree
from joblib import dump
import numpy as np
import random
import matplotlib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from joblib import dump
# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

import numpy as np
import random
from sklearn.model_selection import train_test_split, cross_val_score, validation_curve, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn import tree
from joblib import dump
import matplotlib.pyplot as plt

def getData():
    """ loads, shuffles, categorizes and splits data

    Returns:
        [type] [description]
        X_train [np.ndarray]: attribute values of train data
        X_test [np.ndarray]: attribute values of test data
        y_train [np.ndarray]: class labels of train data
        y_test [np.ndarray]: class labels of test data
    """

    # read data
    with open(r"C:\Users\TOSHIBA\PycharmProjects\test\ML\Cloud\storage\data\data.csv", "r") as file_object:
        raw_data = file_object.read().split('\n')

    # remove empty string
    raw_data = [x for x in raw_data if x]

    # split each row from ','
    splitted_data = []
    for i in raw_data:
        splitted_data += [list(map(int, i.split(',')))]

    random.shuffle(splitted_data)

    # categorize attributes
    for i in range(len(splitted_data)):
        if splitted_data[i][1] <= 100:
            splitted_data[i][1] = 0
        else:
            splitted_data[i][1] = 1

        if splitted_data[i][2] <= 10:
            splitted_data[i][2] = 0
        else:
            splitted_data[i][2] = 1

    data = np.array(splitted_data)

    X_train, X_test, y_train, y_test = train_test_split(list(data[:,0:4]), list(data[:,4]), test_size=0.3, random_state=42)

    return X_train, X_test, y_train, y_test

if __name__ == '__main__':
    """ start point of the Clout System,
        creates model, trains it and stores it in the Clout storage

    """

   ###################################KNN model#########################################################
    # get cleaned and splitted data
    X_train, X_test, y_train, y_test = getData()

    # create a KNN model
    param_grid = {'n_neighbors': np.arange(1,20), 'metric':['euclidean','manhattan']}
    grid = GridSearchCV(KNeighborsClassifier(),param_grid, cv=20)
    grid.fit(X_train, y_train)
    print("score is : ", grid.best_score_)
    print(" best_params_is : ", grid.best_params_)
    #print(" best_estimator is : ", grid.best_estimator_)
    #print("confusion_matrix: " ,confusion_matrix(y_test, grid.predict(X_test)))
############################################decision tree model#############################################################
    # create a decision tree model
    model2 = tree.DecisionTreeClassifier()
    # train the model
    model2.fit(X_train, y_train)
    print("DTC : ",model2.score(X_test, y_test))

    # Choisir le meilleur modèle entre KNN et Decision Tree
    best_model = grid if grid.best_score_ > model2.score(X_test, y_test) else model2
    print("le meilleur modèle entre KNN et DTC: ", best_model)

    # store model1 in the cloud storage
    dump(best_model, r'C:\Users\TOSHIBA\PycharmProjects\test\ML\Cloud\storage\best_model.joblib')
    # store model in the cloud storage
    #dump(model2, r'C:\Users\TOSHIBA\PycharmProjects\test\ML\Cloud\storage\TDC.joblib')