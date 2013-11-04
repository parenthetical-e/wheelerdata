import os
import pandas as pd
from wheelerdata.load.base import Wheelerdata


class Butterfly(Wheelerdata):
    """Butterfly data"""

    def __init__(self):
        super(Butterfly, self).__init__()
        
        self.scodes = [4, 5, 7, 17, 18, 19, 20, 21, 22, 23, 25, 26, 30]
        self.name = "butterfly"
        
        self.datapath = "/data/data2/meta_accumulate/" + self.name
        self.roipath = os.path.join(self.datapath, "roinii")
        self.metapath = os.path.join(self.datapath, "fidl")

