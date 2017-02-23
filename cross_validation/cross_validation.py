from sklearn.datasets import load_digits
from sklearn.preprocessing import label_binarize
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt 

def main():

    digits = load_digits()
    print("digits.data.shape: " + str(digits.data.shape))
    print("digits.data: ")
    print(digits.data)
    print("digits.target: ")
    print(digits.target)
    
    # visualize
    #plt.gray() 
    #plt.matshow(digits.images[1796]) 
    #plt.show()

    # convert class labels to be 1 if digit is 9; 0 for all other digits
    #binarized_digits = label_binarize([9], digits.target)
    binarized_digits = []
    for i in range(len(digits.target)):
        if digits.target[i] == 9:
            binarized_digits.append(9)
        else:
            binarized_digits.append(0)
    #print(len(binarized_digits))
    #print(binarized_digits)

    # 1-nearest neighbor
    print("")
    print("running 1-nearest neighbor...")
    clf = KNeighborsClassifier(n_neighbors=1)
    scores = cross_val_score(clf, digits.data, binarized_digits, cv=10)

    print("cross_val_scores for 1-nearest neighbor: " + str(scores))
    

if __name__ == '__main__':
    main()
