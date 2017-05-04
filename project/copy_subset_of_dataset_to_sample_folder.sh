
if [[ -z "$1" ]]; then
  echo "usage: ${0} [subfolder_to_copy]"
  exit
fi

PATH_TO_DATASET=${HOME}/MalwareTrainingSets/trainingSets
SUBFOLDER=$1
PATH_TO_SAMPLE_DATASET=${HOME}/ml/project/sample_dataset
NUM_FILES_TO_COPY=50

# copy files into sample_dataset directory
for file in $(ls -p ${PATH_TO_DATASET}/${SUBFOLDER} | grep -v / | tail -${NUM_FILES_TO_COPY}); do 
    echo ${PATH_TO_DATASET}/${SUBFOLDER}/${file};
    cp ${PATH_TO_DATASET}/${SUBFOLDER}/${file} ${PATH_TO_SAMPLE_DATASET}
done
