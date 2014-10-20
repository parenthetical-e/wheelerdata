from wheelerdata.load.butterfly import Butterfly, SimAccumButterfly
from wheelerdata.load.clock import Clock, SimAccumClock
from wheelerdata.load.fh import FH, SimAccumFH
from wheelerdata.load.polygon import Polygon, SimAccumPolygon
from wheelerdata.load.redgreen import Redgreen, SimAccumRedgreen
from wheelerdata.load.biasbox import Biasbox

def get_data(name):
    """Return the named Wheelerdata object"""

    if name == 'fh':
        data = FH()
    elif name == 'butterfly':
        data = Butterfly()
    elif name == 'clock':
        data = Clock()
    elif name == 'polygon':
        data = Polygon()
    elif name == 'redgreen':
        data = Redgreen()
    elif name == "biasbox":
        data = Biasbox()
    else:
        raise ValueError('Data not understood.  Try fh, butterfly, clock,' 
                ' polygon, or redgreen')

    return data


def get_sim_data(name):
    """Return the named SimAccumWheelerdata object"""

    if name == 'fh':
        data = SimAccumFH()
    elif name == 'butterfly':
        data = SimAccumButterfly()
    elif name == 'clock':
        data = SimAccumClock()
    elif name == 'polygon':
        data = SimAccumPolygon()
    elif name == 'redgreen':
        data = SimAccumRedgreen()
    else:
        raise ValueError('Data not understood.  Try fh, butterfly, clock,' 
                ' polygon, or redgreen')

    return data
