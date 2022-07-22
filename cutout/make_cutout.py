"""Script to make cutout for all objects in the object table."""
import pandas as pd
import numpy as np
import imageio
import os, sys, time
from joblib import delayed, Parallel


def make_cutout(objectId, ra, dec, output_dir="."):
    # web api url template
    url = (
        "http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?"
        + "ra={}&dec={}&scale=0.4&height=64&width=64".format(ra, dec)
    )

    # saving path template
    save_path = f"{output_dir}/{objectId}.npy"

    for i in range(5):  # retry loop
        try:
            im = imageio.imread(url)
            err = 0
            np.save(save_path, im)
            break  # On success, stop retry.
        except:
            print("timeout, retry in 1 second.")
            time.sleep(1)
            err = 1

    return err


def main(objectTablePath, output_dir):

    # create directory if not exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # read min object table and reset index (move objectId into cols)
    object_df = pd.read_parquet(objectTablePath, columns=["ra", "dec"])
    object_df_flat = object_df.reset_index()

    #     # TEST code
    #     object_df_flat = object_df_flat.iloc[:100].copy()

    n_core = 15
    errs = Parallel(n_jobs=n_core)(
        delayed(make_cutout)(
            row[1]["objectId"], row[1]["ra"], row[1]["dec"], output_dir=output_dir
        )
        for row in object_df_flat.iterrows()
    )

    # write error code back to min object table and save to disk
    object_df_flat["cutout_err"] = errs
    object_df_flat.to_parquet("cutout_result.parquet", index=False)

    # print out total number of failed requests
    print(f"Total number of failed cutout request: {object_df_flat.cutout_err.sum()}")


if __name__ == "__main__":

    objectTablePath = sys.argv[1]  # Path for 'ObjectTable.parquet'
    output_dir = sys.argv[2]  # Directory to save cutouts

    main(objectTablePath, output_dir)
