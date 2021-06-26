### Getting Started
All dataset released in this data challenge are hosted in SciServer at:

>/home/idies/workspace/Temporary/ywx649999311/LSST_AGN/Class_Training/DC/

You will only see this directory after you successfully mounted the shared volumne. 

#### The files contained in the above data directory are:
- ObjectTable.parquet: The master `Object` table
- ForcedSourceTable.parquet: The table of light curves
- SourceTable.parquet: The master `Source` table
- s82ObjectTable.parquet: The Stripe 82 `Object` table
- s82SourceTable.parquet: The Stripe 82 `Source` table
- xmmlssObjectTable.parquet: The XMM-LSS `Object` table
- xmmlssSourceTable.parquet: The XMM-LSS `Source` table
- lc_feats.yml: A dictionary describing the various derived light curve features


#### A few notebooks guiding you through this dataset:
- [ReadTables.ipynb](ReadTables.ipynb): Show you how to read in the data shared with you. 
- A notebook exploring the dataset.
- A notebook demonstrating how to (efficiently) interact with the raw light curves.
- A notebook giving simple examples about how to perform classifications/regressions on the dataset.