"""usage: dcm_to_nifti expname mapname scode"""
import sys, os, re
from subprocess import Popen, PIPE


def _dobash(cmd):
    """Execute 'cmd' (a str) in bash, returns STDOUT as a str."""

    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    stdout = p.communicate()
            
    return stdout


def _process_exp(exp):
    """Use the exp name to return the names of the MPRAGE 
    data and the bold data (in that order).
    """
     
    if exp == "fh":
        mpragename = "mprage"
        boldname = "fh"
    else:
        raise ValueError("exp name not understood.")
    
    return mpragename, boldname


def _parse_ana():
    """After a dcm to nifti conversion of MPRAGE (i.e anatomical) data
    there should be three nii files matching the following form

        *.nii
        o*.nii
        co*nii
    
    This function checks the PWD for these and returns their full names
    in the order listed above."""

    ana = None
    ana_o = None
    ana_co = None

    files = os.listdir(".")
    for fi in files:
        finame, ext = os.path.splitext(fi)
        if ext == ".nii":
            if re.match("co", finame):
                ana_co = finame + ext
            elif re.match("o", finame):
                ana_o = finame + ext
            else:
                ana = finame + ext
    return ana, ana_o, ana_co


def _dcm2nii_ana(dirname, niiname, move=True):
    initialdir = os.getcwd()

    os.chdir(dirname) 
    _dobash("dcm2nii *")
    
    ana, ana_o, ana_co = _parse_ana()
    _dobash("mv {0} {1}.nii".format(ana, niiname))
    _dobash("mv {0} {1}_o.nii".format(ana_o, niiname))
    _dobash("mv {0} {1}_co.nii".format(ana_co, niiname))

    if move:
        _dobash("mv *.nii ..".format(niiname))

    os.chdir(initialdir)


def _dcm2nii(dirname, niiname, move=True):
    """Convert dicoms into a nifti file. 
    
    Parameters
    ----------
    dirname - name of the dir with rhe .dcms in it
    niiname - what to name the resulting dicom file
    move - If True, the nifti file into the parent dir.
        It is often the case that the dcm data is in a subdir

    Note:
    ----
    Uses dcm2nii to do the converison.  
    
    http://www.mccauslandcenter.sc.edu/mricro/mricron/dcm2nii.html

    Any customization, subformating, etc, should be handled using the
    dcm2nii config file (which should be in ~/.dcm2nii/dcm2nii.ini).
    """

    initialdir = os.getcwd()
    niiname = niiname+".nii"

    os.chdir(dirname)
    
    _dobash("dcm2nii *")
    _dobash("mv *.nii {0}".format(niiname))

    if move:
        _dobash("mv {0} ..".format(niiname))

    os.chdir(initialdir)


if __name__ == "__main__":
    
    # Process args
    expname = sys.argv[1]
    mapname = sys.argv[2]
    scode = int(sys.argv[3])
    
    # Get the bold map
    mrimap = eval(open(mapname).read())[scode]
     
    # Use the exp name to get the location (scan)
    # codes of the data
    mpragename, boldname = _process_exp(expname)
    mprage = mrimap[mpragename]
    bolds = mrimap[boldname]
    
    # Note:
    # ----
    # We assume the all the MRI data is in dirs in the PWD
    # with the format of studyX or studyXX, where X is a single
    # or double digit int

    # Do ana
    _dcm2nii_ana("study{0}".format(mprage[0]), "ana", move=True)
    
    # Loop over, doing each BOLD (epi) scan.
    for ii, bold in enumerate(bolds):
        _dcm2nii("study{0}".format(bold), 
                "{0}{1}".format(expname, ii), 
                move=True)


