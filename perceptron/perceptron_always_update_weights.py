import random

MAX_ITER = 100 
D = 2
ACTUAL_IDX = D #last index in each example array

#data_set = [[2,6,-1],[1,3,1],[3,9,1]]    # linearly inseparable
#data_set = [[1,2,1],[1,3,1],[3,1,-1]]   # linearly separable
#data_set = [[1,2,-1],[1,3,-1],[3,1,1]]   # linearly separable

'''
data_set = [[1,1,-1],
            [1,2,-1],
            [1,3,-1],
            [2,2,-1],
            [2,3,-1],
            [3,1,1],
            [4,1,1],
            [4,2,1],
            [5,2,1]]
'''
# this is the above data_set just shuffled
data_set = [[3, 1, 1], [1, 1, -1], [1, 2, -1], [1, 3, -1], [4, 2, 1], [5, 2, 1], [2, 2, -1], [4, 1, 1], [2, 3, -1]]

def calculate_hyperplane_slope(weights, bias):
    if weights[1] == 0:
        print("      division by zero for w2")
    else:
        slope = -(float(weights[0]) / float(weights[1])) # -w1/w2
        y_int = -(float(bias) / float(weights[1]))
        print("      slope [m] = " + str(slope) + " , y_int = " + str(y_int))

if __name__ == '__main__':
    print("data_set : " + str(data_set))
    #random.shuffle(data_set)
    #print("data_set (shuffled): " + str(data_set))
    
    # initialize weights and bias to zero
    weights = []
    for i in range(D):
        weights.append(0)
    bias = 0
    print("initial weights: " + str(weights))
    print("intial bias: " + str(bias))

    NUM_WRONG = 0
    NUM_TOTAL_ITERATIONS = 0
    for i in range(MAX_ITER):
        NUM_CORRECT = 0 
        for x_input_vector in data_set:

            # compute activation for this input vector
            activation = 0
            for j in range(D):
                activation += weights[j] * x_input_vector[j] # dot product of weights and input vector
            activation = activation + bias
            print("**data point: " + str(x_input_vector)) 
            print("  weights:    " + str(weights) + ", bias: " + str(bias))			

            y_actual = x_input_vector[ACTUAL_IDX]
            print("    activation = " + str(activation) +  ",  y_actual = " + str(y_actual))

            # ALWAYS UPDATE WEIGHTS AND BIAS
            if True:
                for k in range(D):
                    weights[k] = weights[k] + (y_actual * x_input_vector[k])
                bias = bias + y_actual
                if (y_actual * activation) <= 0:
                    print("    MISCLASSIFIED")
                    NUM_WRONG += 1
                    calculate_hyperplane_slope(weights, bias)
                else:
                    print("    CORRECT")
                    NUM_CORRECT +=1
                    calculate_hyperplane_slope(weights, bias)
                print("    ALWAYS UPDATE --> updated weights and bias are now: " + str(weights) + ", bias = " + str(bias))
            
        NUM_TOTAL_ITERATIONS += 1

        # converge if no errors after iterating over entire data set once
        if NUM_CORRECT == len(data_set):
            print("/// CONVERGED ///")
            break;
        print("----------------------------------------")

    print("================================================")
    print("FINAL WEIGHTS: " + str(weights) + ", FINAL BIAS: " + str(bias))
    print("# MISCLASSIFICATIONS: " + str(NUM_WRONG))
    print("# TOTAL ITERATIONS: " +  str(NUM_TOTAL_ITERATIONS))
    
    calculate_hyperplane_slope(weights, bias)
    # dot product: sum(i[0] * i[1] for i in zip(v1,v2))
