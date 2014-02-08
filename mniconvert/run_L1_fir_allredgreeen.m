clc;
clear all;

addpath('~/src/wheelerdata/mniconvert/spm/')

DATAPATH = '/data/data2/meta_accumulate/redgreen/'

Ss = {'/redgreen1' '/redgreen2' '/redgreen5' '/redgreen7' '/redgreen8' '/redgreen9' '/redgreen10' '/redgreen11' '/redgreen12' '/redgreen14' '/redgreen15' '/redgreen16' '/redgreen17' '/redgreen19' '/redgreen22' '/redgreen24' '/redgreen25'}

NODS = {'redgreen1' 'redgreen2' 'redgreen5' 'redgreen7' 'redgreen8' 'redgreen9' 'redgreen10' 'redgreen11' 'redgreen12' 'redgreen14' 'redgreen15' 'redgreen16' 'redgreen17' 'redgreen19' 'redgreen22' 'redgreen24' 'redgreen25'}

for ii=1:size(Ss,2),
    disp(Ss{ii})
    datadir = fullfile(DATAPATH,Ss{ii})

    % ----
    disp('Calculating L1 reaction time')
    savedir = [Ss{ii} '_rt_fir']
    [stat, meSs] = rmdir(fullfile(datadir,savedir), 's')  
    meta_L1_fir(datadir,savedir,'warredgreen.nii', ...
        ['fidl/nod_' NODS{ii} '_rt_event.mat'], ...
        'rp_redgreen0.txt', 2, 38, 'RT', 3)
end

exit;
