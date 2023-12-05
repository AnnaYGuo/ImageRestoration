#!/bin/bash

set -e
git submodule update --init --recursive
conda update conda

echo "Installing HAT"

cd HAT
if conda env list | grep -q hat; 
then echo "env already exists";
else conda create --name hat; fi

source $SCRATCH/miniconda3/etc/profile.d/conda.sh
conda activate hat
conda install pip

conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
python -m pip install basicsr==1.3.4.9
python -m pip install -r requirements.txt
python setup.py develop
