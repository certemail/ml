import json
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="path to feature-values")
    args = parser.parse_args()

    features_with_no_values = []
    counter_features = 0 

    with open(args.filename) as data_file:
        data = json.load(data_file)

        for feature in data:
            if len(data[feature]) == 0:
                features_with_no_values.append(feature)
            else:
                print(feature + ": " + str(len(data[feature])))
                counter_features += 1
        print("------------------------")
        
        print("features in dataset with no values: ")
        for f in features_with_no_values:
            print(f)

        print("=========================")
        print("total features: " + str(len(data.items())))
        print("total features with non-zero values: " + str(counter_features))
        print("total features with zero values (unusable): " + str(len(features_with_no_values)))
