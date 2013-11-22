import os
import pandas as pd
from wheelerdata.load.base import Wheelerdata


class FH(Wheelerdata):
    """Face/House data"""

    def __init__(self):
        super(FH, self).__init__()
        
        self.scodes = [9, 11, 13, 14, 15, 17, 19, 21, 23, 24, 25, 26, 27, 28]
        #self.scodes = [9, 11, 13, 14, 17, 19, 21, 23, 24, 25, 27, 28]
        self.name = "fh"
        
        self.datapath = "/data/data2/meta_accumulate/" + self.name
        self.roipath = os.path.join(self.datapath, "roinii")
        self.metapath = os.path.join(self.datapath, "fidl")

