[names] = function findcontrasts(dirname, prefix),
% Find all unique contrasts that bagin with prefix,
% for example there are two Ss fh01 and fh11, and two
% contrasts for each fh09_con_0001, fh09_con_0002,
% fh11_con_0001, fh11_con_0002, this will return a 
% struct whose first level name is the contrast number
% and whose value is a cell array of all the file names
% that match it.

    constring = [prefix 'con_0*'];
    confiles = dir(fullfile(dirname,constring);
    unique
    for ii=1:size(confiles,1),
        
    end
end
