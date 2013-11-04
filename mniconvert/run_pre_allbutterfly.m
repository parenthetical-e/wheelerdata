addpath('~/src/wheelerdata/mniconvert/spm/')

DATAPATH = '/data/data2/meta_accumulate/butterfly/'

Ss = {'/butterfly4' '/butterfly5' '/butterfly7' '/butterfly17' '/butterfly18' '/butterfly19' '/butterfly20' '/butterfly21' '/butterfly22' '/butterfly23' '/butterfly25' '/butterfly26' '/butterfly30'}

for ii=1:size(Ss,2),
    datadir = [DATAPATH Ss{ii}]
    cd(datadir)

    meta_ana(datadir)
    meta_realign(datadir,{'butterfly0' 'butterfly1' 'butterfly2' 'butterfly3' 'butterfly4' 'butterfly5'})
    meta_func(datadir,'butterfly',2,35,[1:2:35 2:2:35],floor(35/2),[3 3 3])
end

exit;
