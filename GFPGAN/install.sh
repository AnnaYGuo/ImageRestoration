#!/bin/bash

set -e
#git submodule update --init --recursive
conda update conda

echo "Installing GFPGAN"

cd GFPGAN
if conda env list | grep -q gfpgan; 
then echo "env already exists";
else conda create --name gfpgan; fi

source $SCRATCH/miniconda3/etc/profile.d/conda.sh
conda activate gfpgan
conda install pip
python -m pip install basicsr facexlib
python -m pip install -r requirements.txt
python setup.py develop
python -m pip install realesrgan

wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth -P experiments/pretrained_models

cd ..
