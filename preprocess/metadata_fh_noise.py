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
    "0fix" : "trial",
    "1Face65" : "trial",
    "2Face66" : "trial",
    "3Face67" : "trial",
    "4Face68" : "trial",
    "5Face69" : "trial",
    "6Face70" : "trial",
    "7NoiseRespFace" : "trial",
    "8NoiseRespHouse" : "trial",
    "10NoResp" : "trial",
    "11House65" : "trial",
    "12House66" : "trial",
    "13House67" : "trial",
    "14House68" : "trial",
    "15House69" : "trial",
    "16House70" : "trial",
    "MultiResp" : "trial"}
fuzzy_label(csv_f, condcol, triallab, "trial", header=True)

# ----
# 4. Add labels for rt independent of stim type
noiselab = {
    "Face65" : "65percent",
    "Face66" : "66percent",
    "Face67" : "67percent",
    "Face68" : "68percent",
    "Face69" : "69percent",
    "Face70" : "70percent",
    "House65" : "65percent",
    "House66" : "66percent",
    "House67" : "67percent",
    "House68" : "68percent",
    "House69" : "69percent",
    "House70" : "70percent"}
fuzzy_label(csv_f, condcol, noiselab, "noise", header=True)

# ----
# 5. Add labels for stim type
explab = {
    "Face65" : "face",
    "Face66" : "face",
    "Face67" : "face",
    "Face68" : "face",
    "Face69" : "face",
    "Face70" : "face",
    "NoiseRespFace" : "face",
    "House65" : "house",
    "House66" : "house",
    "House67" : "house",
    "House68" : "house",
    "House69" : "house",
    "House70" : "house",
    "NoiseRespHouse" : "house"}
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
trials = csvdata["trial"]

names = csvdata["noise"]
onsets = csvdata["TR"]
durations = np.array([triallen, ] * len(trials))

nod_mat(names, onsets, durations, "nod_" + basename + ".mat")

