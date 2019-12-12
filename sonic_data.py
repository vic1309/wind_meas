"""
This is the file for the sonic data.
"""

__author__ = "Astrid Myren, UiB"
__email__ = "astrid.myren@student.uib.no"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def load_csv(file):
    dataframe = pd.read_csv(file, na_filter=False, low_memory=False)
    dataframe['datetime'] = pd.to_datetime(dataframe["time (seconds since 1970-01-01 00:00:00)"], unit='s', origin='unix')
    dataframe = dataframe.set_index('datetime')
    dataframe = dataframe.drop(columns=["time (seconds since 1970-01-01 00:00:00)"])
    return dataframe


def resample_df(dataframe):
    # Resample
    dataframe = dataframe.resample('T').mean()
    return dataframe


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


def uh_wd(dataframe):
    # Get horizontal wind speed and wind direction
    dataframe['Horizontal wind speed'] = dataframe.apply(lambda row: np.sqrt(row['X Wind Speed (m/s)']**2+row['Y Wind Speed (m/s)']**2), axis=1)
    dataframe['Wind direction'] = dataframe.apply(lambda row: simple_wind_from_vector(row['X Wind Speed (m/s)'], row['Y Wind Speed (m/s)']), axis=1)
    return dataframe


def plot_wind(dataframe):

    ax = plt.gca()
    dataframe['X Wind Speed (m/s)'].plot(kind='line', ax=ax)
    dataframe['Y Wind Speed (m/s)'].plot(kind='line', ax=ax)
    dataframe['Z Wind Speed (m/s)'].plot(kind='line', ax=ax)
    plt.title('Wind speed from sonic anemometer')
    plt.ylabel('Wind speed [m/s]')
    plt.legend(loc='best')
    # plt.savefig('SA_wind.png')
    plt.show()

    plt.subplots(2, 1, figsize=(15,20)) # 3x3 frame
    plt.subplot(211)
    plt.plot(dataframe['Horizontal wind speed'])
    plt.title('Horizontal wind speed [m/s]')
    plt.ylabel('Wind speed [m/s]')

    plt.subplot(212)
    plt.plot(dataframe['Wind direction'])
    plt.title('Wind direction')
    plt.ylabel('Degrees')
    plt.show()


# cols = ['Horizontal wind speed', 'Wind direction']
# axes = df[cols].plot(subplots=True, figsize=(11,9))
# for ax in axes:
#     ax.set_ylabel('Wind speed (m/s)')
# plt.savefig('SA_uh_wd.png')
# plt.show()

# print(df)
# Output the number of rows
# print("Total rows: {0}".format(len(df)))
# See which headers are available
# print(list(df))
# print(df.head())
# print(pd.isnull(df).sum())

directory = r'C:\Users\astri\.PyCharm2019.2\wind_meas\Sonic_processed'
for entry in os.scandir(directory):
    df = load_csv(entry)
    # print(df.dtypes)
    df = resample_df(df)
    df = uh_wd(df)
    filename = 'SP' + os.path.splitext(os.path.basename(entry))[0][-10:] + '.csv'
    df.to_csv(os.path.join(directory, 'SP' + os.path.splitext(os.path.basename(entry))[0][-10:] + '.csv'))
