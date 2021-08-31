# LSSTC AGN Data Challenge
### Update:
**Aug-31, 2021**

- Added thumbnails/cutouts (from SDSS DR16) for all objects in the `Object` table, ~130 objects have no matched thumbnails/cutouts. 
- A new example notebook ([link](getting_started/05_Cutout.ipynb)) is added to show how to access the pre-generated thumbnails/cutouts.

This repository hosts information for the LSSTC AGN Data Challenge 2021 (PI: Gordon Richards). A github page is available at [here](https://richardsgroup.github.io/AGN_DataChallenge/). More (basic) information about this data challenge and the released dataset can be found at [About.md](About.md).

The dataset released for this data challenge is hosted on SciServer. To participate in this data challenge using the released dataset, please follow the steps listed below:
1. Set up an account on [SciServer](https://www.sciserver.org/)
2. Fill out this google [form](https://forms.gle/Eq689gqNMvb7QwQk8) and then we will send you an invitation to join the `Drexel_LSST` group
4. Accept our invitation, see [here](setup/sciserver.pdf) for an example invitation
5. Get familiar with how to run a container (and correctly mount the shared volume) on SciServer, see [here](https://github.com/RichardsGroup/LSST_training/blob/master/Setup/Container.ipynb)
6. Set up the conda environment following the suggestions provided in the [setup](setup) folder
7. Explore the [getting_started](getting_started) folder, play with the example notebooks and take off from there

If you want to learn more about how this dataset is built, serveral notebooks explaining the data construction are included in the [docs](docs) folder.

For those that aren't familiar with AGNs (or perhaps even astronomy), please see this DRAFT [AGN for Non-Astronomers](https://www.overleaf.com/read/vtnrpcprjdns) document.
