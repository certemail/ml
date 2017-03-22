#!/usr/bin/env python


from sklearn import preprocessing
import numpy as np


# Training set
#data = [
#    [1, 0, 'r', 1],
#    [0, 0, 'b', 0],
#    [1, 1, 'g', 0],
#    [0, 0, 'g', 0],
#    [1, 1, 'b', 1],
#    [0, 1, 'b', 1],
#    [0, 0, 'r', 0],
#    [1, 0, 'b', 0],
#    [1, 1, 'r', 1]
#]


# each feature vector is different length -is this ok?
# length of feature vector too long? (e.g., api_resolv vector is of length 7,481 for over 7,000 unique API's called) (i.e., curse of dimensionality?) 
#  

data = [     #f_1 (reg_read)             f_2(reg_write)  f_3(net_con) f_4(net_http)    label
          [[1,0,1,1,1,0,0,0,1,0,0,0,1], [0,0,0,1,0,1,1], [1,1,0,1], [0,0,0,0,0,0,0], [1,0,0]],
          [[1,0,1,0,1,0,1,0,1,0,0,1,0], [1,0,0,1,0,1,0], [0,1,0,1], [0,1,0,1,0,0,0], [0,1,0]], 
          [[1,0,1,1,1,0,0,0,1,0,0,1,1], [0,1,0,1,0,1,1], [1,1,0,1], [0,0,1,0,0,0,0], [1,0,0]], 
          [[1,0,1,1,1,0,0,0,1,0,0,1,1], [1,0,0,1,0,0,1], [1,1,0,1], [1,0,0,0,1,0,1], [1,0,0]] 
]
print("data:")
for d in data:
    print(d)

X = [row[:-1] for row in data]
print("X: ")
for x in X:
    print(x)
Y = [row[-1] for row in data]
print("Y: ")
for y in Y:
    print(y)
