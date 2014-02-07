addpath('~/src/wheelerdata/mniconvert/spm/')

DATAPATH = '/data/data2/meta_accumulate/biasbox/'
Ss = {'/biasbox8' '/biasbox10' '/biasbox11' '/biasbox13' '/biasbox15' '/biasbox16' '/biasbox17' '/biasbox18' '/biasbox19' '/biasbox20' '/biasbox21' '/biasbox22' '/biasbox23' '/biasbox24' '/biasbox26' '/biasbox27' '/biasbox29' '/biasbox30' '/biasbox31'}

for ii=1:size(Ss,2),
    datadir = [DATAPATH Ss{ii}]
    cd(datadir)

    meta_ana(datadir)
    meta_realign(datadir,{'biasbox0' 'biasbox1' 'biasbox2' 'biasbox3' 'biasbox4'})
    meta_func(datadir,'biasbox',1.5,29,[1:2:29 2:2:29],floor(29/2),[3 3 3])
end

exit;
