function meta_contrast_fir_stim_facehouse(data_path,delete_old),
% meta_contrast_stim_facehouse(data_path,delete_old)
% 
% <data_path> - the location of the SPM.mat you want to use
%   Note: all contrast files end up here
% <delete_old> - Keep (0) or delete (1) old contrasts 

    % Init
    firwindow = 11;

    % ---
    % SPM go!
    spm('Defaults','fMRI');
    spm_jobman('initcfg'); 
    clear jobs
        %% SPM8 only
    
    % Directory setup
    olddir = pwd;
    jobs{1}.util{1}.cdir.directory = cellstr(data_path);
    jobs{1}.util{1}.md.basedir = cellstr(data_path);

    % Create contrasts!
    jobs{2}.stats{1}.con.spmmat =  cellstr( ...
            fullfile(data_path,'SPM.mat'))

    cvecfh = [repmat(1, 1, firwindow) repmat(-1, 1, firwindow)]
    jobs{2}.stats{1}.con.consess{1}.fcon.name = 'face > house';
    jobs{2}.stats{1}.con.consess{1}.fcon.convec = {cvecfh};
    jobs{2}.stats{1}.con.consess{1}.fcon.sessrep = 'none';

    cvechf = [repmat(-1, 1, firwindow) repmat(1, 1, firwindow)]
    jobs{2}.stats{1}.con.consess{2}.fcon.name = 'face < house';
    jobs{2}.stats{1}.con.consess{2}.fcon.convec = {cvechf};
    jobs{2}.stats{1}.con.consess{2}.fcon.sessrep = 'none';

    cvecf = [repmat(1, 1, firwindow) repmat(0, 1, firwindow)]
    jobs{2}.stats{1}.con.consess{3}.fcon.name = 'Face';
    jobs{2}.stats{1}.con.consess{3}.fcon.convec = {cvecf};
    jobs{2}.stats{1}.con.consess{3}.fcon.sessrep = 'none';

    cvech = [repmat(0, 1, firwindow) repmat(1, 1, firwindow)]
    jobs{2}.stats{1}.con.consess{4}.fcon.name = 'House';
    jobs{2}.stats{1}.con.consess{4}.fcon.convec = {cvech};
    jobs{2}.stats{1}.con.consess{4}.fcon.sessrep = 'none';

    jobs{2}.stats{1}.con.delete = delete_old;

    % Run them with the following threshold parameters
    jobs{2}.stats{2}.results.spmmat = cellstr( ...
            fullfile(data_path,'SPM.mat'));
    jobs{2}.stats{2}.results.conspec.titlestr = 'FWE, p < 0.05';
    jobs{2}.stats{2}.results.conspec.contrasts = Inf;
    jobs{2}.stats{2}.results.conspec.threshdesc = 'FWE';
    jobs{2}.stats{2}.results.conspec.thresh = 0.05;
    jobs{2}.stats{2}.results.conspec.extent = 4;
    jobs{2}.stats{2}.results.units = 1;
    jobs{2}.stats{2}.results.print = false;
     
    % Reset dir
    jobs{3}.util{1}.cdir.directory = cellstr(olddir);
    
    % Go!
    spm_jobman('run',jobs);
end
