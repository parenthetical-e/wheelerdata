% To examine the results from the below, load the created SPM
% choose a F contrast and enter 'eye(16)' in the contrast box

contrastdir = '/data/data2/meta_accumulate/fh/contrasts/motor_fir'

%-----------------------------------------------------------------------
% Job configuration created by cfg_util (rev $Rev: 4252 $)
%-----------------------------------------------------------------------
matlabbatch{1}.spm.stats.factorial_design.dir = {'/data/data2/meta_accumulate/fh/rfx/motor_respXtime'};
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.name = 'respXtime';
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.levels = 16;
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.dept = 1;
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.variance = 1;
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.gmsca = 0;
matlabbatch{1}.spm.stats.factorial_design.des.fd.fact.ancova = 0;

% Want to contrasts for main effect of resp, i.e 19-34.
% which is the why the index is shited by 18
for ii=1:16,
    matlabbatch{1}.spm.stats.factorial_design.des.fd.icell(ii).levels = ii;
    matlabbatch{1}.spm.stats.factorial_design.des.fd.icell(ii).scans = cellstr(spm_select('FPList',contrastdir,['con_00' num2str(ii+18)]))
end

matlabbatch{1}.spm.stats.factorial_design.cov = struct('c', {}, 'cname', {}, 'iCFI', {}, 'iCC', {});
matlabbatch{1}.spm.stats.factorial_design.masking.tm.tm_none = 1;
matlabbatch{1}.spm.stats.factorial_design.masking.im = 1;
matlabbatch{1}.spm.stats.factorial_design.masking.em = {''};
matlabbatch{1}.spm.stats.factorial_design.globalc.g_omit = 1;
matlabbatch{1}.spm.stats.factorial_design.globalm.gmsca.gmsca_no = 1;
matlabbatch{1}.spm.stats.factorial_design.globalm.glonorm = 1;
