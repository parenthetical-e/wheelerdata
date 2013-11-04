""" In a nice table, write out various useful statistics on the Ploran 2007 
metadata. """
import csv
from fidl import stats


# ----
# 0. "Globals"
cols = ["acc", "rt", "exp"]
csvfiles = [
    "s17.csv",
    "s18.csv",
    "s19.csv",
    "s20.csv",
    "s21.csv",
    "s22.csv",
    "s23.csv",
    "s25.csv",
    "s30.csv",
    "s4.csv",
    "s5.csv",
    "s7.csv"]

# ----
# 1. Calc the stats for each col in cols
# and write out the results
fid = open('s_stats.txt', "w")
csvout = csv.writer(fid, delimiter="\t")

allstats = {}
for col in cols:
    # Get the group_counts
    gc = stats.group_counts(csvfiles, col)
    
    # And write them....
    # The name of the col, the keys 
    # and the counts and add a newline
    # to sep from the next col's data
    csvout.writerow(['[' + col + ']', ])
    csvout.writerow(gc.keys())
    csvout.writerow(gc.values())
    csvout.writerow([])

# Cleanup
fid.close()
