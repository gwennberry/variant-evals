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

print "Running CSV Scatter"

if os.path.exists(path):
    df = pd.read_csv(path, low_memory=False, header=0)
    print df.describe()

    # See which headers are available
    cols = (list(df))
    print cols

    another = True

    while another:
        col = raw_input("Choose one or more (comma separated) of the available headers to group by:\n")

        interest_cols = col.split(',')
        print "You chose",interest_cols

        col_values = raw_input("Choose one of the available headers to draw a scatter plot:\n")
        grouped = df.groupby(interest_cols)[col_values]

        df.plot(kind='scatter', x=interest_cols[0], y=col_values)
        break

        # Make the histograms
        print "Making histogram"
        rows = 3
        rowlength = grouped.ngroups/rows

        if grouped.ngroups%rows!=0:
            rows +=1
        fig, axs = plt.subplots(figsize=(9,4),
                        nrows=rows, ncols=rowlength,
                        gridspec_kw=dict(hspace=0.4))

        sorted_keys = sorted(grouped.groups.keys(), key=lambda tup: (tup[0], tup[1]))
        targets = zip(sorted_keys, axs.flatten())

        for i, (key, ax) in enumerate(targets):
            grouped.get_group(key).hist(label=key, alpha=.25, ax=ax, bins=50)
            ax.set_title(key)
        plt.show()


        makeAnother = raw_input("Another?")
        if makeAnother == "y":
            print "OK"
        else:
            break

else:
    print "Path does not exist: ",path
plt.show()

