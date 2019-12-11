"""
This is the file for the sonic data.
"""

__author__ = "Astrid Myren, UiB"
__email__ = "astrid.myren@student.uib.no"

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy as np


def simple_wind_from_vector(u, v):
    """
    Transformation from cartesian coordinates to coodinates

    Parameters
    ----------
    u : float
        single value of longitudinal wind component

    v : float
        single component of latitudinal wind component

    Results
    -------
    u_h : float
        single value horizontal wind speed
    wd : float
        single value horizontal wind direction
    """
    # Get the wind direction
    wd = 180 / np.pi * np.arctan(u / v)

    if u >= 0 and v >= 0:
        wd = wd + 180
    elif u <= 0 and v >= 0:
        wd = wd + 180
    elif u >= 0 and v <= 0:
        wd = wd + 360
    else:
        wd = wd

    # Make sure no wind direction value exeeds 360 or falls below 0
    if wd >= 360:
        wd = wd - 360
    elif wd < 0:
        wd = wd + 360

    return wd


# Load csv
df = pd.read_csv("Sonic_processed_2019_11_06.csv", na_filter=False, low_memory=False)
df['datetime'] = pd.to_datetime(df["time (seconds since 1970-01-01 00:00:00)"], unit='s', origin='unix')
df = df.set_index('datetime')
df = df.drop(columns=["time (seconds since 1970-01-01 00:00:00)"])

#Resample
df = df.resample('T').mean()

# Get horizontal wind speed and wind direction
df['Horizontal wind speed'] = df.apply(lambda row: np.sqrt(row['X Wind Speed (m/s)']**2+row['Y Wind Speed (m/s)']**2), axis=1)
df['Wind direction'] = df.apply(lambda row: simple_wind_from_vector(row['X Wind Speed (m/s)'], row['Y Wind Speed (m/s)']), axis=1)

# print(df)
# Output the number of rows
# print("Total rows: {0}".format(len(df)))
# See which headers are available
# print(list(df))
print(df.head())
# print(pd.isnull(df).sum())

cols = ['Horizontal wind speed', 'Wind direction']
axes = df[cols].plot(subplots=True, figsize=(11,9))
for ax in axes:
    ax.set_ylabel('Wind speed (m/s)')
plt.show()