#!/bin/bash

set -e
git submodule update --init --recursive
conda update conda

cd StableSR

echo "Installing StableSR"
if conda env list | grep -q stablesr; 
then echo "env already exists"; 
else conda env create --yes --file environment.yaml; fi

source $SCRATCH/miniconda3/etc/profile.d/conda.sh
conda activate stablesr
conda install pip

set +e
python -m pip install -e git+https://github.com/CompVis/taming-transformers.git@master#egg=taming-transformers
python -m pip install -e git+https://github.com/openai/CLIP.git@main#egg=clip
set -e

python -m pip install -e .

mkdir $SCRATCH/ckpt/
if ! test -f $SCRATCH/ckpt/stablesr_000117.ckpt; then wget https://huggingface.co/Iceclear/StableSR/resolve/main/stablesr_000117.ckpt -P $SCRATCH/ckpt; fi
if ! test -f $SCRATCH/ckpt/vqgan_cfw_00011.ckpt; then wget https://huggingface.co/Iceclear/StableSR/resolve/main/vqgan_cfw_00011.ckpt -P $SCRATCH/ckpt; fi

cd ..
