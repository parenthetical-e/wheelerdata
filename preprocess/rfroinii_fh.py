"""Apply the mask to the nifiti data

Usage: roinii_fh roifile
"""
import re
import os
import sys
from roi.pre import join_time
import nibabel as nb
from metaaccumulate.datatools.nii import findallnii, masknii
from metaaccumulate.datatools.load import load_roifile


def create(args):
    """Create a roi dataset using all Ploran 2007 (i.e. butterfly) 
    datasets.
    
    Parameters
    ----------
    mask - name of a roi found in the Harvard Oxford atlas (see roi 
    package for details)
    newname - what (if anything) to rename the roi data as,
        often the default name (i.e. mask) are rather long
    subdatatable - a dictionary whose keys are subject numbers
        and whose values are absoluate paths to that Ss
        whole brain (functional) data.
    basepath - the top-level directory where all the Ss BOLD 
        (and other) data lives.
    """
     
    # Process args, a dunmb way to make 
    # this function compatible with pool.map()
    mask, newname, subdatatable, basepath = args
    print("Mask is {0}.".format(mask))

    maskednames = []
    for s in sorted(subdatatable.keys()):
        print("Running subject {0}.".format(s))

        # Look up the location of that Ss data, 
        # and mask it, finally save the masked 
        # file to disk
        datadir = subdatatable[s]
        saveas = os.path.join(basepath, 
                'roinii', "{0}_{1}.nii.gz".format(newname, s))
        masknii(mask, datadir, save=saveas)
         

if __name__ == '__main__':
    """Command line invocation setup."""    

    from multiprocessing import Pool
     
    # ----
    # User parameters
    basepath = os.getcwd()
    ncore = 3
        ## Set ncore > 1 if you want to 
        ## parallelize the roi extractions
    
    # ----
    # Create a place for the roi data to 
    # live if necessary.
    try:
        os.mkdir("./roinii")
    except OSError:
        pass
     
    # ----
    # Process argv
    if len(sys.argv[1:]) != 1:
        raise ValueError("One argument are required.")

    rois, names = load_roifile(sys.argv[1])

    # ----
    # Link subjects with paths to data
    subdatatable = {9 : os.path.join(basepath, 'fh09', 'warfh.nii'), 
            11 : os.path.join(basepath, 'fh11', 'warfh.nii'),
            13 : os.path.join(basepath, 'fh13', 'warfh.nii'),
            14 : os.path.join(basepath, 'fh14', 'warfh.nii'),
            15 : os.path.join(basepath, 'fh15', 'warfh.nii'),
            17 : os.path.join(basepath, 'fh17', 'warfh.nii'),
            19 : os.path.join(basepath, 'fh19', 'warfh.nii'),
            21 : os.path.join(basepath, 'fh21', 'warfh.nii'),
            23 : os.path.join(basepath, 'fh23', 'warfh.nii'),
            24 : os.path.join(basepath, 'fh24', 'warfh.nii'),
            25 : os.path.join(basepath, 'fh25', 'warfh.nii'),
            26 : os.path.join(basepath, 'fh26', 'warfh.nii'),
            27 : os.path.join(basepath, 'fh27', 'warfh.nii'),
            28 : os.path.join(basepath, 'fh28', 'warfh.nii')}
    
    # subdatatable = {
    #         14 : os.path.join(basepath, 'fh14', 'warfh.nii')}
    
    # Build up 4-tuples that contain all the args
    # create needs, iterate over all the entries
    # in the roifile
    arglist = []
    for roi, name in zip(rois, names):
        arglist.append((roi, name, subdatatable, basepath))
    
    # ---
    # Go!
    # Parallelize using the arglist and Pool
    pool = Pool(ncore)
    pool.map(create, arglist)
