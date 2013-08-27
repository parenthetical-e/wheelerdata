# L1/L2

## Face/house

The general workflow is
        
        cd /data/data2/metaaccumulate/fh

        run_L1_fir_allfh_stim_facehouse
        run_contrast_stim_facehouse_fhall        
        copycontrasts

### Slow/Event
For L2, intial run using a HRF estimate that spanned 5 TRs/trial showed no face or house ROIs (face-house and the reverse), nor were face-baseline or house-baseline significant at FWE 0.05.  

The desgin was then modified to a fast-event design coding.  Trials were modeled a single impluse ar the start (still using double gamma).  This to showed essentially no significant clusters too.  Odd.  

Next movement correction was removed, in case this was the problem.  I am not sure if movement was regressed out prior to war[...].nii files getting written.  If this were the case a second movement regression would be devistating.

