#!/bin/bash

git submodule update --init --recursive

if conda info --envs | grep -q stablesr; 
then echo "stablesr already exists"; 
else
    # Install StableSR env
    echo "Installing StableSR\n"
    cd StableSR/StableSR
    conda env create --file environment.yaml
    conda activate stablesr
    pip install -e git+https://github.com/CompVis/taming-transformers.git@master#egg=taming-transformers
    pip install -e git+https://github.com/openai/CLIP.git@main#egg=clip
    pip install -e .
    
    cd ..
    mkdir ckpt/
    wget https://huggingface.co/Iceclear/StableSR/resolve/main/stablesr_000117.ckpt
    wget https://huggingface.co/Iceclear/StableSR/resolve/main/vqgan_cfw_00011.ckpt

    cd ..
fi

# Install Microsoft env
if conda info --envs | grep -q microsoft; 
then echo "microsoft already exists";
else
    echo "Installing Microsoft model\n"
    cd Microsoft/Bringing-Old-Photos-Back-to-Life
    conda create --name microsoft
    conda activate microsoft
    pip install -r requirements.txt
    
    cd ../..
fi
