%-----------------------------------------------------------------------
% Job configuration created by cfg_util (rev $Rev: 4252 $)
%-----------------------------------------------------------------------
matlabbatch{1}.spm.stats.factorial_design.dir = {'/data/data2/meta_accumulate/fh/rfx/motor/anova/'};
%%
matlabbatch{1}.spm.stats.factorial_design.des.anova.icell(1).scans = {
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh09_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh11_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh13_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh14_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh15_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh17_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh19_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh21_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh23_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh24_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh25_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh26_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh27_con_0003.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh28_con_0003.img,1'
                                                                      };
%%
%%
matlabbatch{1}.spm.stats.factorial_design.des.anova.icell(2).scans = {
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh09_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh11_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh13_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh14_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh15_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh17_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh19_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh21_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh23_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh24_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh25_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh26_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh27_con_0004.img,1'
                                                                      '/data/data2/meta_accumulate/fh/contrasts/motor//fh28_con_0004.img,1'
                                                                      };
%%
matlabbatch{1}.spm.stats.factorial_design.des.anova.dept = 0;
matlabbatch{1}.spm.stats.factorial_design.des.anova.variance = 1;
matlabbatch{1}.spm.stats.factorial_design.des.anova.gmsca = 0;
matlabbatch{1}.spm.stats.factorial_design.des.anova.ancova = 0;
matlabbatch{1}.spm.stats.factorial_design.cov = struct('c', {}, 'cname', {}, 'iCFI', {}, 'iCC', {});
matlabbatch{1}.spm.stats.factorial_design.masking.tm.tm_none = 1;
matlabbatch{1}.spm.stats.factorial_design.masking.im = 1;
matlabbatch{1}.spm.stats.factorial_design.masking.em = {''};
matlabbatch{1}.spm.stats.factorial_design.globalc.g_omit = 1;
matlabbatch{1}.spm.stats.factorial_design.globalm.gmsca.gmsca_no = 1;
matlabbatch{1}.spm.stats.factorial_design.globalm.glonorm = 1;
matlabbatch{2}.spm.stats.fmri_est.spmmat = {'/data/data2/meta_accumulate/fh/rfx/motor/anova/SPM.mat'};
matlabbatch{2}.spm.stats.fmri_est.method.Classical = 1;
matlabbatch{3}.spm.stats.con.spmmat = {'/data/data2/meta_accumulate/fh/rfx/motor/anova/SPM.mat'};
matlabbatch{3}.spm.stats.con.consess{1}.tcon.name = 'L > R';
matlabbatch{3}.spm.stats.con.consess{1}.tcon.convec = [1 -1];
matlabbatch{3}.spm.stats.con.consess{1}.tcon.sessrep = 'none';
matlabbatch{3}.spm.stats.con.consess{2}.tcon.name = 'L < R';
matlabbatch{3}.spm.stats.con.consess{2}.tcon.convec = [-1 1];
matlabbatch{3}.spm.stats.con.consess{2}.tcon.sessrep = 'none';
matlabbatch{3}.spm.stats.con.delete = 1;
matlabbatch{4}.spm.stats.results.spmmat = {'/data/data2/meta_accumulate/fh/rfx/motor/anova/SPM.mat'};
matlabbatch{4}.spm.stats.results.conspec.titlestr = 'L > R';
matlabbatch{4}.spm.stats.results.conspec.contrasts = Inf;
matlabbatch{4}.spm.stats.results.conspec.threshdesc = 'FWE';
matlabbatch{4}.spm.stats.results.conspec.thresh = 0.05;
matlabbatch{4}.spm.stats.results.conspec.extent = 4;
matlabbatch{4}.spm.stats.results.conspec.mask = struct('contrasts', {}, 'thresh', {}, 'mtype', {});
matlabbatch{4}.spm.stats.results.units = 1;
matlabbatch{4}.spm.stats.results.print = true;
matlabbatch{5}.spm.stats.results.spmmat = {'/data/data2/meta_accumulate/fh/rfx/motor/anova/SPM.mat'};
matlabbatch{5}.spm.stats.results.conspec.titlestr = 'L > R';
matlabbatch{5}.spm.stats.results.conspec.contrasts = Inf;
matlabbatch{5}.spm.stats.results.conspec.threshdesc = 'none';
matlabbatch{5}.spm.stats.results.conspec.thresh = 0.0001;
matlabbatch{5}.spm.stats.results.conspec.extent = 4;
matlabbatch{5}.spm.stats.results.conspec.mask = struct('contrasts', {}, 'thresh', {}, 'mtype', {});
matlabbatch{5}.spm.stats.results.units = 1;
matlabbatch{5}.spm.stats.results.print = true;
matlabbatch{6}.spm.stats.results.spmmat = {'/data/data2/meta_accumulate/fh/rfx/motor/anova/SPM.mat'};
matlabbatch{6}.spm.stats.results.conspec.titlestr = 'L > R';
matlabbatch{6}.spm.stats.results.conspec.contrasts = Inf;
matlabbatch{6}.spm.stats.results.conspec.threshdesc = 'none';
matlabbatch{6}.spm.stats.results.conspec.thresh = 0.001;
matlabbatch{6}.spm.stats.results.conspec.extent = 4;
matlabbatch{6}.spm.stats.results.conspec.mask = struct('contrasts', {}, 'thresh', {}, 'mtype', {});
matlabbatch{6}.spm.stats.results.units = 1;
matlabbatch{6}.spm.stats.results.print = true;
