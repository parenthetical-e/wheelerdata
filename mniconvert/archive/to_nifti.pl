#! /usr/bin/perl
# Convert select 4dfp data in bold* and atlas directories to
# nifti format.  For what select means in this case see finddata().

# For testing:
# chdir("/Users/type/Code/mniconvert/test/") or die $!;
# print `pwd`;

# Find just the right data to convert
sub finddata {
	my @data;
	for(@_) {
		# Normalized BOLD matches the below
		if(/faln_dbnd_xr3d_MNI152_3mm.4dfp.ifh/){
			print "\tBold: $_\n"; ## return
			push(@data, $_);
		}
		# Anatomical data matches the below
		elsif(/mpr_n1_\d\d\d_t88.4dfp.ifh/){
			print "\tAna: $_\n"; ## return
			push(@data, $_)
		}
	}
	@data;
}

# List all the files in the pwd
$dir_list = `ls -1`;
@dirs = split(/\n/,$dir_list);
chomp(@dirs);

# Remember the current path for later
$pwd = `pwd`;
chomp($pwd);
print "[".$pwd."]\n";

# Loop over all subdirs looking for
# bold and atlas directories
for(@dirs) {
	if(/^bold/ || /^atlas/) {
		# Show the user the matched dir,
		# then step into that dir and convert
		# the appropriate files based finddata()
		print "Processing files in $_\n";
		
		# Create a array of all the files in
		# $_
		$path = $pwd.'/'.$_;
		$file_list = `ls -1 $path`;
		@files = split(/\n/, $file_list);
		
		# Find the data...
		@data = 0;
		@data = finddata(@files);
		
		# and convert it.
		for(@data) {
			print "\tConverting $_ to nifti\n";
			@parts = split(/\./, $_);
		    pop @parts; 
				## Drop the end, the ifh portion,
			$rootname = join '.', @parts; 
				## and rejoin the rest
			$filepath = $path."/".$rootname;
			`nifti_4dfp -n $filepath $filepath`;	
		}
	}
}

print "Success.\n";
