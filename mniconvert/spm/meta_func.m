function meta_func(dir_path,func_name,tr,nslice,sliceorder,refslice,isovox),
% Preprocess <func_name> in <dir_path>, using ana.nii to coregister.

	% SPM go!
	spm('Defaults','fMRI');
	spm_jobman('initcfg'); 
		%% SPM8 only

	clear jobs
	jobs{1}.util{1}.cdir.directory = cellstr(dir_path);
		%% set wd	

	% LOCATE DATA
    f = spm_select('ExtList', dir_path, ['^' func_name '+\d\.nii$'],1:5000);
        %% Matches 'func_nameX.nii' where X is one or more integers.
        %% Assume a nifti set won't have more than 5000 slices.

	a = spm_select('FPList', dir_path, ['^ana.nii$']);
		%% This returns absolute path of every volumne in func_name or 
		%% ana_name which we assume is a 4d nifti file
	
	% SLICE TIMING CORRECTION
	jobs{2}.temporal{1}.st.scans{1} = editfilenames(f,'prefix','r');
	jobs{2}.temporal{1}.st.nslices = nslice;
	jobs{2}.temporal{1}.st.tr = tr;
	jobs{2}.temporal{1}.st.ta = tr-tr/nslice;
	jobs{2}.temporal{1}.st.so = sliceorder;
	jobs{2}.temporal{1}.st.refslice = refslice;

	% COREGISTRATION
	jobs{3}.spatial{1}.coreg{1}.estimate.ref = cellstr('meanfunc.nii');
	jobs{3}.spatial{1}.coreg{1}.estimate.source = cellstr(a);
	
	% NORMALIZE
	% Esitimate between ana and t1.nii
	jobs{3}.spatial{2}.normalise{1}.write.subj.matname  = editfilenames(...
			a,'suffix','_seg_sn','ext','.mat');

	ff = cellstr('meanfunc.nii');
    
    jobs{3}.spatial{2}.normalise{1}.write.subj.resample = [editfilenames(...
			f,'prefix','ar'); ff];
	jobs{3}.spatial{2}.normalise{1}.write.roptions.vox = isovox;
	jobs{3}.spatial{2}.normalise{1}.write.roptions.interp = 4;
		%% 4th degree B spline
	
	% Go!
	spm_jobman('run',jobs);
end
