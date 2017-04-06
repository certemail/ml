#!/usr/bin/python3.4

import os
import shutil
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("cifar10_data_bin_file", help="binary file to be modified")
    args = parser.parse_args()

    data_bin_file = args.cifar10_data_bin_file
    if not os.path.exists(data_bin_file):
        print("file does not exist")
        exit(1)

    label_size = 1         
    image_size = 15   #3072
    record_size = label_size + image_size 

    offset = 0

    new_byte_array = bytearray() 

    with open(data_bin_file, 'rb') as f:
	
	# read in entire file into a byte array
        b_arr = f.read()	
        num_bytes_in_file = len(b_arr)
        print("num bytes in file: " + str(num_bytes_in_file))

        while offset < num_bytes_in_file:
            label = b_arr[offset]
            print("label: " + str(hex(label)))	

            # label is a bird or horse, extract record
            if label == 0x2 or label == 0x7:
                slice_obj = slice(offset, offset+record_size)
                sliced_record = b_arr[slice_obj]
                print("\tsliced record: " + str(sliced_record))
                new_byte_array.extend(sliced_record)
             
            # advance to next record 
            offset = offset + record_size
            print("offset: " + str(offset) + " (" + hex(offset) + ")" )
            print("----------------------")

    print("======================")
    print("extracted records: " + str(new_byte_array))

    # write out new bytes to file
    outfile = os.path.splitext(data_bin_file)[0] + "__processed.bin"
    print("writing extracted records to: " + str(outfile))
    with open(outfile, 'wb') as f:
        f.write(new_byte_array)
	
       

	
        #f.seek(offset)
        #print("file pointer at: " + str(hex(f.tell())))
        #label = bytearray(f.read(label_size))

        ### only keep bird and horse labels (2 and 7)
        #if label[0] == 0x2 or label[0] == 0x7:
        #    print("found it")
        #    print(label)
        #else:
        #    print("not bird or horse")
        #    print(label) 
#
#    exe_file = args.executable_filename
#    if not os.path.exists(exe_file):
#        print(f + "does not exist...exiting")
#        exit(1)
#
#    encrypted_filename = exe_file + "_encrypted"
#
#    # delete encrypted file if already exists
#    if os.path.exists(encrypted_filename):
#        print("deleting: ", encrypted_filename)
#        os.remove(encrypted_filename)
#
#    # copy and rename new file with encrypted_filename
#    shutil.copy(exe_file, encrypted_filename) 
#
#
#    # decode file offset hex strings as integers
#    s_offset = int.from_bytes(bytes.fromhex(args.start_offset), byteorder='big')
#    e_offset = int.from_bytes(bytes.fromhex(args.end_offset), byteorder='big')
#    num_bytes_to_change = e_offset - s_offset
#
#    print("file offset start: ", hex(s_offset))
#    print("file offset end:   ", hex(e_offset))
#    print("number of bytes to overwrite: ", num_bytes_to_change)
#    print()
#	
#    with open(encrypted_filename, 'rb+') as f:
#
#        # seek to offset in file
#        print("seeking to start position...")
#        f.seek(s_offset)
#
#        print("file pointer at: " + str(hex(f.tell())))
#
#        # get bytes to be encrypted
#        b_arr = bytearray(f.read(num_bytes_to_change))
#        
#        print("-----------")
#        print("bytes to be encrypted: ")
#        print(b_arr)
#        print("-----------")
#
#        xor_key = 0xCC
#        for i in range(len(b_arr)):
#            b_arr[i] ^= xor_key
#
#        print("bytes after encryption:")
#        print(b_arr) 
#        print("-----------")
#        print("file pointer at: " + str(hex(f.tell())))
#
#        # reset file pointer
#        print("reseting file back to start: ", str(hex(s_offset)))
#        f.seek(s_offset)
#
#        print()
#        print("writing encrypted bytes back to disk...") 
#        f.write(b_arr)
#        f.flush()
#
#
#
#
