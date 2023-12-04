#!/bin/bash

set -e
git submodule update --init --recursive
conda update conda

cd SuperSR/StableSR
echo "Installing StableSR"

if conda env list | grep -q stablesr; 
then echo "env already exists"; 
else conda env create --yes --file environment.yaml; fi

source $SCRATCH/miniconda3/etc/profile.d/conda.sh
conda activate stablesr
conda install pip
if ! conda list | grep taming-transformers ; python -m pip install -e git+https://github.com/CompVis/taming-transformers.git@master#egg=taming-transformers; fi
if ! conda list | grep taming-transformers ; python -m pip install -e git+https://github.com/openai/CLIP.git@main#egg=clip; fi
python -m pip install -e .

cd ..
mkdir $SCRATCH/ckpt/
if test -f $SCRATCH/ckpt/stablesr_000117.ckpt; then wget https://huggingface.co/Iceclear/StableSR/resolve/main/stablesr_000117.ckpt -P $SCRATCH/ckpt; fi
if test -f $SCRATCH/ckpt/vqgan_cfw_00011.ckpt; then wget https://huggingface.co/Iceclear/StableSR/resolve/main/vqgan_cfw_00011.ckpt -P $SCRATCH/ckpt; fi

cd ..

# Install Microsoft env
echo "Installing Microsoft Model"
cd Microsoft/Bringing-Old-Photos-Back-to-Life

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

cd ../../
