"""Combine war* functional data in along their 4th axes.

usage: combined_func_fh datadir
"""
import sys
import os
from roi.pre import combine4d
from roi.io import read_nifti, write_nifti

# Process the argv
if len(sys.argv[1:]) != 1:
    raise ValueError('Only one argument allowed')
datadir = sys.argv[1]

# Name the names, then read in the data
fnames = ["warfh0.nii", "warfh1.nii", "warfh2.nii", "warfh3.nii",
        "warfh4.nii", "warfh5.nii", "warfh6.nii"]
niftis = [read_nifti(os.path.join(datadir, fname)) for fname in fnames]

# Combine the nifti objects and write the result
write_nifti(combine4d(niftis), os.path.join(datadir, "warfh.nii"))
