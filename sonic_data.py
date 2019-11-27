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
print(df.head(4))

pd.isnull(df).sum()

df.plot(x='time (seconds since 1970-01-01 00:00:00)', y='Y Wind Speed (m/s)', kind='line')
# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show(