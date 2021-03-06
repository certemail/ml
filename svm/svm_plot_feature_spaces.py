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
    plt.xlim(-6.5, 6.5)
    plt.ylim(-6.5, 6.5)
    #plt.plot([0,2],[2,1])
    plt.title('Feature Space (x1,x2) --> ((x1)^2, (x1*x2)')
    plt.xlabel('x1 axis')
    plt.ylabel('x2 axis')
    plt.legend(loc='upper left')
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
    plt.title('Input Space (non-linearly separable)')
    plt.xlabel('x1 axis')
    plt.ylabel('x2 axis')
    plt.legend(loc='center left')
    plt.show()

def main():
    show_original_dataset()
    show_new_feature_space()

if __name__ == '__main__':
    main()
