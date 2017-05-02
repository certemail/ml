import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn import svm


#def my_kernel(X, y):
#    X_new = np.array([  [4,4],
#                        [4,2],
#                        [1,2],
#                        [4,2],
#                        [4,-4],
#                        [0,0],
#                        [0,0],
#                        [4,-2]])
#    y_new = y
#    return(X_new, y)


X = np.array([  [2,2],
                [-2,-1],
                [1,2],
                [2,1],
                [-2,2],
                [0,2],
                [0,-1],
                [2,-1]])

y = [0,0,0,0,1,1,1,1]

clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(X,y)

w = clf.coef_[0]
print(w)
print(clf.intercept_[0])

a = -w[0] / w[1]

xx = np.linspace(0,4)
yy = a * xx - clf.intercept_[0] / w[1]

h0 = plt.plot(xx, yy, 'k-', label="non weighted div")

plt.scatter(X[:, 0], X[:, 1], c = y)
plt.legend()
plt.show()

