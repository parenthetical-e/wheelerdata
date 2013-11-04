"""Extract subject ROIs for the selected Wheeler Lab experiment.

Usage: roinii roifile expname
"""
import re, os, sys
import nibabel as nb

from fmrilearn.preprocess.nii import masknii
from fmrilearn.load import load_roifile

from wheelerdata.load import fh
from wheelerdata.load import butterfly
from wheelerdata.load import clock
from wheelerdata.load import polygon
from wheelerdata.load import redgreen
from multiprocessing import Pool


def create(maskname, newname, expname, overwrite=False):
    # Experimental config 
    basepath, path, scodes, datas = None, None, None, None
    if expname == "fh":
        basepath = fh.get_datapath()
        paths = fh.get_subject_paths()
        scodes = fh.get_subject_codes()
        datas = [os.path.join(path, "arfh.nii") for path in paths]
    elif expname == "butterfly":
        basepath = butterfly.get_datapath()
        paths = butterfly.get_subject_paths()
        scodes = butterfly.get_subject_codes()
        datas = [os.path.join(path, "arbutterfly.nii") for path in paths]
    elif expname == "clock":
        basepath = clock.get_datapath()
        paths = clock.get_subject_paths()
        scodes = clock.get_subject_codes()
        datas = [os.path.join(path, "arclock.nii") for path in paths]
    elif expname == "polygon":
        basepath = polygon.get_datapath()
        paths = polygon.get_subject_paths()
        scodes = polygon.get_subject_codes()
        datas = [os.path.join(path, "arpolygon.nii") for path in paths]
    elif expname == "redgreen":
        basepath = redgreen.get_datapath()
        paths = redgreen.get_subject_paths()
        scodes = redgreen.get_subject_codes()
        datas = [os.path.join(path, "arredgreen.nii") for path in paths]    
    else:
        raise ValueError("expname ({0}) not valid".format(expname))

    # then create the roi data for each S.
    for s, data in zip(scodes, datas):
        saveas = os.path.join(
                basepath, 'roinii', "{0}_{1}.nii.gz".format(newname, s))

        if overwrite:
            print("Overwriting {0}.".format(saveas))
            masknii(maskname, data, save=saveas)
        elif os.path.exists(saveas):
            print("{0} exists, moving on.".format(saveas))
            continue
        else:
            masknii(maskname, data, save=saveas)


if __name__ == '__main__':
    """Command line invocation setup."""    

    ncore = 1

    # Process argv
    if len(sys.argv[1:]) != 2:
        raise ValueError("Two arguments are required.")
    roinames, newnames = load_roifile(sys.argv[1])
    expname = sys.argv[2]

    # Go, multpprocess on request    
    if ncore == 1:
        [create(roiname, newname, expname) for
                roiname, newname in zip(roinames, newnames)] 
    elif ncore > 1:
        p = Pool(ncore)
        for roiname, newname in zip(roinames, newnames):
            p.apply_async(create, args = (roiname, newname, expname))
        p.close()
        p.join()
    else:
        raise ValueError("ncore must be 1 or greater")
