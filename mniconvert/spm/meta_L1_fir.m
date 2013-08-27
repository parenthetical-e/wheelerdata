function meta_L1_fir(basepath,savename,func_name,nod_name,movement_name,tr,nslice,event,cond_name,n_levels),
% Run a Level 1 analysis.
%
% meta_L1(savename,func_name,nod_name,movement_name,tr,nslice,event)
%
% <basepath> - a top location of the top-level directory to work in
%           and save data into.
% <savename> where all the SPM files will end up
% <func_name> - the name of the functional data
% <nod_name> - the name of the nod_* data
% <movement_name> - the name of the SPM-generated movement file
% <tr> - the TR
% <nslice> - the number of slices / TR
% <event> If is 1, set durations to 0. If 0, use nod_* durations.

	% Intial var setup
	old_path = pwd;
	data_path = fullfile(basepath);
    
	% Create the dir for the model files, if necessary.
	if exist(fullfile(data_path,savename),'dir') ~= 7,
		mkdir(fullfile(data_path,savename));
	end

    % Get the nod data
    load(fullfile(data_path,nod_name))
            %% Creates names, onsets, durations - cell arrays
	
	% SPM go!
	spm('Defaults','fMRI');
	spm_jobman('initcfg'); 
		%% SPM8 only

	clear jobs
	
    % DIRECTORY SETUP
	jobs{1}.util{1}.cdir.directory = cellstr(data_path);
		%% set wd	

	jobs{1}.util{1}.md.basedir = cellstr(data_path);
	% jobs{1}.util{1}.md.name = savename;
		%% Output lives here

	% MODEL SPECIFICATION
	jobs{2}.stats{1}.fmri_spec.dir = cellstr(fullfile(data_path,savename));
	jobs{2}.stats{1}.fmri_spec.timing.units = 'scans';
	jobs{2}.stats{1}.fmri_spec.timing.RT = tr;
	jobs{2}.stats{1}.fmri_spec.timing.fmri_t = nslice;
	jobs{2}.stats{1}.fmri_spec.timing.fmri_t0 = floor(nslice/2);
	
    f = spm_select('ExtFPListRec',data_path,['^' func_name],Inf);
    jobs{2}.stats{1}.fmri_spec.sess(1).scans = f;

    % Movement regressor, hardcode
    jobs{2}.stats{1}.fmri_spec.sess(1).multi_reg = cellstr(...
            fullfile(data_path,movement_name));
     
    % Setup each col in the design matrix
    for jj=1:size(names,2),
		names{jj}
		onset{jj}
        jobs{2}.stats{1}.fmri_spec.sess(1).cond(jj).name = names{jj};
        jobs{2}.stats{1}.fmri_spec.sess(1).cond(jj).onset = onsets{jj};

        % Do events or epoch-like (or slow)
        if event == 1,
            jobs{2}.stats{1}.fmri_spec.sess(1).cond(jj).duration = 0;
        elseif event == 0,
            jobs{2}.stats{1}.fmri_spec.sess(1).cond(jj).duration = ...
                    durations{jj};
        else,
            error('<event> must be 0 or 1.');
        end
    end

    jobs{2}.stats{1}.fmri_spec.sess.hpf = 128;
    jobs{2}.stats{1}.fmri_spec.fact.name = cond_name;
    jobs{2}.stats{1}.fmri_spec.fact.levels = n_levels;
    jobs{2}.stats{1}.fmri_spec.bases.fir.length = 24;
    jobs{2}.stats{1}.fmri_spec.bases.fir.order = 16;
    jobs{2}.stats{1}.fmri_spec.volt = 1;
    jobs{2}.stats{1}.fmri_spec.global = 'Scaling';
    jobs{2}.stats{1}.fmri_spec.mask = {''};
    jobs{2}.stats{1}.fmri_spec.cvi = 'AR(1)'

	% Factorial info
	% jobs{2}.stats{1}.fmri_spec.fact.name = cond_code
	% jobs{2}.stats{1}.fmri_spec.fact.levels = num_levels
	
	% HRF choice and params
	% jobs{2}.stats{1}.fmri_spec.bases.hrf.derivs = [1 1];
		%% the [1 1] adds time and 
		%% dispersion to the canonical HRF.

	% MODEL ESTIMATION
	jobs{2}.stats{2}.fmri_est.spmmat = cellstr(fullfile( ...
            data_path,savename,'SPM.mat'));

	jobs{3}.util{1}.cdir.directory = cellstr(old_path);
		%% reset wd	

	% RUN
	spm_jobman('run',jobs);
end
