import os
from wheelerdata.load.base import Wheelerdata


class Butterfly(Wheelerdata):
    """Butterfly data"""

    def __init__(self):
        super(Butterfly, self).__init__()

        self.scodes = [4, 5, 7, 17, 18, 19, 21, 22, 23, 25, 26, 30]
        # self.scodes = [4, 5, 7, 17, 18, 19, 20, 21, 22, 23, 25, 26, 30]
        # S20's data was corrupted in roinii and I don't have
        # access to the orignal nii to recreate it.

        self.name = "butterfly"

        self.datapath = "/data/data2/meta_accumulate/" + self.name
        self.roipath = os.path.join(self.datapath, "roinii")
        self.metapath = os.path.join(self.datapath, "fidl")
        self.TR = 2.0


class SimAccumButterfly(Butterfly):
    """Simulated accumulator Butterfly data"""

    def __init__(self):
        super(SimAccumButterfly, self).__init__()

        self.datapath = "/data/data2/meta_accumulate/" + self.name
        self.roipath = os.path.join(self.datapath, "simnii")
        self.metapath = os.path.join(self.datapath, "fidl")
