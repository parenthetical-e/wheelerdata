#! /usr/local/bin/python
"""A program that takes a .fidl file from the Ploran 2007 dataset and converts then to a csv file suitable for import and use as attributes in PyMVPA Datasets. 

Usage: metadata_butterfly fidl
"""
import os
import sys
import fidl

# ----
# 1. Get the name of the file to process
if len(sys.argv[1:]) > 1:
    raise ValueError('Too many arguments.')
fidlfile = sys.argv[1]
basename = os.path.splitext(fidlfile)[0]
    ## drop the fidl extension

# ----
# 0. "Globals"
triallen = 8    ## The length (in TR) of each trial
condcol = 2     ## The location in csv_f of the cond names
trialcol = 4    ## The location in csv_f of the trial desginator

# and convert the fidl to csv, 
# and write that csv to disk.
csv_f = basename + ".csv"
fidl.convert.fidl_to_csv(fidlfile, csv_f)

# ----
# 2. Find all trial data, excluding dropped 
# trials and jitter periods, etc.
# Being overly explicit rather than
# relying on fuzzy_label() regex
# as the names are so damn
# inconsistent; Damn that Ploran. :)
triallab = {
    "1BPonepic" : "trial",
    "2BPtwopic" : "trial",
    "3BPpicthr" : "trial",
    "4BPpicfour" : "trial",
    "5BPpicfive" : "trial",
    "6BOpicsix" : "trial",
    "7BPpicsev" : "trial",
    "8BPpicegt" : "trial",
    "11BPwone" : "trial",
    "12BPwtwo" : "trial",
    "13BPwthr" : "trial",
    "14BPwfr" : "trial",
    "15BPwfive" : "trial",
    "16BPwsix" : "trial",
    "17BPwsev" : "trial",
    "18BPwegt" : "trial",
    "21BPpINCone" : "trial",
    "22BPpINCtwo" : "trial",
    "23BPpINCthr" : "trial",
    "24BPpINCfr" : "trial",
    "25BPpINCfv" : "trial",
    "26BPpINCsix" : "trial",
    "27BPpINCsev" : "trial",
    "28BPpINCegt" : "trial",
    "31BPwINCone" : "trial",
    "32BPwINCtwo" : "trial",
    "33BPwINCthr" : "trial",
    "34BPwINCfr" : "trial",
    "35BPwINCfv" : "trial",
    "36BPwINCsix" : "trial",
    "37BPwINCsev" : "trial",
    "38BPwINCegt" : "trial"}

fidl.convert.fuzzy_label(csv_f, condcol, triallab, "trial", header=True)

# ----
# 3. Add new labels for accuracy
acclab = {
    "BPonepic" : "1",  ## A exact few edge cases
    "BPtwopic" : "1",
    "BOpicsix" : "1",
    "BPpic" : "1",     ## The general pic/correct regex
    "BPwo" : "1",      ## The non-INC "word" labels
    "BPwt" : "1", 
    "BPwf" : "1",
    "BPws" : "1",
    "BPwe" : "1",
    "INC" : "0"}        ## All incorrect are INC
fidl.convert.fuzzy_label(csv_f, condcol, acclab, "acc", header=True)

# ----
# 4. Add labels mapping the rt (recognition times) to one of
# tw0 classes, fast or slow
# Do a comple variations 1/2, extremes, based on the paper curves, etc
rtlab = {
    "one" : "1",
    "two" : "2",
    "thr" : "3",
    "four" : "4",   ## There are two fours...
    "fr" : "4",  
    "five" : "5",   ## And fives.... sigh.
    "fv" : "5",
    "six" : "6",
    "sev" : "7",
    "egt" : "8"}
fidl.convert.fuzzy_label(csv_f, condcol, rtlab, "rt", header=True)

# ----
# 5. Add labels for word versus pic
explab = {
    "BPonepic" : "pic",  ## Edge cases for "pic"
    "BPtwopic" : "pic",
    "BOpicsix" : "pic",
    "BPp" : "pic",       ## General "pic" match
    "BPw" : "word"}      ## General "word" match
fidl.convert.fuzzy_label(csv_f, condcol, explab, "exp", header=True)

# ----
# 6. Add Subject code
sublab = {"trial" : basename}
fidl.convert.fuzzy_label(csv_f, trialcol, sublab, "scode", header=True)

# ----
# N. Expand labels so they cover every TR
final_ncol = 8
tdur  = {'trial' : triallen}
fidl.convert.tr_time(csv_f, trialcol, tdur, drop=True, header=True)
fidl.convert.fill_tr_gaps('trtime_' + csv_f, final_ncol)
    ## As trial labels were added first, following
    ## csv conversion, the trial label lives in col 3

