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

cd ..
