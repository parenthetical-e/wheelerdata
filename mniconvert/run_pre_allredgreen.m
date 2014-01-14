addpath('~/src/wheelerdata/mniconvert/spm/')

DATAPATH = '/data/data2/meta_accumulate/redgreen/'

Ss = {'/redgreen1' '/redgreen2' '/redgreen5' '/redgreen7' '/redgreen8' '/redgreen9' '/redgreen10' '/redgreen11' '/redgreen12' '/redgreen14' '/redgreen15' '/redgreen16' '/redgreen17' '/redgreen18' '/redgreen19' '/redgreen22' '/redgreen24' '/redgreen25'}

for ii=1:size(Ss,2),
    datadir = [DATAPATH Ss{ii}]
    cd(datadir)

    meta_ana(datadir)
    meta_realign(datadir,{'redgreen0' 'redgreen1' 'redgreen2' 'redgreen3' 'redgreen4' 'redgreen5'})
    meta_func(datadir,'redgreen',2,38,[1:2:38 2:2:38],floor(38/2),[3 3 3])
end

exit;
