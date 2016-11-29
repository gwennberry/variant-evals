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


if os.path.exists(path):
    df = pd.read_csv(path, low_memory=False, header=0)
    print df.describe()

    # See which headers are available
    cols = (list(df))
    print cols

    another = True

    # fig, ax = plt.subplots()
    while another:
        col = raw_input("Choose one or more (comma separated) of the available headers to group by for first level:\n")
        interest_cols = col.split(',')
        print "You chose",interest_cols

        col2 = raw_input("Choose one or more (comma separated) of the available headers to compare/group by for second level:\n")
        interest_cols2 = col2.split(',')
        print "You chose",interest_cols2

        while True:
            col_values = raw_input("Choose one of the available headers to draw a histogram:\n")
            grouped = df.groupby(interest_cols)

            col_values_split = col_values.split(',')


            print "Making boxplot"
            count_ax = 0

            #plt.figure()

            ax = grouped.boxplot(subplots=True, by=interest_cols2, showfliers=False, figsize=(15,15), fontsize=7, return_type='axes')
            # ax = grouped.boxplot(subplots=True, column=col_values_split, by=interest_cols2, showfliers=False, figsize=(15,15), fontsize=7, return_type='axes')
            plt.show()

            makeAnotherForGrouping = raw_input("Another plot for" + col + " / " + col2 + "? (y/n)")
            if makeAnotherForGrouping == "y":
                print "OK"
            else:
                break



        makeAnother = raw_input("Another?")
        if makeAnother == "y":
            print "OK"
        else:
            break

plt.show()

