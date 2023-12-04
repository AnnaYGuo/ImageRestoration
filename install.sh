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
python -m pip install -e git+https://github.com/CompVis/taming-transformers.git@master#egg=taming-transformers
python -m pip install -e git+https://github.com/openai/CLIP.git@main#egg=clip
python -m pip install -e .

cd ..
mkdir $SCRATCH/ckpt/
wget https://huggingface.co/Iceclear/StableSR/resolve/main/stablesr_000117.ckpt -P $SCRATCH/ckpt
wget https://huggingface.co/Iceclear/StableSR/resolve/main/vqgan_cfw_00011.ckpt -P $SCRATCH/ckpt

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
python -m pip install -r requirements.txt
