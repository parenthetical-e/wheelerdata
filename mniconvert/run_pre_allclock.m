addpath('~/src/wheelerdata/mniconvert/spm/')

DATAPATH = '/data/data2/meta_accumulate/clock/'

Ss = {'/clock4' '/clock5' '/clock7' '/clock8' '/clock9' '/clock10' '/clock11' '/clock13' '/clock14' '/clock15' '/clock16' '/clock17' '/clock18' '/clock19' '/clock20' '/clock21'}

for ii=1:size(Ss,2),
    datadir = [DATAPATH Ss{ii}]
    cd(datadir)

    meta_ana(datadir)
    meta_realign(datadir,{'clock0' 'clock1' 'clock2' 'clock3'})
    meta_func(datadir,'clock',2,38,[1:2:38 2:2:38],floor(38/2),[3 3 3])
end

exit;
