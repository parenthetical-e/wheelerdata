"""Apply the mask to the nifiti data

Usage: rfroinii_butterfly roifile
"""
import re
import os
import sys
from roi.pre import join_time
import nibabel as nb
from metaaccumulate.data.nii import findallnii, masknii
from metaaccumulate.data.load import load_roifile


def create(args):
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
    
    # Process args, a dunmb way to make this function
    # compatible with pool.map()
    mask = args[0]
    path = args[1]
    niipartial = args[2]
    newname = args[3]
    restart = args[4]
    
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
        cname = os.path.join(
                "./roinii", "{0}_{1}.nii.gz".format(newname, sub))
        
        # If the combinedniis exists, move on (if we're
        # in restart mode)
        if restart and os.path.isfile(cname):
            print("{0} exists, continuing on.".format(cname))
        else:
            for scan in scans:
                combinedniis = join_time(combinedniis, nb.load(scan))
            
            print("Saving {0}.".format(sub))
            nb.save(combinedniis, cname)
            
            # [os.remove(scan) for scan in scans]
                ## Clean up old scans


def _mask_butterfly(mask, nii, newname, restart):
    """Apply mask to nii, save as newname."""
    
    print("Masking {0} with {1}.".format(os.path.basename(nii), mask))
    
    # Create a name for the temp roi data
    # then use the mask, saving with the tmpname
    name = newname + "_" + os.path.basename(nii)
    name = os.path.join(path, "roinii", name)
    
    # Ensure we are compressing the 
    # data by adding .nii.gz instead of, 
    # say, .nii
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
    """Order a the provided list of nifti1 (.nii) files as appropriate 
    for the Ploran 2007 dataset (a.k.a butterfly).
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
                    ## key:scode, val:[None, ...]
            scanmap[scode][scannum] = fipath
                    ## and index into [None, ...]
            
    # Use scanmap to create an ordered list of niis
    orderedniis = []
    [orderedniis.extend(scanmap[sub]) for sub in sorted(scanmap.keys())]
        ## Want a 1d list thus .extend()
    
    orderedniis = [nii for nii in orderedniis if nii != None]
        ## Drop Nones
    
    return orderedniis, scanmap


if __name__ == '__main__':
    """Command line invocation setup."""    
    from multiprocessing import Pool
    
    # ----
    # User parameters
    niipartial = "MNI152_3mm.4dfp.nii"
    path = os.getcwd()
    restart = True
    
    ncore = 4
        # Set ncore > 1 if you want to 
        # parallelize the roi extractions
    
    # ----
    # Create a place for 
    # the roi data to 
    # live if necessary.
    try:
        os.mkdir("./roinii")
    except OSError:
        pass
    
    # ----
    # Process argv
    if len(sys.argv[1:]) != 1:
        raise ValueError("One arguments are required.")
    
    # ----
    # Go!
    rois, names = load_roifile(sys.argv[1])
    
    # Build up arguements lists
    # creates needs 
    # (roi, path, niipartial, name, restart)
    arglist = []
    for roi, name in zip(rois, names):
        print("Creating ROI data for {0} as {1}.".format(roi, name))
        arglist.append((roi, path, niipartial, name, restart))
    
    # Parallelize using the arglist and Pool
    pool = Pool(ncore)
    pool.map(create, arglist)
