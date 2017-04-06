#!/usr/bin/env python

import os
import shutil
import argparse
import glob

def rebuild(path_to_training_images):
    label_size = 1         
    image_size = 3072   #3072
    record_size = label_size + image_size 

    # delete older processed files
    for old_file in glob.iglob(path_to_training_images + '/**/*__only*.bin', recursive=True):
        print("deleting " + str(old_file))
        os.remove(old_file)

    for data_bin_file in glob.iglob(path_to_training_images + '/**/*.bin', recursive=True):
        with open(data_bin_file, 'rb') as f:
            # read in entire file into a byte array
            b_arr = f.read()	
            num_bytes_in_file = len(b_arr)
            print("num bytes in file: " + str(num_bytes_in_file))

            offset = 0
            num_birds = 0
            num_horses = 0
            num_other_records = 0
            new_byte_array = bytearray() 

            while offset < num_bytes_in_file:
                label = b_arr[offset]
                print("label: " + str(hex(label)))	

                # label is BIRD 
                if label == 0x2:
                    print("\tFOUND A BIRD")
                    new_label = 0x0
                    sliced_record = bytearray([new_label])
                    slice_obj = slice(offset+1, offset+record_size)
                    sliced_record.extend(b_arr[slice_obj])
                    
                    #print("\tsliced record: " + str(sliced_record))
                    new_byte_array.extend(sliced_record)
                    num_birds += 1

                # label is HORSE
                elif label == 0x7:
                    print("\tFOUND A HORSE")
                    new_label = 0x1
                    sliced_record = bytearray([new_label])
                    slice_obj = slice(offset+1, offset+record_size)
                    sliced_record.extend(b_arr[slice_obj])
                    
                    #print("\tsliced record: " + str(sliced_record))
                    new_byte_array.extend(sliced_record)
                    num_horses += 1

                else:
                    num_other_records += 1
                 
                # advance to next record 
                offset = offset + record_size
                print("offset: " + str(offset) + " (" + hex(offset) + ")" )
                print("----------------------")

        print("======================")
        #print("extracted records: " + str(new_byte_array))

        # write out new bytes to file
        print("total number of birds: " + str(num_birds))
        print("total number of horses: " + str(num_horses))
        print("total number of other records: " + str(num_other_records))
        outfile = os.path.splitext(data_bin_file)[0] + "__only_birds_and_horses.bin"
        print("writing extracted records to: " + str(outfile))
        with open(outfile, 'wb') as f:
            f.write(new_byte_array)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_training_images", help="path to cifar10 data")
    args = parser.parse_args()

    if not os.path.exists(args.path_to_training_images):
        print("file path does not exist")
        exit(1)

    rebuild(args.path_to_training_images)
