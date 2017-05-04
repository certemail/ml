import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn import svm
from sklearn.model_selection import cross_val_score


def display_accuracy(scores):
    print("cross validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))



#X = [[1,0,1,1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,0],
#     [1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,1,0,1,0,0,0,0,1,0], 
#     [0,0,1,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,0], 
#     [1,0,1,1,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
#     [1,1,1,1,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,1,1,1,0]]
#
#y = [0,3,2,1,0,1,1,2,3,2,1,0,0,1,2,1,2,1,0,1,0,1]
# convert X to numpy ndarray
#X = np.array(X)
N_SAMPLES = 100
N_FEATURES = 700
N_CLASSES = 4

X = np.random.random_integers(0, 1, (N_SAMPLES, N_FEATURES))
y = np.random.random_integers(0, N_CLASSES-1, N_SAMPLES)


# print original dataset feature values
print("dataset (X):")
print(X)
print('{}: {}'.format("length of feature vector", len(X[0])))
print()
print("classification (y):")
print(y)
print('{}: {}'.format("number of samples", len((y))))
print('{}: {}'.format("number of classes", len(set(y))))

print("*************\n")

# TODO account for unbalanced dataset (use 'class_weight')
clf = svm.SVC(kernel='linear', C = 1.0)

# cross validation score
scores = cross_val_score(clf, X, y, cv=10)
print("SCORES:")
print(scores)
display_accuracy(scores)
print()

clf.fit(X,y)
print('{} {}'.format("clf:", clf))
print()

w = clf.coef_[0]
print("clf.coef_[0] (w):")
print("feature vector length: " + str(len(clf.coef_[0])))
print(w)
print()

print('{}: {}'.format("clf.intercept_[0]", clf.intercept_[0]))

print('{}: {}'.format("number of classes", len(clf.n_support_)))
print('{}: {}'.format("number of support vectors for each class:", clf.n_support_))

print("support vectors:")
print(clf.support_vectors_)
print()

# predict
#print("Make predictions...(testing on same rows in X)")
#print(clf.predict( [[1,0,1,1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,0]] )) 
#print(clf.predict( [[1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,1,0,1,0,0,0,0,1,0]] ))
#print(clf.predict( [[0,0,1,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,0]] ))
#print(clf.predict( [[1,0,1,1,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0]] ))
#print(clf.predict( [[0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1]] ))
#print(clf.predict( [[1,1,1,1,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,1,1,1,0]] ))
#print
#print("correct classifications: ")
#print(y)
