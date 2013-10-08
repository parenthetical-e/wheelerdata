This code has two parts.  

Part 1 is a python module for finding/loading wheeler lab data, espescially ROI data derived from SPM preprocessing.  To use it try

        # For face/house data
        import wheelerdata.load.fh as fh  

        # For Ploran 2007 data
        import wheelerdata.load.fh as fh

        # And so on for the rest of the data sets

This python module also contains a function for generating (and therefore loading) BOLD *simulations* of accumulator, and related decision-signals.  To use it (there is only one public function).

        from wheelerdata.load.sim import make_bold
        # This function is badly in need of documentation.

Part 2 is a set of .sh and .py scripts that created the data the can be found and loaded with the python module.  To rerun/use these scripts, and to see how they all interact, see the Makefile in.
        
        ./wheelerdata/Makefile
