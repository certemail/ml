from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt 

def main():
    print("hw2")

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

    # 1-nearest neighbor
    print("")
    print("running 1-nearest neighbor...")
    clf = KNeighborsClassifier(n_neighbors=1)
    

if __name__ == '__main__':
    main()
