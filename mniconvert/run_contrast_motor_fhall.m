addpath('~/src/metaaccumulate/mniconvert/spm/')

DATAPATH = '/data/data2/meta_accumulate/fh';

Ss = {'fh09' 'fh11' 'fh13' 'fh14' 'fh15' 'fh17' 'fh19' 'fh21' 'fh23' 'fh24' 'fh25' 'fh26' 'fh27' 'fh28'}
%Ss = {'fh09' 'fh11'}

NODS = {'fh009' 'fh011' 'fh013' 'fh014' 'fh015' 'fh017' 'fh019' 'fh021' 'fh023' 'fh024' 'fh025' 'fh026' 'fh027' 'fh028'}
%NODS = {'fh009' 'fh011'}

[stat, meSs] = mkdir(fullfile(DATAPATH,'contrasts'));
for ii=1:size(Ss,2),
    disp(Ss{ii});
    datadir = [Ss{ii} '_motor'];
    datadir = fullfile(DATAPATH,Ss{ii},datadir);
    
    % And run the contrast for this S
    meta_contrast_motor(datadir,1);

    % ----
    % Contrast file reorg...
    olddir = pwd
    cd(fullfile(DATAPATH,'contrasts'))
    [stat, meSs] = mkdir('motor')

    % Get the names of the new contrasts
    % and use them to rename using a Ss{ii}
    % prefix.
    cons = dir(fullfile(datadir,'con_00*'))
    for jj=1:size(cons,1),
        conname = cons(jj).name
        newconname = [Ss{ii} '_' conname]
        
        % Append s{ii} to the contrast names
        % in a copy, then move the renamed to
        % DATAPATH/contrast/XX_motor/
        copyfile(fullfile(datadir,conname),...
                fullfile(datadir,newconname))
        movefile(fullfile(datadir,newconname),'motor')
    end

    cd(olddir);
end

