import os
import pandas as pd


class Wheelerdata(object):
    """A skeleton class for Wheelerdata.  

    Usage 
    -----
    To use subclass then hardcode the following attrs inside the top-level __init__() call,

            self.scodes = None
            self.name = None
            self.datapath = None
            self.roipath = None
            self.metapath = None

    An example using the facehouse data, see `wheelerdata.load.fh`:

        class FH(Wheelerdata):
            def __init__(self):
                super(FH, self).__init__()
                
                self.scodes = [9, 11, 13, 14, 15, 17, 19, 
                        21, 23, 24, 25, 26, 27, 28]
                self.name = 'fh'
                self.datapath = "/data/data2/meta_accumulate/" + self.name
                self.roipath = os.path.join(DATAPATH, "roinii")
                self.metapath = os.path.join(DATAPATH, "fidl")
    Note
    ----
    When posssible the get_* methods check for file existence before 
    returning.  Just becuase a file exists doesn't mean it's valid, 
    complete, or correct.
    """

    def __init__(self):
        super(Wheelerdata, self).__init__()

        self.scodes = None
        self.name = None
        self.datapath = None
        self.roipath = None
        self.metapath = None


    def _exists(self, files):
        for fi in files:
            if not os.path.exists(fi):
                raise IOError("{0} doesn't exist.".format(fi))


    def get_subject_dirs(self):
        return [self.name + str(scode) for scode in self.scodes]


    def get_subject_paths(self):
        spaths = [os.path.join(self.datapath, sdir) for 
                sdir in self.get_subject_dirs()]
        self._exists(spaths)

        return spaths


    def get_roi_data_paths(self, roi):
        dpaths = [os.path.join(
                self.roipath, roi + "_{0}.nii.gz".format(scode)) for 
                scode in self.scodes]
        self._exists(dpaths)

        return dpaths


    def get_RT_NOD_paths(self):
        nodpaths = [os.path.join(
                self.metapath, "nod_{1}{0}_rt.mat".format(
                scode, self.name)) for scode in self.scodes]
        self._exists(nodpaths)

        return nodpaths


    def get_RT_metadata_paths(self):
        mpaths = [os.path.join(
                self.metapath, "trtime_{1}{0}_rt.csv".format(
                scode, self.name)) for scode in self.scodes]
        self._exists(mpaths)

        return mpaths


