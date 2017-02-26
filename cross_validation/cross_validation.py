from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt 

def display_accuracy(scores):
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

'''convert class labels to be 1 if digit is 9; 0 for all other digits'''
def convert_class_labels(d_target):
    converted_digits = []
    for i in range(len(d_target)):
        if d_target[i] == 9:
            converted_digits.append(1)
        else:
            converted_digits.append(0)
    return converted_digits
#---convert_class_labels---------------------------------


def run_nearest_neighbor(X_digits, y_digits):
    print("running 1-nearest neighbor...")
    clf = KNeighborsClassifier(n_neighbors=1)
    scores = cross_val_score(clf, X_digits, y_digits, cv=10)
    print("cross_val_scores for 1-nearest neighbor:")
    [print("\t" + str(s)) for s in scores]
    display_accuracy(scores)
#---run_nearest_neighbor---------------------------------

	
def run_decision_tree(X_digits, y_digits):
    print("running decision tree...")
    clf = DecisionTreeClassifier()
    scores = cross_val_score(clf, X_digits, y_digits, cv=10)
    print("cross_val_scores for decision tree: ")
    [print("\t" + str(s)) for s in scores]
    display_accuracy(scores)
#---run_decision_tree------------------------------------


def run_logistic_regression(X_digits, y_digits):
    print("running logistic regression...")
    clf = LogisticRegression()
    scores = cross_val_score(clf, X_digits, y_digits, cv=10)
    print("cross_val_scores for logistic regression: ")
    [print("\t" + str(s)) for s in scores]
    display_accuracy(scores)

    clf.fit(X_digits, y_digits)
    print("coefficients: " + str(clf.coef_))

#---run_logistic_regression------------------------------------


def main():
    digits = load_digits()
    print("digits.data.shape: " + str(digits.data.shape))
    print("digits.data: ")
    print(digits.data)
    print("digits.target: ")
    print(digits.target)
    print(convert_class_labels(digits.target).count(1))
    print(convert_class_labels(digits.target).count(0))

    X_digits, y_digits = digits.data, convert_class_labels(digits.target)

    # 1-nearest neighbor
    print("==========================")
    run_nearest_neighbor(X_digits, y_digits)
    print("--------------------------")
    
    # decision tree
    run_decision_tree(X_digits, y_digits)
    print("--------------------------")

    # logistic regression
    run_logistic_regression(X_digits, y_digits)
    print("--------------------------")

if __name__ == '__main__':
    main()

# visualize
#plt.gray() 
#plt.matshow(digits.images[1796]) 
#plt.show()
