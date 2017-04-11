import json
import argparse
import glob
import os
import shutil
import itertools as it

features_and_vector_lengths = {}

def display_data_matrix(data):
    print("\n========DATA MATRIX======")
    print(*data, sep='\n')

    print("~~~~~~~~~~~~~")
    X = [row[:-1] for row in data]
    Y = [row[-1] for row in data]

    print("X: ")
    for x in X:
        print(x)
    print("Y: ")
    for y in Y:
        print(y)
    print("========DATA SUMMARY======")
    print("matrix dimensions: " + str(len(data)) + " x " + str(len(data[0])))
    print("number of rows: " + str(len(data)))
    print("length of feature vector: " + str(len(X[0])))

def convert_label(label_as_list):
    # index of where "1" indicates the class (0,1,2,3)
    class_label = [label_as_list.index(1)]
    return class_label 

def get_all_features_and_vector_lengths(path_to_all_possible_feature_values_filename):
    # open json file containing all possible features and feature_values
    print("ALL POSSIBLE FEATURES AND COUNT OF FEATURE-VALUES IN DATASET:")
    with open(path_to_all_possible_feature_values_filename) as data_file:
        data_set_features_values = json.load(data_file)
        for feature in data_set_features_values:
            print(feature + ": " + str(len(data_set_features_values[feature])))
            features_and_vector_lengths[feature] = len(data_set_features_values[feature])
       
def build_matrix_from_selected_features(path_to_dataset, path_to_list_of_features_to_train):
    # read in desired features for use in the model from text file and sort alphabetically
    features_to_use = sorted([line.rstrip() for line in open(path_to_list_of_features_to_train)])

    print("-----------")
    print("FEATURES USED FOR THIS MODEL:", *features_to_use, sep='\n')
    print("-----------")

    # 2D matrix that can be used in the model
    data_matrix = []

    for filename in glob.iglob(path_to_dataset + '/**/*.json', recursive=True):
        with open(filename) as data_file:
            print("PROCESSING: " + filename)
            malware_sample = json.load(data_file)

            row = []
            for feature in features_to_use:

                # if feature is not present in sample, pad feature vector with zeros
                if feature not in malware_sample:
                    vector_len = features_and_vector_lengths[feature]
                    print("  " + feature + ": " + "NOT present in " + filename + " (padding feature vector with " + str(vector_len) + " zeros)")
                    temp = list(map(lambda x: 0, range(vector_len)))     
                    row.extend(temp)
                    #print("  row: " + str(row))
                else:
                    print("  " + feature + ":" + str(malware_sample[feature]))
                    # collapse all features into one list (X)
                    row.extend(malware_sample[feature])
                    #print("row: " + str(row))

            class_label = convert_label(malware_sample['label'])
            row.extend(class_label)
            print("  label: " + str(class_label))
            print("  row: " + str(row))

            # append X to matrix
            data_matrix.append(row)

    return data_matrix

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_normalized_dataset", help="path to normalized dataset")
    parser.add_argument("path_to_all_possible_feature_values_filename", help="path to all possible feature values .json file ")
    parser.add_argument("path_to_list_of_features_to_train", help="path to .txt file with list of features to use for training")
    args = parser.parse_args()

    get_all_features_and_vector_lengths(args.path_to_all_possible_feature_values_filename)
    data = build_matrix_from_selected_features(args.path_to_normalized_dataset, args.path_to_list_of_features_to_train)

    # print out data (for debugging)
    display_data_matrix(data)

    X = [row[:-1] for row in data]
    Y = [row[-1] for row in data]

    # TODO - train SVM using X and Y from 'data'
