import csv
import glob
import os
import re

import numpy as np
import pandas as pd

basepath = "C:\\Users\\Mari\\Documents\\Uni\Master\\SoSe19\\praat skript\\pitchlists"
tablepath = '~/tables/dict.csv'
filespath = "\\*.txt"

tbl_raw_data = pd.read_csv(tablepath)
print(tbl_raw_data)

txtFiles = glob.glob(basepath+filespath)
txtCount = len(txtFiles)
# print("There are "+str(txtCount)+" files.")


# extracts the name of the file from the given path
# @param: path as string
def extract_name(path):
    head, tail = os.path.split(path)
    name = re.sub('.txt$', '', tail)
    return name


# converts string value into float
# @param: value as string
def pitch_value_float(strvalue):
    #define the return value as float
    flVal = 0.0

    # if there is 'Hz' in strvalue, it contains the frequency value
    if "Hz" in str(strvalue):
        # remove ' Hz' from value
        strVal = strvalue.rpartition(" ")[0]
        flVal = round(float(strVal),2)
    return flVal



def create_pitch_dict(txtFiles):
    pitchDict = {}
    for txtFile in txtFiles:

        pitchValues = []
        lines = open(txtFile, "r").readlines()
        fileName = extract_name(txtFile)

        for line in lines:
            pitchValue = pitch_value_float(line)
            if pitchValue > 0.0:
                pitchValues.append(pitchValue)

        print(fileName + ": ")

        pitchValues.sort()
        print(pitchValues)
        pmed = st.median_low(pitchValues)
        pmedlow = st.median_low(pitchValues)
        np_med = np.median(pitchValues)
        pmean = round(st.mean(pitchValues), 3)
        pstdev = round(st.stdev(pitchValues), 3)
        print("mean: " + str(pmean))
        print("median: " + str(pmed))
        print("median low: " + str(pmedlow))
        print("stdev: " + str(pstdev))
        #pitchDict[fileName] = pmed
        pitchDict.update({fileName: pmed})

    df_pitch = pd.DataFrame(pitchDict)
    print("df: ")
    print(df_pitch)

    return pitchDict


def dict_to_cvs(dict):
    with open('dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dict.items():
            writer.writerow([key, value])



pitchTable = create_pitch_dict(txtFiles)
#sorted_pitchTable = OrderedDict( sorted(pitchTable.items(), key=lambda x: x[1]))
sorted_pitchTable = sorted(pitchTable.items(), key=lambda x: x[1])

#https://jakevdp.github.io/PythonDataScienceHandbook/05.13-kernel-density-estimation.html
#hist = plt.hist(sorted_pitchTable, bins=30, normed=True)

print(sorted_pitchTable)
dict_to_cvs(pitchTable)


