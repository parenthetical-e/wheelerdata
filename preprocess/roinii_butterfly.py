"""Apply the mask to the nifiti data

Usage: roinii_butterfly roiname newname
"""
import re
import os
import sys
from roi.pre import join_time
import nibabel as nb
from metaaccumulate.data.nii import findallnii, masknii


def create(mask, path, niipartial, newname, restart=False):
    """Create a roi dataset using all Ploran 2007 (i.e. butterfly) 
    datasets.

    Input
    -----
    mask - name of a roi found in the Harvard Oxford atlas (see roi 
    package for details)
    path - the base path where all the BOLD data lives
    niipartial - a string the matches all data of interest
    newname - a name for all the combined roi data.  Note: all roi data is 
        saved in ./roinii/
    """
    
    try:
        os.mkdir("./roinii")
    except OSError:
        pass
    
    # Get and order the nii files
    print("Finding nii files.")
    niis = findallnii(path, niipartial)
    niis, bysub = _ordernii_butterfly(niis)

    # Mask and combine
    roinames = {}
    for sub in sorted(bysub.keys()):
        roinames[sub] = []
        for scan in bysub[sub]:
            if scan != None:
                roiname = _mask_butterfly(mask, scan, newname, restart)
                roinames[sub].append(roiname)
            else:
                roinames[sub].append(None)
    
    print("Combining all roi data by subject.")
    for sub, scans in roinames.items():
        scans = [scan for scan in scans if scan != None]
            ## Drop None

        # Init combinedniis then add the 
        # remaining scans to it and save 
        # the result
        print("Combining {0}.".format(sub))
        combinedniis = nb.load(scans.pop(0))
        for scan in scans:
            combinedniis = join_time(combinedniis, nb.load(scan))
        
        print("Saving {0}.".format(sub))
        nb.save(combinedniis, 
                os.path.join(
                "./roinii", "{0}_{1}.nii.gz".format(newname, sub)))
        
        # [os.remove(scan) for scan in scans]
            ## Clean up old scans


def _mask_butterfly(mask, nii, newname, restart):
    """Apply mask to nii, save as newname."""
    
    print("Masking {0} with {1}.".format(os.path.basename(nii), mask))
    
    # Create a name for the temp roi data
    # then use the mask, saving with the tmpname
    name = newname + "_" + os.path.basename(nii)
    name = os.path.join(path, "roinii", name)
    
    # Ensure we are compressing the data
    fullname = os.path.basename(name)
    filename, fileextension = os.path.splitext(fullname)
    name = os.path.join(
            os.path.dirname(name), "{0}.nii.gz".format(filename))
    
    # If the file exists and we are
    # restarting continue on.
    if restart and os.path.isfile(name):
        print("{0} exists, continuing on.".format(name))
    else:
        # Mask! Save as name
        masknii(mask, nii, save=name)

    return name


def _ordernii_butterfly(niis):
    """Order a the provided list of nifti1 (.nii) files as appropriate for the 
    Ploran 2007 dataset (a.k.a butterfly).
    """
    
    scanmap = {} 
        ## Keyed on scode, values are a list of scans
    
    for fipath in niis:
        fi = os.path.basename(fipath)
        fi_name_parts = fi.split('_')
        
        scode = fi_name_parts[0]
        scode = int(scode[1:])
            ## strip 's' from subcode, e.g 's4' -> 4
                   
        # Parse the scancode, looking for the scan number
        scancode = fi_name_parts[1]
        mat = re.match("^b\d+", scancode)
        scannum = int(mat.group()[1:]) - 1 
            ## mat.group() should contain, for example, 'b2'
            ## so we drop the first letter and
            ## cast to an int then offset by 1 so it can
            ## be used as an index into a list (e.g. 'b2' -> 1)
        
        # Debug:
        # print("{0} match: {2}, scan: {1}".format(fi, scannum, mat.group()))
        
        # If scode is in scanmap add fipath (not fi)
        # otherwise init scode first
        max_num_scans = 10          ## ....for Ploran 2007
        if scode in scanmap.keys():
            scanmap[scode][scannum] = fipath
        else:
            scanmap[scode] = [None, ] * max_num_scans
            scanmap[scode][scannum] = fipath
    
    # Use scanmap to create an ordered list of niis
    orderedniis = []
    [orderedniis.extend(scanmap[sub]) for sub in sorted(scanmap.keys())]
        ## Want a 1d list thus .extend()
    
    orderedniis = [nii for nii in orderedniis if nii != None]
        ## Drop Nones
    
    return orderedniis, scanmap


if __name__ == '__main__':
    """Command line invocation setup."""
    
    # ----
    # User parameters
    niipartial = "MNI152_3mm.4dfp.nii"
    restart = True
    # ----
    
    # Create a place for the roi data to live
    # if necessary.
    try:
        os.mkdir("./roinii")
    except OSError:
        pass
    
    # Process argv
    if len(sys.argv[1:]) != 2:
        raise ValueError("Two arguments are required.")

    mask = sys.argv[1]
    newname = sys.argv[2]
    path = os.getcwd()

    # Go!
    create(mask, path, niipartial, newname, restart)

