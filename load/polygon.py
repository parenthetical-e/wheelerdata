import os
import pandas as pd
from wheelerdata.load.base import Wheelerdata


class Polygon(Wheelerdata):
    """Polygon data"""

    def __init__(self):
        super(Polygon, self).__init__()
        
        self.scodes = [1, 2, 3, 5, 6, 8, 9, 11, 12, 19, 20, 
                21, 22, 24, 25, 26, 27, 28, 29]
                # I have no subjective weight (sw) metadata for 7
                # so they were dropped.
        self.name = "polygon"
        
        self.datapath = "/data/data2/meta_accumulate/" + self.name
        self.roipath = os.path.join(self.datapath, "roinii")
        self.metapath = os.path.join(self.datapath, "fidl")

