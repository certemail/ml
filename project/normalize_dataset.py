import json
import argparse
import glob
import os
import shutil

data_set_features_values = {}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_dataset", help="path to dataset")
    parser.add_argument("all_possible_feature_value_filename", help="path to feature-values")
    parser.add_argument("path_to_normalized_dataset", help="new directory that will contain the normalized dataset")
    args = parser.parse_args()

    # open json file containing all possible features and feature_values
    with open(args.all_possible_feature_value_filename) as data_file:
        data_set_features_values = json.load(data_file)

        for feature in data_set_features_values:
            print(feature + ": " + str(len(data_set_features_values[feature])))

    # create output directory of normalized dataset
    # delete directory first if already exists
    print("CREATING OUTPUT DIRECTORY FOR NORMALIZED DATASET: " +  args.path_to_normalized_dataset)
    if os.path.exists(args.path_to_normalized_dataset):
        print("\tdirectory already exists - overwriting...")
        shutil.rmtree(args.path_to_normalized_dataset)
    os.mkdir(args.path_to_normalized_dataset)

    # open every .json file and write normalized version to new folder
    for filename in glob.iglob(args.path_to_dataset + '/**/*.json', recursive=True):
        with open(filename) as data_file:
            data = json.load(data_file)

            # include only Zeus, Crypto, Locker, and APT1 
            # and ignore other malware families
            lbl = data["properties"]["label"]
            if not lbl == "APT1" and \
               not lbl == "Crypto" and \
               not lbl == "Locker" and \
               not lbl == "Zeus":
                print("SKIPPING: " + filename)
                continue

            print("NORMALIZING: " + filename)
            
