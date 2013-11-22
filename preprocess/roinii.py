"""Extract subject ROIs for the selected Wheeler Lab experiment.

Usage: roinii roifile expname
"""
import re, os, sys
import nibabel as nb

import roi
#from fmrilearn.preprocess.nii import masknii
from fmrilearn.load import load_roifile

from wheelerdata.load.fh import FH
from wheelerdata.load.butterfly import Butterfly
from wheelerdata.load.clock import Clock
from wheelerdata.load.polygon import Polygon
from wheelerdata.load.redgreen import Redgreen
from multiprocessing import Pool


def create(maskname, newname, expname, overwrite=False):
    """Save all subjects nifti1 datasets to ./roinii for the given mask/ROI name.
    
    Parameters
    ---------
    maskname : str 
        A valid ROI name (see my `roi` package at `https://github.com/andsoandso/roi`
    newname : str
        A new name for the roi
    expname : str
        A valid `wheelerdata.load.*` instance name
    """

    # Experimental config 
    if expname == "fh":
        data = FH()
    elif expname == "butterfly":
        data = Butterfly()
    elif expname == "clock":
        data = Clock()
    elif expname == "polygon":
        data = Polygon()
    elif expname == "redgreen":
        data = Redgreen()
    else:
        raise ValueError("expname ({0}) not valid".format(expname))

    basepath = data.datapath
    paths = data.get_subject_paths()
    scodes = data.scodes
    datas = [os.path.join(path,"war{0}.nii".format(expname)) for path in paths]

    # then create the roi data for each S.
    for s, data in zip(scodes, datas):
        saveas = os.path.join(
                basepath, 'roinii', "{0}_{1}.nii.gz".format(newname, s))

        if os.path.exists(saveas) and not overwrite:
            print("{0} exists, moving on.".format(saveas))
            continue

        mask = roi.atlas.get_roi('HarvardOxford', maskname)
        nii = roi.io.read_nifti(data)
        maskednii = roi.pre.mask(nii, mask, standard=True)

        # (Potentially expensive) sanity checks
        assert sum([nz.size for nz in mask.get_data().nonzero()]) != 0, ("Mask" 
                " {0} was empty".format(maskname))
        assert sum([nz.size for nz in nii.get_data().nonzero()]) != 0, ("Nifiti1" 
                " {0} was empty".format(maskname))

        # It's possiblethat the ROI covers an area outside the 
        # functional acquisition window.  Proceed but warn.
        if sum([nz.size for nz in maskednii.get_data().nonzero()]) == 0:
            print("{0} maskednii was empty. Nothing to write.".format(maskname))
            continue

        print("Writing {0}".format(saveas))
        roi.io.write_nifti(maskednii, saveas)
    
    # Log success
    f = open("{0}_roinii.log".format(expname), "a")
    f.write("{0}:{1}\n".format(maskname, newname))
    f.close()


if __name__ == '__main__':
    """Command line invocation setup."""    

    ncore = 1
    overwrite = False

    # Process argv
    if len(sys.argv[1:]) != 2:
        raise ValueError("Two arguments are required.")
    roinames, newnames = load_roifile(sys.argv[1])
    expname = sys.argv[2]
   
    # Cleaup success log from previous runs
    try:
        os.remove("{0}_roinii.log".format(expname))
    except OSError:
        pass

    # Go, multpprocess on request
    if ncore == 1:
        [create(roiname, newname, expname, overwrite) for
                roiname, newname in zip(roinames, newnames)] 
    elif ncore > 1:
        p = Pool(ncore)
        for roiname, newname in zip(roinames, newnames):
            p.apply_async(create, args = (roiname, newname, expname, overwrite))
        p.close()
        p.join()
    else:
        raise ValueError("ncore must be 1 or greater")

