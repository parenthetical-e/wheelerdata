import os
import numpy as np
import pandas as pd
from fidl.convert import nod_mat
from fmrilearn.preprocess.labels import (construct_targets, construct_filter,
        filter_targets)
from wheelerdata.load.fh import (get_RT_metadata_paths, get_subject_fidl_paths,
        get_nod_subject_names)


def _create_nod(metapath, fidlpath, scode):
    triallen = 5

    meta = pd.read_csv(metapath)
    faceshouses = np.array(meta["exp"].tolist())
    trs = np.array(meta["TR"].tolist())
    trial_index = np.array(meta["trialcount"].tolist())

    targets = construct_targets(
            trs=trs,
            faceshouses=faceshouses,
            trial_index=trial_index)

    keepers = ["face", "house"]
    keep_fhs = construct_filter(targets["faceshouses"], keepers, True)
    targets = filter_targets(keep_fhs, targets)
    
    names = targets["faceshouses"]
    onsets = targets["trs"]
    durations = np.array([triallen, ] * len(targets["trial_index"]))

    nod_mat(names, onsets, durations, os.path.join(fidlpath, 
            "nod_" + scode + "_stim_facehouse.mat"))


if __name__ == "__main__":
    metapaths = get_RT_metadata_paths()
    fidlpaths = get_subject_fidl_paths()
    nodnames = get_nod_subject_names()

    [_create_nod(mpath, fpath, nodname) for 
            mpath, fpath, nodname in zip(metapaths, fidlpaths, nodnames)]
