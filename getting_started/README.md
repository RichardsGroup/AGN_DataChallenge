### Getting Started
All dataset released in this data challenge are hosted on SciServer at:

>/home/idies/workspace/Temporary/ywx649999311/LSST_AGN/Class_Training/DC/

You will only see this directory after you successfully mount the shared volumne (see [here](https://github.com/RichardsGroup/LSST_training/blob/master/Setup/Container.ipynb) for an example).

#### The files contained in the data directory are:
- ObjectTable.parquet: The master `Object` table (Stripe 82 + XMM-LSS)
- ForcedSourceTable.parquet: The table of light curves
- SourceTable.parquet: The master `Source` table (Stripe 82 + XMM-LSS)
- s82ObjectTable.parquet: The Stripe 82 `Object` table
- s82SourceTable.parquet: The Stripe 82 `Source` table
- s82MultiWavelengthTable.parquet: A table of multiwavelength data for the objects included in the Stripe 82 `Object` table
- xmmlssObjectTable.parquet: The XMM-LSS `Object` table
- xmmlssSourceTable.parquet: The XMM-LSS `Source` table
- xmmlssMultiWavelengthTable.parquet: A table of multiwavelength data for the objects included in the XMM-LSS `Object` table
- lc_feats.yml: A dictionary describing the various features derived from light curves. You can also find this file in the 'docs' folder.
- mv_cols.yml: A dictionary definitions for the columns in the multiwavelength table(s). You can also find this file in the 'docs' folder.


#### A few notebooks guiding you through this dataset:
- [01_ReadTables.ipynb](01_ReadTables.ipynb): Showing you how to read in the tables.
- [02_ObjectTable.ipynb](02_ObjectTable.ipynb): Exploratory data analysis with the `Object` table
- [03_ForcedSourceTable.ipynb](03_ForcedSourceTable.ipynb): Demonstrating how to interact with the raw light curves.
- A notebook giving simple examples about how to perform classifications/regressions on the dataset.