addpath('~/src/wheelerdata/mniconvert/spm/')

DATAPATH = '/data/data2/meta_accumulate/polygon/'

Ss = {'/polygon1' '/polygon2' '/polygon3' '/polygon5' '/polygon6' '/polygon7' '/polygon8' '/polygon9' '/polygon11' '/polygon12' '/polygon19' '/polygon20' '/polygon21' '/polygon22' '/polygon24' '/polygon25' '/polygon26' '/polygon27' '/polygon28' '/polygon29'}

for ii=1:size(Ss,2),
    datadir = [DATAPATH Ss{ii}]
    cd(datadir)

    meta_ana(datadir)
    meta_realign(datadir,{'polygon0' 'polygon1' 'polygon2' 'polygon3' 'polygon4' 'polygon5'})
    meta_func(datadir,'polygon',2,38,[1:2:38 2:2:38],floor(38/2),[3 3 3])
end

exit;
