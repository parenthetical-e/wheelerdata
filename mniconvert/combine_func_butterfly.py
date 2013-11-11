"""Combine ar* functional data in along their 4th axes.

usage: combined_func_butterfly datadir
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
fnames = [
        "arbutterfly0.nii", 
        "arbutterfly1.nii", 
        "arbutterfly2.nii", 
        "arbutterfly3.nii",
        "arbutterfly4.nii",
        "arbutterfly5.nii",
        "arbutterfly6.nii",
        "arbutterfly7.nii",
        "arbutterfly8.nii",
        "arbutterfly9.nii"]

for i, fname in enumerate(fnames):
    if not os.path.exists(os.path.join(datadir, fname)):
        print("Missing {0}".format(fname))
        fnames.pop(i)

# Create the niftis, remove and arn if they do not exist
niftis = []
for fname in fnames:
    try:
        niftis.append(read_nifti(os.path.join(datadir, fname)))
    except IOError:
        print("Warning: {0} not found".format(fname))
        pass
#niftis = [read_nifti(os.path.join(datadir, fname)) for fname in fnames]

# Combine the nifti objects and write the result
write_nifti(combine4d(niftis),
        os.path.join(datadir, "arbutterfly.nii"))
