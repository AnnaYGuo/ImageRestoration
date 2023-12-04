#!/bin/bash
set -e
git submodule update --init --recursive
conda update conda

# Install base packages
source $SCRATCH/miniconda3/etc/profile.d/conda.sh
conda activate base
conda install pip
python -m pip install opencv-python imageio
