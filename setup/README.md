## Instructions
Two ways to get all the needed packages installed:
#### 1. Create a new conda environment
Run the following command within this folder to create a new conda environment called `agn_dc`:
```sh
bash setup.sh
conda activate agn_dc
```

#### 2. Using the built-in `py38` environment
```sh
conda activate py38
pip install pyarrow
```

__Note:__ If you have already created a couple conda environments, I would suggest following the second method given that each SciServer container has limited disk quota.
