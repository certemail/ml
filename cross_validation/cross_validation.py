from sklearn.datasets import load_digits
from sklearn.preprocessing import label_binarize
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt 

'''convert class labels to be 1 if digit is 9; 0 for all other digits'''
def convert_class_labels(d):
    converted_digits = []
    for i in range(len(d.target)):
        if d.target[i] == 9:
            converted_digits.append(9)
        else:
            converted_digits.append(0)
    return converted_digits
#---convert_class_labels---------------------------------


def run_nearest_neighbor(digits):
    print("running 1-nearest neighbor...")
    clf = KNeighborsClassifier(n_neighbors=1)
    scores = cross_val_score(clf, digits.data, convert_class_labels(digits), cv=10)
    print("cross_val_scores for 1-nearest neighbor:")
    for i in range(len(scores)):
        print("\t" + str(scores[i]))
#---run_nearest_neighbor---------------------------------

	
def run_decision_tree(digits):
    print("running decision tree...")
    print("cross_val_scores for decision tree: ")
#---run_decision_tree------------------------------------


def run_logistic_regression(digits):
    print("running logistic regression...")
    print("cross_val_scores for logistic regression: ")
#---run_logistic_regression------------------------------------


def main():
    digits = load_digits()
    print("digits.data.shape: " + str(digits.data.shape))
    print("digits.data: ")
    print(digits.data)
    print("digits.target: ")
    print(digits.target)
    

    # 1-nearest neighbor
    print("--------------------------")
    run_nearest_neighbor(digits)
    print("--------------------------")
    
    # decision tree
    run_decision_tree(digits)
    print("--------------------------")

    # logistic regression
    run_logistic_regression(digits)
    print("--------------------------")

if __name__ == '__main__':
    main()

# visualize
#plt.gray() 
#plt.matshow(digits.images[1796]) 
#plt.show()
