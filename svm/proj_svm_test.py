import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn import svm

#X =    [[ 4,  4,  3,  4 ],  
#        [ 4,  2, -2,  2 ],  
#        [ 1,  2,  3,  2 ],  
#        [ 4,  2,  3,  2 ],  
#        [ 4, -4,  2, -4 ],  
#        [ 0,  0,  3,  0 ],  
#        [ 0,  0,  1,  0 ],  
#        [ 4, -2, -3, -2 ]]  
#
#y = [1,2,3,1,0,2,0,3]

X = [[1,0,1,1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,0],
     [1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,1,0,1,0,0,0,0,1,0], 
     [0,0,1,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,0], 
     [1,0,1,1,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0],
     [0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1],
     [1,1,1,1,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,1,1,1,0]]

y = [0,3,2,1,0,1]
# convert X to numpy ndarray
X = np.array(X)

# print original dataset feature values
print("dataset (X):")
print(X)
print('{}: {}'.format("length of feature vector", len(X[0])))
print()
print("classification (y):")
print(y)
print('{}: {}'.format("number of classes", len(set(y))))

print("*************\n")

clf = svm.SVC(kernel='linear', C = 1.0)
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
print("Make predictions...(testing on same rows in X)")
print(clf.predict( [[1,0,1,1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,0]] )) 
print(clf.predict( [[1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,1,0,1,0,0,0,0,1,0]] ))
print(clf.predict( [[0,0,1,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,0]] ))
print(clf.predict( [[1,0,1,1,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0]] ))
print(clf.predict( [[0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1]] ))
print(clf.predict( [[1,1,1,1,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,1,1,1,0]] ))
print
print("correct classifications: ")
print(y)
