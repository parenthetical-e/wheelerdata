#! /usr/local/bin/python
"""A program that takes a .fidl file from a Wheeler lab dataset and converts 
then to a csv file suitable for import and use as labels in a
sklearn classfication experiemnt, and also produces a .mat file suitable
for use in SPM.

Usage: metadata fidl name filterfile
"""
import os
import sys
from json import load
import pandas as pd
import numpy as np
from fidl.convert import fidl_to_csv
from fidl.convert import fuzzy_label
from fidl.convert import tr_time
from fidl.convert import fill_tr_gaps
from fidl.convert import nod_mat


def _get_name(fd):
    return fd.keys()[0]

def _get_filt(fd):
    return fd.values()[0]    


def create(name, fidl, filterf, nod=True):
    """Use a fild file to create a metadata label table, using the json
    filter file to convert, rename, and reorganize labels as needed.

    Parameters
    ----------
    name : str
        The name of the csv file (inculde extension)
    fidl : str
        The name of the .fidl file
    filterf : str
        The name of the filer json file (see Note for format details)
    nod : Boolean
        Write SPM compatile NOD (Names, Onsets, Durations) .mat files

    Notes
    -----
    Overall filterf has two goals. 1. Configure create() for the 
    current exp.  2. Remap/join labels/conditions from the fidl file
    before using them in the csv.  Fidl names are often rather
    confusing and noisy.

    The filterf should be valid json file, where the top level
    is a list.  The first element in that list must be the exp parameters
    in a dict.  The next and remaining elements are dicts whose keys 
    will become a colname in the csv.  The values are the 
    fuzzy_label : label pairs.

    Nothing is done to validate the filterf.  Use with care and
    double check the results.

    For example (delete comments (#) before use/validation):
        
        [
        # The parameters
            {
                "triallen" : 5, 
                "condcol" : 2,
                "trialcol" : 4,
                "final_ncol" : 8
            },
            {
        # The first filteration, col with be trial
        # and each fidl match on the right gets 
        # coded as 'trial'
                "trial": {
                    "1FaceCor1" : "trial",
                    "2FaceCor2" :  "trial",
                    "3FaceCor3" :  "trial",
                    "4FaceCor4" : "trial",
                    "5FaceCor5" : "trial",
                    "6HouseCor1" : "trial",
                    "7HouseCor2" : "trial",
                    "8HouseCor3" :  "trial",
                    "9HouseCor4" :  "trial",
                    "10HouseCor5" :  "trial",
                    "11NoiseResp1" : "trial",
                    "12NoiseResp2" : "trial",
                    "13NoiseResp3" : "trial",
                    "14NoiseResp4" : "trial",
                    "15NoiseResp5" : "trial",
                    "16NoiseResp5" : "trial",
                    "16MultiResp" :  "trial",
                    "17NoResp" : "trial"
                }
            },
            }
        # Col is rt, and both Cor1 and Resp1
        # get remapped to rt1 (and repeat for 2, 3 ...)
                "rt": {
                    "Cor1" : "rt1",
                    "Cor2" : "rt2",
                    "Cor3" : "rt3",
                    "Cor4" : "rt4",
                    "Resp1" : "rt1",
                    "Resp2" : "rt2",
                    "Resp3" : "rt3",
                    "Resp4" : "rt4"
                }    
            },
            {
        # And so on....
                "exp": {
                    "Face" : "face",
                    "House" : "house",
                    "Noise" : "noise"
                }
            }
        ]
    """

    fidl_to_csv(fidlfile, name, 0)
        ## Write a csv to disk

    filterdata = load(open(filterf, 'r'))
    expdata = filterdata.pop(0)
    condcol = expdata["condcol"]
    trialcol = expdata["trialcol"]
    triallen = expdata["triallen"]

    for fd in filterdata:
        fuzzy_label(
                name, condcol, _get_filt(fd), _get_name(fd), header=True)

    # Add the name of the fidl file as a factor
    dname = os.path.splitext(os.path.basename(fidl))[0]
    if len(dname) < 3:
        dname += "__"

    sublab = {"trial" : dname}
    fuzzy_label(name, trialcol, sublab, "scode", header=True)

    # Fill in TR time
    tdur  = {"trial" : triallen} 
    tr_time(name, trialcol, tdur, drop=True, header=True)
    ncol = expdata["final_ncol"]
    fill_tr_gaps(os.path.join(
            os.path.dirname(name), 
            "trtime_"+os.path.basename(name)), ncol, fill='nan')
    
    # Be SPM compatible?
    if nod:
        csvdata = pd.read_csv(name)
        names = csvdata["rt"]
        trials = csvdata["trial"]
        onsets = csvdata["TR"]

        durations = np.array([triallen, ] * len(trials))
        nod_mat(names, onsets, durations,
                os.path.join(
                    os.path.dirname(name),  
                    "nod_"+os.path.splitext(
                        os.path.basename(name))[0]+".mat"))


if __name__ == '__main__':
    if len(sys.argv[1:]) != 3:
        raise ValueError("Three arguemnts required.")

    fidlfile = sys.argv[1]
    name = sys.argv[2]
    filterfile = sys.argv[3]

    # print(open(fidlfile, 'r').readline())
    create(name, fidlfile, filterfile, True)

