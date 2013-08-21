function meta_L2_onesided_t(basedir,save_dir,contrast_basename,title,display_results),

    % Use contrast_basename to create find 
    % all the appropriate contrasts
    % files in basedir
    contrasts = spm_select( ...
            'FPList', basedir, [contrast_basename '.img$'],Inf)

    spm('Defaults','fMRI');
	spm_jobman('initcfg'); 
	clear jobs
		%% SPM8 only
    
    % Create the SPM.mat 
    jobs{1}.stats{1}.factorial_design.dir = {save_dir}
    jobs{1}.stats{1}.factorial_design.des.t1.scans = cellstr(contrasts)
    jobs{1}.stats{1}.factorial_design.cov = struct('c', {}, ... 
            'cname', {}, 'iCFI', {}, 'iCC', {});
    jobs{1}.stats{1}.factorial_design.masking.tm.tm_none = 1;
    jobs{1}.stats{1}.factorial_design.masking.im = 1;
    jobs{1}.stats{1}.factorial_design.masking.em = {''};
    jobs{1}.stats{1}.factorial_design.globalc.g_omit = 1;
    jobs{1}.stats{1}.factorial_design.globalm.gmsca.gmsca_no = 1;
    jobs{1}.stats{1}.factorial_design.globalm.glonorm = 1;
    
    % Run the statitics
    jobs{2}.stats{1}.fmri_est.spmmat = cellstr(...
            fullfile(save_dir,'SPM.mat'));
    jobs{2}.stats{1}.fmri_est.method.Classical = 1;

    % and the contrast
    jobs{3}.stats{1}.con.spmmat = cellstr(...
                fullfile(save_dir,'SPM.mat'));    
    jobs{3}.stats{1}.con.consess{1}.fcon.name = save_dir;
    jobs{3}.stats{1}.con.consess{1}.fcon.convec = {1};
    jobs{3}.stats{1}.con.consess{1}.fcon.sessrep = 'none';
    jobs{3}.stats{1}.con.delete = 1;

    % Generate thresholded map and .ps file?
    if display_results,
        jobs{4}.stats{1}.results.spmmat = cellstr(...
               fullfile(save_dir,'SPM.mat'));
        jobs{4}.stats{1}.results.conspec.titlestr = title;
        jobs{4}.stats{1}.results.conspec.contrasts = 1;
        jobs{4}.stats{1}.results.conspec.threshdesc = 'FWE';
        jobs{4}.stats{1}.results.conspec.thresh = 0.05;
        jobs{4}.stats{1}.results.conspec.extent = 4;
        jobs{4}.stats{1}.results.conspec.mask = struct('contrasts', {},...
               'thresh', {}, 'mtype', {});
        jobs{4}.stats{1}.results.units = 1;
        jobs{4}.stats{1}.results.print = true;

        jobs{5}.stats{1}.results.spmmat = cellstr(...
              fullfile(save_dir,'SPM.mat'));
        jobs{5}.stats{1}.results.conspec.titlestr = title;
        jobs{5}.stats{1}.results.conspec.contrasts = 1;
        jobs{5}.stats{1}.results.conspec.threshdesc = 'FWE';
        jobs{5}.stats{1}.results.conspec.thresh = 0.10;
        jobs{5}.stats{1}.results.conspec.extent = 4;
        jobs{5}.stats{1}.results.conspec.mask = struct('contrasts', {},...
              'thresh', {}, 'mtype', {});
        jobs{5}.stats{1}.results.units = 1;
        jobs{5}.stats{1}.results.print = true;

        jobs{6}.stats{1}.results.spmmat = cellstr(...
              fullfile(save_dir,'SPM.mat'));
        jobs{6}.stats{1}.results.conspec.titlestr = 'Uncorr 0.001';
        jobs{6}.stats{1}.results.conspec.contrasts = Inf;
        jobs{6}.stats{1}.results.conspec.threshdesc = 'none';
        jobs{6}.stats{1}.results.conspec.thresh = 0.001;
        jobs{6}.stats{1}.results.conspec.extent = 4;
        jobs{6}.stats{1}.results.units = 1;
        jobs{6}.stats{1}.results.print = true;
    end

	% RUN
	spm_jobman('run',jobs);
end
