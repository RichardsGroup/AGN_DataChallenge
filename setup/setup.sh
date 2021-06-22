#!/bin/bash

# activate shell for conda
echo ". /home/idies/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc
source ~/.bashrc

# create a new conda environment and activate 
conda env create --file env_sciserver.yml
conda activate agn_dc

# install new ipython kernel
python -m ipykernel install --user --name agn_dc --display-name "AGN DC"

# source again to activate current shell and conda env
source ~/.bashrc
