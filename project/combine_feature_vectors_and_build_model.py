import json
import argparse
import glob
import os
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_dataset", help="path to dataset")
    parser.add_argument("path_to_list_of_features", help="path to list of features to concactenate into one vector")
    args = parser.parse_args()


    # read in desired features for use in the model from text file
    features_to_use = [line.rstrip() for line in open(args.path_to_list_of_features)]
    print("FEATURES USED FOR THIS MODEL:", *features_to_use, sep='\n')
    print("-----------")

    for filename in glob.iglob(args.path_to_dataset + '/**/*.json', recursive=True):
        with open(filename) as data_file:
            print("PROCESSING: " + filename)
            data_to_normalize = json.load(data_file)
