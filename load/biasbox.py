import os
import pandas as pd
from wheelerdata.load.base import Wheelerdata


class Biasbox(Wheelerdata):
    """Face/House data using a probablistic bias cue."""

    def __init__(self):
        super(Biasbox, self).__init__()
        
        self.scodes = [8, 10, 11, 13, 15, 16, 17, 18, 19, 
                20, 21, 22, 23, 24, 26, 27, 29, 30, 31]
        self.name = "biasbox"
        
        self.datapath = "/data/data2/meta_accumulate/" + self.name
        self.roipath = os.path.join(self.datapath, "roinii")
        self.metapath = os.path.join(self.datapath, "fidl")

