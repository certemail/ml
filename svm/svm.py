from matplotlib import pyplot as plt
from matplotlib import style

style.use('ggplot')


def show_new_feature_space():
    # class A
    x1_A =  [  4,  4,  1,  4  ]
    x2_A =  [  4,  2,  2,  2  ]
    
    # class B
    x1_B =  [  4,  0,  0,  4  ]
    x2_B =  [ -4,  0,  0, -2  ]
    
    plt.scatter(x1_A, x2_A, label='class A', color='b')
    plt.scatter(x1_B, x2_B, label='class B', color='r')
    plt.title('svm - new feature space')
    plt.xlabel('x1 axis')
    plt.ylabel('x2 axis')
    plt.legend(loc='center')
    plt.show()

def show_original_dataset():
    # class A
    x1_A =  [  2, -2,  1,  2  ]
    x2_A =  [  2, -1,  2,  1  ]
    
    # class B
    x1_B = [  -2,  0,  0,  2  ]
    x2_B = [   2,  2, -1, -1  ]
    
    plt.scatter(x1_A, x2_A, label='class A', color='b')
    plt.scatter(x1_B, x2_B, label='class B', color='r')
    plt.title('svm - non-linearly separable')
    plt.xlabel('x1 axis')
    plt.ylabel('x2 axis')
    plt.legend(loc='center')
    plt.show()

def main():
    show_original_dataset()
    show_new_feature_space()

if __name__ == '__main__':
    main()
