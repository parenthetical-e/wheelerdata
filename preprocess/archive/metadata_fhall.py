# For some (idiotic) reason insted of importing and using the 
# functions defined in metadata_fh_* I called them 
# via Popen i.e. the cammand line.  Dumb and slow, but it works
# so I'm just moving on. Don't code while drunk kids!
import sys, os, re
from subprocess import Popen, PIPE


subnums = [9, 11, 13, 14, 15, 17, 19, 21, 23, 24, 25, 26, 27, 28]
basecmd = "python ~/src/metaaccumulate/bin/preprocess/"
print("base command is {0}".format(basecmd))

for s in subnums:
    # Create meta and dirs names for subjects/subnums
    if s < 10:
        smetacode = "fh00" + str(s)
        sdir = "fh0" + str(s)
    else:
        smetacode = "fh0" + str(s)
        sdir = "fh" + str(s)
    
    # Move into the Ss dir, gen the csv and mat files
    # then move back to the original dir
    initialdir = os.getcwd()
    os.chdir(os.path.join(sdir, "fidl"))
    print("Moving into {0}, using metaname {1}.".format(sdir, smetacode))

    # do the three calls
    calls = [basecmd + "metadata_fh_rt.py {0}_RT_corr_EF.fidl".format(smetacode), ]
    calls.append(basecmd + "metadata_fh_noise.py {0}_noise_corr_EF.fidl".format(smetacode))
    calls.append(basecmd + "/metadata_fh_motor.py {0}_motor_EF.fidl".format(smetacode))
    
    for call in calls:
        p = Popen(call, 
                shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)

        print(p.communicate())
    
    os.chdir(initialdir)

