import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn import svm

X = np.array([[4,4],  # class A (+)
              [4,2],  # class A (+)
              [1,2],  # class A (+)
              [4,2],  # class A (+)
              [4,-4], # class B (-)
              [0,0],  # class B (-)
              [0,0],  # class B (-)
              [4,-2]])# class B (-)

y = [1,1,1,1,0,0,0,0]

clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(X,y)

w = clf.coef_[0]
print('{}: {}'.format("clf.coef_[0] (w)", w))
print('{}: {}'.format("clf.intercept_[0]", clf.intercept_[0]))
print('{}: {}'.format("number of support vectors for each class:", clf.n_support_))
print('{}: {}'.format("support vectors", clf.support_vectors_))
print()

a = -w[0] / w[1]
print('{} {}'.format("a:", a))

test_point = [[0,-1]]
print('{} {} --> class {}'.format("predicting point:", test_point, clf.predict(test_point)))

xx = np.linspace(0,4)
yy = a * xx - clf.intercept_[0] / w[1]

h0 = plt.plot(xx, yy, 'k-', label="non weighted div")

plt.scatter(X[:, 0], X[:, 1], c = y)
plt.legend()
plt.show()

