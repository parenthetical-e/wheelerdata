function cr_realign(dir_path,func_names),
% Realign *all* catreward functional data in <dir_path>.
% cr_realign(dir_path, func_names) 
%
% Notes:
% * Face/house info:
%  - func_names: {'fh0' 'fh1' 'fh2' 'fh3' 'fh4' 'fh5' 'fh6'};

	% SPM go!
	spm('Defaults','fMRI');
	spm_jobman('initcfg'); 
		% SPM8 only

	% Set the wd.
	clear jobs
	jobs{1}.util{1}.cdir.directory = cellstr(dir_path);
	
	% REALIGN, do it for all functional data.
	% Get all file names and volumne counts for each
	% of the functional sets, in order.
	allf = {};
	for ii=1:size(func_names,2),
		func_name = func_names{ii};
		cf = cellstr(spm_select( ...
			'ExtList', dir_path, ['^' func_name '\.nii$'], 1:10000));
		allf = cat(1,allf,cf);
	end
	jobs{2}.spatial{1}.realign{1}.estwrite.data{1} = allf;

	% RUN
	spm_jobman('run',jobs);
	
	movefile(['mean' func_names{1} '.nii'],'meanfunc.nii');
	    %% spm uses the first filename for the mean image,
		%% but the mean imag will relfect all the functional data
		%% do we rename it. 
        %%
        %% The name/file meanfunc.nii is assumed to be constant/present
        %% for all subsequent processing steps.
end
