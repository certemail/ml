import json
import argparse
import glob
import os
import shutil
import logging
import itertools as it
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_val_score

features_and_vector_lengths = {}


def display_accuracy(scores):
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

def display_data_matrix(data):
    logging.debug("\n========DATA MATRIX======")
    #logging.debug(*data, sep='\n')
    for row in data:
        logging.debug(row)

    logging.debug("~~~~~~~~~~~~~")
    X = [row[:-1] for row in data]
    y = [row[-1] for row in data]

    logging.debug("X: ")
    for x in X:
        logging.debug(x)
    logging.debug("y: ")
    logging.debug(y)

    print("Preprocessing complete; matrix dimensions: " + str(len(data)) + " x " + str(len(data[0])))

def convert_label(label_as_list):
    # index of where "1" indicates the class (0,1,2,3)
    class_label = [label_as_list.index(1)]
    return class_label 

def get_all_features_and_vector_lengths(path_to_all_possible_feature_values_filename):
    # open json file containing all possible features and feature_values
    logging.info("ALL POSSIBLE FEATURES AND COUNT OF FEATURE-VALUES IN DATASET:")
    logging.info("-----------")
    with open(path_to_all_possible_feature_values_filename) as data_file:
        data_set_features_values = json.load(data_file)
        for feature in data_set_features_values:
            logging.info(feature + ": " + str(len(data_set_features_values[feature])))
            features_and_vector_lengths[feature] = len(data_set_features_values[feature])
       
def build_matrix_from_selected_features(path_to_dataset, path_to_list_of_features_to_train):
    # read in desired features for use in the model from text file and sort alphabetically
    features_to_use = sorted([line.rstrip() for line in open(path_to_list_of_features_to_train)])

    print("Preprocessing...")
    print("Building input matrix from the following features:")
    for feature in features_to_use:
        print('  {}'.format(feature))
    #print(*features_to_use, sep='\n')
    print()
    logging.info("\n")
    logging.info("FEATURES USED FOR THIS MODEL:")
    logging.info("-----------")
    for f in features_to_use:
        logging.info(f)
    logging.info("-----------")


    # 2D matrix that can be used in the model
    data_matrix = []

    for filename in glob.iglob(path_to_dataset + '/**/*.json', recursive=True):
        with open(filename) as data_file:
            logging.debug("PROCESSING: " + filename)
            malware_sample = json.load(data_file)

            row = []
            for feature in features_to_use:

                # if feature is not present in sample, pad feature vector with zeros
                if feature not in malware_sample:
                    vector_len = features_and_vector_lengths[feature]
                    logging.debug("  " + feature + ": " + "NOT present in " + filename + " (padding feature vector with " + str(vector_len) + " zeros)")
                    temp = list(map(lambda x: 0, range(vector_len)))     
                    row.extend(temp)
                    #logging.debug("  row: " + str(row))
                else:
                    logging.debug("  " + feature + ":" + str(malware_sample[feature]))
                    # collapse all features into one list (X)
                    row.extend(malware_sample[feature])
                    #logging.debug("row: " + str(row))

            class_label = convert_label(malware_sample['label'])
            row.extend(class_label)
            logging.debug("  label: " + str(class_label))
            logging.debug("  row: " + str(row))

            # append X to matrix
            data_matrix.append(row)

    return data_matrix


def train_svm(X, y):
    print("Training SVM w/ linear kernel...")
    
    # print original dataset feature values
    logging.debug("feature values (X):")
    logging.debug(X)
    logging.debug("classification (y):")
    logging.debug(y)
    
    # account for 'unbalanced' with class_weight
    clf = svm.SVC(kernel='linear', class_weight='balanced', C = 1.0)
    clf.fit(X,y)

    print()
    print('{}\n'.format(clf))
    
    w = clf.coef_[0]
    logging.info("")
    logging.info("clf.coef_[0] (w):")
    logging.info(w)
    logging.info("")
    print('{}: {}'.format("Number of samples", len(y)))
    print('{}: {}'.format("Number of classes", len(clf.n_support_)))
    print("Feature vector length: " + str(len(clf.coef_[0])))
    
    logging.info('{}: {}'.format("clf.intercept_[0]", clf.intercept_[0]))
    print('{}: {}'.format("Number of support vectors for each class", clf.n_support_))
    
    logging.info("Support vectors:")
    logging.info(clf.support_vectors_)

    # cross validation scores (10-fold)
    scores = cross_val_score(clf, X, y, cv=10)
    print()
    print("Cross validation scores:")
    for score in scores:
        print('  {:.3f}'.format(score))
    display_accuracy(scores)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_normalized_dataset", help="path to normalized dataset")
    parser.add_argument("path_to_all_possible_feature_values_filename", help="path to all possible feature values .json file ")
    parser.add_argument("path_to_list_of_features_to_train", help="path to .txt file with list of features to use for training")
    parser.add_argument("--log", help="log level")
    args = parser.parse_args()

    if args.log:
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        logging.basicConfig(filename='log.txt', filemode='w', level=numeric_level, format='%(levelname)s: %(message)s')


    print('{}'.format('='*60))
    get_all_features_and_vector_lengths(args.path_to_all_possible_feature_values_filename)
    data = build_matrix_from_selected_features(args.path_to_normalized_dataset, args.path_to_list_of_features_to_train)

    # print out data (for debugging)
    display_data_matrix(data)
    print('{}'.format('='*60))

    # convert matrix to numpy ndarray
    data = np.array(data)

    # randomize samples (by row)
    np.random.shuffle(data)

    # split into matrix of feature values and classification vector
    X = [row[:-1] for row in data]
    y = [row[-1] for row in data]

    # train SVM using X and Y from 'data'
    train_svm(X, y)
    print('{}'.format('='*60))
    
