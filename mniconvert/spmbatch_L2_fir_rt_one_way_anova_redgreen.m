% !!!!!!!!!!!!!!!!!!!
% ASSUMES that L1 was a factorial analysis for RT using a FIR basis of order 15
% !!!!!!!!!!!!!!!!!!!

clc;
clear all;

% SPM go!
spm('Defaults','fMRI');
spm_jobman('initcfg'); 
    %% SPM8 only

clear matlabbatch

%-----------------------------------------------------------------------
% Job configuration created by cfg_util (rev $Rev: 4252 $)
%-----------------------------------------------------------------------
matlabbatch{1}.spm.stats.factorial_design.dir = {'/data/data2/meta_accumulate/redgreen/rfx/RT/fir/'};
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.name = 'RT_fir';
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.levels = 3*15; % 3 rt * 15 fir
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.dept = 0; % there is dep between fir est
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.variance = 1;  % unequal var
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.gmsca = 0;
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.ancova = 0;

% Specifiy cells - one per level
for ii=1:45,     
    if (ii+2) < 10
        conname = ['con_000' num2str(ii+2)]     %% First cons number are main/average effect for L1
                                                %% so we need to offset
    else
        conname = ['con_00' num2str(ii+2)]
    end
    matlabbatch{1}.spm.stats.factorial_design.des.fd.icell(ii).levels = [1
                                                                        ii];
    matlabbatch{1}.spm.stats.factorial_design.des.fd.icell(ii).scans = {
        ['/data/data2/meta_accumulate/redgreen/redgreen1/redgreen1_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen10/redgreen10_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen11/redgreen11_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen12/redgreen12_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen14/redgreen14_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen15/redgreen15_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen16/redgreen16_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen17/redgreen17_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen2/redgreen2_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen22/redgreen22_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen24/redgreen24_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen25/redgreen25_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen5/redgreen5_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen7/redgreen7_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen8/redgreen8_rt_fir/' conname '.img,1']
        ['/data/data2/meta_accumulate/redgreen/redgreen9/redgreen9_rt_fir/' conname '.img,1']
    }; 

end

matlabbatch{1}.spm.stats.factorial_design.cov = struct('c', {}, 'cname', {}, 'iCFI', {}, 'iCC', {});
matlabbatch{1}.spm.stats.factorial_design.masking.tm.tm_none = 1;
matlabbatch{1}.spm.stats.factorial_design.masking.im = 1;
matlabbatch{1}.spm.stats.factorial_design.masking.em = {''};
matlabbatch{1}.spm.stats.factorial_design.globalc.g_omit = 1;
matlabbatch{1}.spm.stats.factorial_design.globalm.gmsca.gmsca_no = 1;
matlabbatch{1}.spm.stats.factorial_design.globalm.glonorm = 1;

% RUN
spm_jobman('run',matlabbatch);

exit;
