"""Apply the mask to the nifiti data

Usage: roinii_fh_custom path/to/mask.hdr
"""
import os
import sys
import nibabel as nb
from roi.pre import mask as masknii


if __name__ == "__main__":
 
    # ----
    # Create a place for the roi data to 
    # live if necessary.
     
    # ----
    # Process argv
    if len(sys.argv[1:]) != 1:
        raise ValueError("One argument are required.")
    mask = sys.argv[1]

    try:
        os.mkdir("./roinii")
    except OSError:
        pass

    basepath = "/data/data2/meta_accumulate/fh"
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
    

    for scode, nii in subdatatable.items():
        print("Masking {0} with {1}.".format(nii, mask))
        
        # Isolate the maskname from its path
        _, maskname = os.path.split(mask)
        maskname, _ = os.path.splitext(maskname)

        nii_data = nb.load(nii)
        mask_data = nb.load(mask)
        masked_nii_data = masknii(nii_data, mask_data, standard=False)
                ## Even though we're in MNI152 the q_form
                ## for the fidl converted data is not set correctly
                ## the s_form is what the q should be
                ## thus standard=False

        saveas = os.path.join(
            basepath, "roinii", "{0}_{1}.nii.gz".format(maskname, scode))
        
        print("Saving {0}.".format(saveas))       
        nb.save(masked_nii_data, saveas)

