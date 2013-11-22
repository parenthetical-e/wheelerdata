"""Combine ar* functional data in along their 4th axes.

usage: combined_func_redgreen datadir
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
fnames = ["warredgreen0.nii", 
        "warredgreen1.nii", 
        "warredgreen2.nii", 
        "warredgreen3.nii",
        "warredgreen4.nii", 
        "warredgreen5.nii"]

# Create the niftis, remove and arn if they do not exist
for i, fname in enumerate(fnames):
    if not os.path.exists(os.path.join(datadir, fname)):
        print("Missing {0}".format(fname))
        fnames.pop(i)

niftis = [read_nifti(os.path.join(datadir, fname)) for fname in fnames]

# Combine the nifti objects and write the result
write_nifti(combine4d(niftis),
        os.path.join(datadir, "warredgreen.nii"))
