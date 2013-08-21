# Notes

* Below is Avi's instructions for the use of 'preprocess_into_mni152', which he called 'cross_bold_pp_121215' but that was a not-descriptive name so I changed it.

		The attached should get you started.
		Put MNI*ifh and cross_bold*csh in $RELEASE.
		APsub1.params is the subject-specific params file (I had to assign some
		name to the subject).
		butterfly.params is intended to be group-wide (maybe "butterfly" is not
		the best name for this particular group).
		cross_bold_pp_121215.csh should be invoked inside the subject directory.

		The general idea is to use the subject-specific params file, which
		generally will reside in the subject directory, only for subject-specific
		info (e.g., what study number corresponds to what acquisition). The
		group-specfic params file (i.e., the instructions file) can reside
		anywhere. It can be referenced including a path when invoking the
		cross_bold_pp script. butterfly.params specifies MNI152 output ($to_MNI152
		== 1). If $to_MNI152 == 0 (or to_MNi52 is undefined) the output will be in
		711-2B space.

		One detail that may be slightly inconvenient is that the cross_bold_pp
		script looks for DICOMs in subdirectories of $inpath (which may be the
		subject directory, i.e., $cwd) named study$k where $k corresponds to the
		study number. Thus, in the case of APsub1, $inpath contains {study3/
		study4/ study8/ study13}. This directory structure can be easily generated
		from, e.g., {3/ 4/ 8/ 13}. And (this is crucial) the DICOM directories
		must contain *ONLY* DICOM (i.e., no extraneous files). It may be
		convenient to create {study$k/} subdirectories using a script and symbolic
		links.

		I recommend redirecting cross_bold_pp_121215.csh stdout to a log file,
		e.g.,

		cross_bold_pp_121215.csh APsub1.params ../butterfly.params >!
		APsub1_cross_bold_pp_121215.log


		The log file provides a good basis for debugging if anything goes wrong.

		To convert 4dfp output to NIfTI use nifti_4dfp -n


		If you have multiple session data on the same subject there is a bit more
		to know (but I take it that you do not).

		Let me know when/if the preprocessing is working. We can then discuss QA
		scripts covering image registration including atlas transformation, motion
		quantitation and SNR.

 
* The 711-2V was needed and not found. I had to copy into ./fidl/lib/ a new copy of all the 711-* templates, among many others.

* Updated templates were pulled (as per Avi's instructions) from ftp://imaging.wustl.edu/pub/raichlab/4dfp_tools/refdfir.tar


# Preprocessing of Ploran 2007 (1)
* 'x' in some of the top subject directories means the following scan number (i.e. x9 or 10 or both) were excluded from fMRI processing and all remaining analyses.
* Once the test subject was working (S4) I created 'run_pre_ploran.sh' to iterate over all the Ss and preprocess them.  See that file, and its log ('run_pre_ploran.log') for details.  
* Prior to this I shifted all the dcm data (study* folders) to the top level of S*.  They were jumbled before this.
* The first run of 'run_pre_ploran.sh' suggests the following subjects failed.  The errors for each are different.
 - S19x10
 - S23x10
* S19x10.params had a stray equals sign.  Processing now ok.
* S23x10 had one to many entries in 'set irun = (...)' portion of its .param file.  Processing now ok.
* I checked the pre.log files for the rest to confirm that everything was ok.  It was.
* Select 4dfp bold and anatomical data was then converted to nifti (see to_nifti.pl and convert.log files for details).
