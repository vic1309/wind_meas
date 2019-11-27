"""
This is the file for the sonic data.
"""

__author__ = "Astrid Myren, UiB"
__email__ = "astrid.myren@student.uib.no"

# Import pandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load csv
df = pd.read_csv("Sonic_processed_2019_11_04.csv", low_memory=False)
#print(df)

# Output the number of rows
print("Total rows: {0}".format(len(df)))

# See which headers are available
print(list(df))
df.head(4)

pd.isnull(df).sum()
# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show(