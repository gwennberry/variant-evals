import sys
import os
import csv

# Parse arguments
path = sys.argv[1]
outpath = sys.argv[2]
tags = sys.argv[3]
append = sys.argv[4] == "1"
splittags = tags.split(",")

# Define functions
def VariantType(ref,alt):
    if len(ref) > 1 and len(alt) > 1:
        return "MNV"
    if len(ref) > len(alt):
        return "Deletion"
    if len(ref) < len(alt):
        return "Insertion"
    if len(ref) == 1:
        return "SNV"

# Read the VCF file
lineCount = 0
formatDict = {}

lines = open(path, 'r').readlines()

datarows = []
for line in lines:
    if line.startswith("#"):
        continue

    splitline = line.strip().split("\t")
    if len(splitline) == 1:
        splitline = line.strip().split(",")
    chr = splitline[0]
    coord = splitline[1]
    ref = splitline[3]
    alt = splitline[4]
    filters = splitline[6]
    dp = int(splitline[7].split('=')[1])  # Assumes we only have DP, no annotation or anything

    if alt == ".":
        continue

    format = splitline[8]
    formatValues = splitline[9].split(":")

    if lineCount == 0:
        splitFormat = format.split(":")
        for i in range(len(splitFormat)):
            formatDict[splitFormat[i]] = i

    vf = float(formatValues[formatDict["VF"]])

    gt_guess = ""
    if vf > .8:
        gt_guess = "HomAlt"
    elif .4 < vf < .6:
        gt_guess = "HetAlt"
    elif vf < .2:
        gt_guess = "Somatic"

    #Write the output
    lineCount += 1

    row = []
    for tag in splittags:
        row.append(tag)
    reg_row = [chr,coord,ref,alt,VariantType(ref,alt),filters,dp,vf,gt_guess]
    for item in reg_row:
        row.append(item)
    datarows.append(row)



print lineCount
print formatDict

if append:
    writeType = 'a'
else:
    writeType = 'wb'
with open(outpath, writeType) as csvfile:
    csvwriter = csv.writer(csvfile)

    header = []

    for i in range(len(splittags)):
        header.append("tag"+str(i))
    reg_header = ["chr","coord","ref","alt","type","filters","dp","vf","gt_guess"]
    for head in reg_header:
        header.append(head)
    if not append:
        csvwriter.writerow(header)
    for row in datarows:
        csvwriter.writerow(row)