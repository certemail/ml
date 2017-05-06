#!/bin/bash

if [[ -z "$2" ]]; then
  echo "usage: ${0} [number_of_files_to_copy] [subfolder_to_copy] "
  echo ""
  echo "example: to copy 50 Zeus files from the full dataset into the sample_dataset directory:"
  echo "${0} 50 Zeus"
  echo ""
  exit
fi

NUM_FILES_TO_COPY=${1}
SUBFOLDER=${2}
PATH_TO_DATASET=${HOME}/MalwareTrainingSets/trainingSets
PATH_TO_SAMPLE_DATASET=${HOME}/ml/project/sample_dataset

# copy files into sample_dataset directory
for file in $(ls -p ${PATH_TO_DATASET}/${SUBFOLDER} | grep -v / | tail -${NUM_FILES_TO_COPY}); do 
    echo ${PATH_TO_DATASET}/${SUBFOLDER}/${file};
    cp ${PATH_TO_DATASET}/${SUBFOLDER}/${file} ${PATH_TO_SAMPLE_DATASET}
done

echo "copied ${NUM_FILES_TO_COPY} ${SUBFOLDER} ..."
