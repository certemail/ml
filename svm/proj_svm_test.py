import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn import svm

X =    [[ 4,  4,  3 ],  
        [ 4,  2,  3 ],  
        [ 1,  2,  3 ],  
        [ 4,  2,  3 ],  
        [ 4, -4,  3 ],  
        [ 0,  0,  3 ],  
        [ 0,  0,  3 ],  
        [ 4, -2,  3 ]]  

# three classes
y = [1,2,1,1,0,2,0,2]

# convert X to numpy ndarray
X = np.array(X)

# print original dataset feature values
print("dataset:")
print(X)
print()

clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(X,y)
print('{} {}'.format("clf:", clf))

w = clf.coef_[0]
print('{}: {}'.format("clf.coef_[0] (w)", w))
print('{}: {}'.format("clf.intercept_[0]", clf.intercept_[0]))
print('{}: {}'.format("number of support vectors for each class:", clf.n_support_))
print('{}: {}'.format("support vectors", clf.support_vectors_))
print()

#a = -w[0] / w[1]
#print('{} {}'.format("a:", a))
#
#test_point_1 = [[ 0, -1 ]]
#test_point_2 = [[ 1,  2 ]]
#test_point_3 = [[ 2,  3 ]]
#print('{} {} --> class {}'.format("predicting point:", test_point_1, clf.predict(test_point_1)))
#print('{} {} --> class {}'.format("predicting point:", test_point_2, clf.predict(test_point_2)))
#print('{} {} --> class {}'.format("predicting point:", test_point_3, clf.predict(test_point_3)))

#xx = np.linspace(0,4)
#yy = a * xx - clf.intercept_[0] / w[1]
#
#h0 = plt.plot(xx, yy, 'k-', label="non weighted div")
#
#plt.scatter(X[:, 0], X[:, 1], c = y)
#plt.legend()
#plt.show()

