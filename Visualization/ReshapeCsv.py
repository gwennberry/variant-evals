import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
import os.path
import pandas as pd
import sys
# Parse arguments
path = sys.argv[1]
outpath = path + "_Reshaped.csv"

if os.path.exists(path):
    df = pd.read_csv(path, low_memory=False, header=0)
    print df.describe()

    print

    cols = (list(df))
    print cols

    rows = []
    col = raw_input("Choose one or more (comma separated) of the available headers to keep :\n")

    indexcols = col.split(',')
    print "You chose",indexcols
    for f in df.keys():
        for i in range(len(df[f])):
            row = []
            for index in indexcols:
                row.append(df[index][i])
            row.append(f)
            row.append(df[f][i])
            rows.append(row)

    with open(outpath, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)

        header = []

        for head in indexcols:
            header.append(head)
        header.append("category")
        header.append("value")
        csvwriter.writerow(header)

        for row in rows:
            csvwriter.writerow(row)

    sys.exit()

