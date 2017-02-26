from sklearn import tree
from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt 
from io import StringIO
from sklearn.linear_model import LogisticRegression
import pydotplus

def display_accuracy(scores):
    print("cross validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

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
    print("RUNNING 1-NEAREST NEIGHBOR...")
    clf = KNeighborsClassifier(n_neighbors=1)
    scores = cross_val_score(clf, X_digits, y_digits, cv=10)
    print("cross_val_scores for 1-nearest neighbor:")
    [print("\t" + str(s)) for s in scores]
    display_accuracy(scores)
#---run_nearest_neighbor---------------------------------

	
def run_decision_tree(X_digits, y_digits):
    print("RUNNING DECISION TREE...")
    clf = DecisionTreeClassifier("entropy")
    scores = cross_val_score(clf, X_digits, y_digits, cv=10)
    print("cross_val_scores for decision tree: ")
    [print("\t" + str(s)) for s in scores]
    display_accuracy(scores)

    # fit digits dataset to the decision tree and display clf attributes
    clf.fit(X_digits, y_digits)
    print("classes_ : " + str(clf.classes_))    
    print("n_features_ : " + str(clf.n_features_))
    print("feature_importances_ : " + str(clf.feature_importances_))

    # display feature importance by pixel position
    print("pixel position | feature_importance")
    f_names = []
    rows, cols = 8, 8
    for i in range(rows):
        for j in range(cols):
            f_names.append("pix_pos_" + str(i) + ":" + str(j))

    for i in range(len(f_names)):
        print(str(f_names[i]) + "      " + str(clf.feature_importances_[i]))

    # print out decision tree
    dotfile = StringIO()
    tree.export_graphviz(clf, out_file = dotfile, 
                              feature_names = f_names, 
                              rounded = True, 
                              class_names = ['-', '+'])
    graph = pydotplus.graph_from_dot_data(dotfile.getvalue())
    graph.write_pdf("digits_tree.pdf")

#---run_decision_tree------------------------------------


def run_logistic_regression(X_digits, y_digits):
    print("RUNNING LOGISTIC REGRESSION...")
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
    #run_nearest_neighbor(X_digits, y_digits)
    print("--------------------------")
    
    # decision tree
    run_decision_tree(X_digits, y_digits)
    print("--------------------------")

    # logistic regression
    #run_logistic_regression(X_digits, y_digits)
    print("--------------------------")

if __name__ == '__main__':
    main()

# visualize
#plt.gray() 
#plt.matshow(digits.images[1796]) 
#plt.show()
