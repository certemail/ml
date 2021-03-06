import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn import svm

X =    [[ 4,  4 ],  # class A (+)
        [ 4,  2 ],  # class A (+)
        [ 1,  2 ],  # class A (+)
        [ 4,  2 ],  # class A (+)
        [ 4, -4 ],  # class B (-)
        [ 0,  0 ],  # class B (-)
        [ 0,  0 ],  # class B (-)
        [ 4, -2 ]]  # class B (-)

y = [1,1,1,1,0,0,0,0]

# convert X to numpy ndarray
X = np.array(X)

clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(X,y)

w = clf.coef_[0]
print('{}: {}'.format("clf.coef_[0] (weights)", w))
print('{}: {}'.format("clf.intercept_[0]", clf.intercept_[0]))
print('{}: {}'.format("number of support vectors for each class", clf.n_support_))
print('{}: {}'.format("support vectors", clf.support_vectors_))
print()

a = -w[0] / w[1]
print('{} {}'.format("a (slope):", a))

test_point_1 = [[ 0, -1 ]]
test_point_2 = [[ 1,  2 ]]
test_point_3 = [[ 2,  3 ]]
print('{} {} --> class {}'.format("predicting point:", test_point_1, clf.predict(test_point_1)))
print('{} {} --> class {}'.format("predicting point:", test_point_2, clf.predict(test_point_2)))
print('{} {} --> class {}'.format("predicting point:", test_point_3, clf.predict(test_point_3)))

xx = np.linspace(0,6)
yy = a * xx - clf.intercept_[0] / w[1]

h0 = plt.plot(xx, yy, 'k-', label='Hyperplane' )

plt.scatter(X[:, 0], X[:, 1], c = y)
plt.title('Feature Space (x1,x2) --> ((x1)^2, (x1*x2)')
plt.xlabel('x1 axis')
plt.ylabel('x2 axis')
plt.legend()
plt.show()

