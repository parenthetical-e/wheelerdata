addpath('~/src/metaaccumulate/mniconvert/spm/')

DATAPATH = '/data/data2/meta_accumulate/fh/'

Ss = {'/fh09' '/fh11' '/fh13' '/fh14' '/fh15' '/fh17' '/fh19' '/fh21' '/fh23' '/fh24' '/fh25' '/fh26' '/fh27' '/fh28'}
%Ss = {'/fh14'} % Redo 14

for ii=1:size(Ss,2),
    datadir = [DATAPATH Ss{ii}]
    cd(datadir)

    meta_ana(datadir)
    meta_realign(datadir,{'fh0' 'fh1' 'fh2' 'fh3' 'fh4' 'fh5' 'fh6'})
    meta_func(datadir,'fh',1.5,29,[1:2:29 2:2:29],floor(29/2),[3 3 3])
end

exit;
