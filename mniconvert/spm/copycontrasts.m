% Find all the con_ in each Ss datadir, add ss{ii}
% as a prefix (copy) and move copy to contrasts
% Repeat for motor, rt and noise sets.

addpath('~/src/metaaccumulate/mniconvert/spm/')

basedatadir = '/data/data2/meta_accumulate/fh';

ss = {'fh09' 'fh11' 'fh13' 'fh14' 'fh15' 'fh17' 'fh19' 'fh21' 'fh23'...
        'fh24' 'fh25' 'fh26' 'fh27' 'fh28'};

[stat, mess] = mkdir(fullfile(basedatadir,'contrasts'));
for ii=1:size(ss,2),
    % -----
    % MOTOR
    disp(ss{ii});
    motordir = [ss{ii} '_motor_fir'];
    motordir = fullfile(basedatadir,ss{ii},motordir);
     
    olddir = pwd
    cd(fullfile(basedatadir,'contrasts'))
    [stat, mess] = mkdir('motor_fir')

    % Get the names of the new contrasts
    % and use them to rename using a ss{ii}
    % prefix.
    cons = dir(fullfile(motordir,'con_00*'))
    for jj=1:size(cons,1),
        conname = cons(jj).name
        newconname = [ss{ii} '_' conname]
        
        % Append s{ii} to the contrast names
        % in a copy, then move the renamed to
        % basedatadir/contrast/XX_motor/
        copyfile(fullfile(motordir,conname),...
                fullfile(motordir,newconname))
        movefile(fullfile(motordir,newconname),'motor_fir')
    end
    cd(olddir);

    % -----
    % NOISE
    noisedir = [ss{ii} '_noise_fir'];
    noisedir = fullfile(basedatadir,ss{ii},noisedir);
    
    olddir = pwd
    cd(fullfile(basedatadir,'contrasts'))
    [stat, mess] = mkdir('noise_fir')

    cons = dir(fullfile(noisedir,'con_00*'))
    for jj=1:size(cons,1),
        conname = cons(jj).name
        newconname = [ss{ii} '_' conname]
        
        % Append s{ii} to the contrast names
        % in a copy, then move the renamed to
        % basedatadir/contrast/XX_noise/
        copyfile(fullfile(noisedir,conname),...
                fullfile(noisedir,newconname))
        movefile(fullfile(noisedir,newconname),'noise_fir')
    end
    cd(olddir);

    % --
    % RT
    rtdir = [ss{ii} '_rt_fir'];
    rtdir = fullfile(basedatadir,ss{ii},rtdir);
     
    olddir = pwd
    cd(fullfile(basedatadir,'contrasts'))
    [stat, mess] = mkdir('rt_fir')

    cons = dir(fullfile(rtdir,'con_00*'))
    for jj=1:size(cons,1),
        conname = cons(jj).name
        newconname = [ss{ii} '_' conname]
        
        % Append s{ii} to the contrast names
        % in a copy, then move the renamed to
        % basedatadir/contrast/XX_rt/
        copyfile(fullfile(rtdir,conname),...
                fullfile(rtdir,newconname))
        movefile(fullfile(rtdir,newconname),'rt_fir')
    end
    cd(olddir);

    % -----
    % FACEHOUSE
    disp(ss{ii});
    fhdir = [ss{ii} '_stim_facehouse'];
    fhdir = fullfile(basedatadir,ss{ii},fhdir);
     
    olddir = pwd
    cd(fullfile(basedatadir,'contrasts'))
    [stat, mess] = mkdir('stim_facehouse')

    % Get the names of the new contrasts
    % and use them to rename using a ss{ii}
    % prefix.
    cons = dir(fullfile(fhdir,'con_00*'))
    for jj=1:size(cons,1),
        conname = cons(jj).name
        newconname = [ss{ii} '_' conname]
        
        % Append s{ii} to the contrast names
        % in a copy, then move the renamed to
        % basedatadir/contrast/XX_motor/
        copyfile(fullfile(fhdir,conname),...
                fullfile(fhdir,newconname))
        movefile(fullfile(fhdir,newconname),'stim_facehouse')
    end
    cd(olddir);

    % -----
    % FACEHOUSE FIR
    disp(ss{ii});
    fhdirfir = [ss{ii} '_stim_facehouse_fir'];
    fhdirfir = fullfile(basedatadir,ss{ii},fhdirfir);
     
    olddir = pwd
    cd(fullfile(basedatadir,'contrasts'))
    [stat, mess] = mkdir('stim_facehouse_fir')

    % Get the names of the new contrasts
    % and use them to rename using a ss{ii}
    % prefix.
    cons = dir(fullfile(fhdirfir,'con_00*'))
    for jj=1:size(cons,1),
        conname = cons(jj).name
        newconname = [ss{ii} '_' conname]
        
        % Append s{ii} to the contrast names
        % in a copy, then move the renamed to
        % basedatadir/contrast/XX_motor/
        copyfile(fullfile(fhdirfir,conname),...
                fullfile(fhdirfir,newconname))
        movefile(fullfile(fhdirfir,newconname),'stim_facehouse_fir')
    end
    cd(olddir);
end

