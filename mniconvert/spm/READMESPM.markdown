Read me carefully!  These functions make some strong assumptions about file names and directory structures.

# Directory structure
By example:

    ROOT
     \ subcode
             \studyX
             \studyXX

* Where ROOT is the top level
* subcode is the name of the _a_ subjects data
* and studyX(X) are the dicom folders

After the preprocessing scripts are done then in addition to the above ROOT
shoud also contain the dicom data (and all the other files not shown here -
these will have names following the fcode and ana.nii designations).

    ROOT
     \ subcode
            \ ana.nii
            \ fcode0.nii
            \ fcode1.nii
            \ ...

* Where ana.nii is the anatomical (i.e. MPRAGE) data, and fcode0 (etc) is the functional data runs.

# Mandatory file names
* Functional data can be named anything, 
* but anatomical _must_ _MUST_ be named ana.nii

# Specific functions
* Details about cr_ana
 - In addition to some mat files (see SPM8 docs for details on these) this
   function produced three nifti files c1ana.nii and c2ana.nii.  
   - c1 is the grey matter mask, c2 is the white matter mask.
   - Not sure what mana.nii is.

* Details about cr_realign
 - No matter the name of the functional data (i.e. fcode) the averaged
   functional image needed for ana-functional alignment will be called
   meanfunc.nii

* Details about cr_func
 - TODO

