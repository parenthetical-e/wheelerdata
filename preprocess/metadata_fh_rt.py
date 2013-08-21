#! /usr/local/bin/python
"""A program that takes a .fidl file from the Face/House dataset and converts then to a csv file suitable for import and use as labels in a
sklearn classfication experiemnt, and also produces a .mat file suitable
for use in SPM.

Usage: metadata_butterfly_rt fidl
"""
import os
import sys
import pandas as pd
import numpy as np
from fidl.convert import (fidl_to_csv, fuzzy_label, tr_time, fill_tr_gaps,
            nod_mat)

# ----
# 1. Get the name of the file to process
if len(sys.argv[1:]) > 1:
    raise ValueError("Too many arguments.")
fidlfile = sys.argv[1]
basename = os.path.splitext(fidlfile)[0]
    ## drop the fidl extension

# ----
# 0. "Globals"
triallen = 5    ## The length (in TR) of each trial
condcol = 2     ## The location in csv_f of the cond names
trialcol = 4    ## The location in csv_f of the trial desginator

# and convert the fidl to csv, 
# and write that csv to disk.
csv_f = basename + ".csv"
fidl_to_csv(fidlfile, csv_f, 0)

# ----
# 2. Separate trials from events we want to ignore
triallab = {
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
        "17NoResp": "trial"}
fuzzy_label(csv_f, condcol, triallab, "trial", header=True)

# ----
# 4. Add labels for rt independent of stim type
rtlab = {
    "Cor1" : "rt1",
    "Cor2" : "rt2",
    "Cor3" : "rt3",
    "Cor4" : "rt4",
    "Resp1" : "rt1",
    "Resp2" : "rt2",
    "Resp3" : "rt3",
    "Resp4" : "rt4"}
        ## Dropping RT5 as it is missing form some 
        ## SS and has low counts overall anyway
fuzzy_label(csv_f, condcol, rtlab, "rt", header=True)

# ----
# 5. Add labels for stim type
explab = {
    "Face" : "face",
    "House" : "house",
    "Noise" : "noise"}
fuzzy_label(csv_f, condcol, explab, "exp", header=True)

# ----
# 6. Add labels for subject/fidl
sublab = {"trial" : basename}
fuzzy_label(csv_f, trialcol, sublab, "scode", header=True)

# ----
# 7. Expand labels so they cover every TR
final_ncol = 8
tdur  = {"trial" : triallen} 
tr_time(csv_f, trialcol, tdur, drop=True, header=True)
fill_tr_gaps("trtime_" + csv_f, final_ncol)
    ## As trial labels were added first, following
    ## csv conversion, the trial label lives in col 3

# ----
# 8. Create the NOD mat file
#
# Get the csv file"s data
# then get onsets, names and 
# create durations 
csvdata = pd.read_csv(csv_f)

names = csvdata["rt"]
trials = csvdata["trial"]

onsets = csvdata["TR"]
durations = np.array([triallen, ] * len(trials))
nod_mat(names, onsets, durations, "nod_" + basename + ".mat")
