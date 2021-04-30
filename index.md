---
layout: default
title: Home
---
## About
This page contains the information for the _**LSSTC Enabling Science: AGN data challenge**_ as proposed by the LSST Active Galactic Nuclei (AGN) Science Collaboration in the Summer of 2020. The dataset used in this data challenge is based on a training set constructed to facilitate AGN classification in LSST. More information about this training set can be found at [Here](https://github.com/RichardsGroup/LSST_training).

## The DataSet
The sources included in this dataset are coming from two main survey regions: _SDSS Stripe 82 (S82)_ and _XMM-LSS_. The S82 region has been redefined to include more coverage from the Dark Energy Survey (DES). The footprint for these two regions are:

#### _Stripe 82_

| RA         | Dec           |
| ---------- | ------------- |
| (-60, -43] | (-1.25, 1.25) |
| (-43, 0]   | (-2, 2)       |
| (0, 45])   | (-7, 5)       |
| (45, 60)   | (-1.25, 1.25) |

#### _XMM-LSS_

| RA             | Dec            |
| -------------- | -------------- |
| [34.2, 37.125] | [-5.72, -3.87] |

## Data Available
#### _Stripe 82_  (QSOs + variable stars)
- True Labels: SDSS (spectra)
- Photometry: SDSS (optical), UKIDSS (NIR), SpIES (MIR), GALEX (NUV and FUV)
- Astrometry: Gaia (proper motion and parallax)
- Time Domain: SDSS light curves

## Data to be ingested
#### _Stripe 82_
- [ ] ZTF light curves
- [ ] HSC-SSP photometry
- [ ] DES photometry
- [ ] ...

#### _XMM-LSS_
- [ ] HSC-SSP photometry
- [ ] DES photometry
- [ ] X-ray (XMM-Newton)

### Support or Contact
If you have any questions related to this data challenge, please do not hesitate to concat Gordon Richards (<gtr@physics.drexel.edu>) or Weixiang Yu (<wy73@drexel.edu>) for more technical questions.
