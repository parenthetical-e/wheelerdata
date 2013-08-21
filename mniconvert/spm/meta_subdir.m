function [dir_name] = cr_subdir(num),
% Return the name of the fMRI data directory given the subject number, <num>.
%
% [dir_name] = cr_subdir(num),

	switch num
	case 09
		dir_name = 'fh09';
    case 11
		dir_name = 'fh11';
	case 13
		dir_name = 'fh13';
	case 14
		dir_name = 'fh14';
	case 15
		dir_name = 'fh15';
	case 17
		dir_name = 'fh17';
	case 19
		dir_name = 'fh19';
	case 21
		dir_name = 'fh21';
	case 23
		dir_name = 'fh23';
	case 24
		dir_name = 'fh24';
	case 25
		dir_name = 'fh25';
	case 26
		dir_name = 'fh26';
	case 27
		dir_name = 'fh27';
	case 28
		dir_name = 'fh28';
    otherwise
        error('Invalid <num> code.');
	end
end
