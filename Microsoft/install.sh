#!/bin/bash

set -e
git submodule update --init --recursive
conda update conda

cd Bringing-Old-Photos-Back-to-Life

echo "Installing Microsoft"
if conda env list | grep -q microsoft; 
then echo "env already exists";
else conda create --name microsoft; fi

source $SCRATCH/miniconda3/etc/profile.d/conda.sh
conda activate microsoft
conda install pip
conda install -c conda-forge dlib

cd Face_Enhancement/models/networks/
git clone https://github.com/vacancy/Synchronized-BatchNorm-PyTorch
cp -rf Synchronized-BatchNorm-PyTorch/sync_batchnorm .
cd ../../../

cd Global/detection_models
git clone https://github.com/vacancy/Synchronized-BatchNorm-PyTorch
cp -rf Synchronized-BatchNorm-PyTorch/sync_batchnorm .
cd ../../

cd Face_Detection/
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
cd ../

cd Face_Enhancement/
wget https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life/releases/download/v1.0/face_checkpoints.zip
unzip face_checkpoints.zip
cd ../
cd Global/
wget https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life/releases/download/v1.0/global_checkpoints.zip
unzip global_checkpoints.zip
cd ../

python -m pip install -r requirements.txt

cd ..