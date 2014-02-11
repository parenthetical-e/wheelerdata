from wheelerdata.load.butterfly import Butterfly
from wheelerdata.load.clock import Clock
from wheelerdata.load.fh import FH
from wheelerdata.load.polygon import Polygon
from wheelerdata.load.redgreen import Redgreen
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
