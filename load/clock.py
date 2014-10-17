import os
from wheelerdata.load.base import Wheelerdata


class Clock(Wheelerdata):
    """Clock data"""

    def __init__(self):
        super(Clock, self).__init__()

        self.scodes = [4, 5, 7, 8, 9, 10, 11, 13, 14, 15,
                       17, 18, 19, 20, 21]
        # Removed 16, was having indeterminate issues
        # using masks from that dataset - they were
        # all coming up empty.
        self.name = "clock"

        self.datapath = "/data/data2/meta_accumulate/" + self.name
        self.roipath = os.path.join(self.datapath, "roinii")
        self.metapath = os.path.join(self.datapath, "fidl")
        self.TR = 2.0

