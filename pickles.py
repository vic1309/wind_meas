"""
This is the file for the sonic data.
"""

__author__ = "Astrid Myren, UiB"
__email__ = "astrid.myren@student.uib.no"

import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib.cm as cm
import numpy as np
import os


def rot_aws(wd):
    #Rotate wind direction with 180 degrees.
    wd = wd + 110
    # Make sure no wind direction value exeeds 360 or falls below 0
    if wd >= 360:
        wd = wd - 360
    elif wd < 0:
        wd = wd + 360
    return wd


def rot_sonic(wd):
    #Rotate wind direction with 180 degrees.
    wd = wd + 110
    # Make sure no wind direction value exeeds 360 or falls below 0
    if wd >= 360:
        wd = wd - 360
    elif wd < 0:
        wd = wd + 360
    return wd


def get_u(u_h, wd):
    # transform wd unit (deg) to radians
    wd_rad = wd / 180 * np.pi

    return - u_h * np.sin(wd_rad)


def get_v(u_h, wd):

    wd_rad = wd / 180 * np.pi

    return - u_h * np.cos(wd_rad)


sonic = r'C:\Users\astri\.PyCharm2019.2\wind_meas\sonic.pkl'
station = r'C:\Users\astri\.PyCharm2019.2\wind_meas\pickled_data\wsd.pkl'
aws = r'C:\Users\astri\.PyCharm2019.2\wind_meas\AWS_processed.csv'

# Weather station

w_df = pd.read_csv(aws, skiprows=1, names=['time','press','temp','hum','wspd','wdir','prec','rad'])

w_df['datetime'] = pd.to_datetime(w_df['time'], unit='s', origin='unix')
w_df = w_df.set_index('datetime')
w_df = w_df.drop(columns=["time"])

w_df['wdir'] = w_df.apply(lambda row: rot_aws(row['wdir']), axis=1)
w_df['u'] = w_df.apply(lambda row: get_u(row['wspd'], row['wdir']), axis=1)
w_df['v'] = w_df.apply(lambda row: get_v(row['wspd'], row['wdir']), axis=1)

# Sonic data
s_df = pd.read_pickle(sonic)

s_df['Wind direction'] = s_df.apply(lambda row: rot_sonic(row['Wind direction']), axis=1)
s_df = s_df.drop(columns=['X Wind Speed (m/s)', 'Y Wind Speed (m/s)'])
s_df['u']= s_df.apply(lambda row: get_u(row['Horizontal wind speed'], row['Wind direction']), axis=1)
s_df['v']= s_df.apply(lambda row: get_v(row['Horizontal wind speed'], row['Wind direction']), axis=1)


#w_df = w_df.shift(-65, axis=0, freq='1T')


ax = plt.gca()
s_df['u'].plot(kind='line', ax=ax)
w_df['u'].plot(kind='line', ax=ax)
plt.legend(loc='best')
plt.show()


# plt.scatter(s_df['Horizontal wind speed'].loc['2019-11-06 00:00:00':'2019-11-07 23:59:00'], w_df['wspd'].loc['2019-11-06 00:00:00':'2019-11-07 23:59:00'])
#
# plt.scatter(s_df['Wind direction'].loc['2019-11-06 00:00:00':'2019-11-07 23:59:00'], fle['wdir'].loc['2019-11-06 00:00:00':'2019-11-07 23:59:00'])
#
# ax1 = plt.gca()
# s_df['X Wind Speed (m/s)'].plot(kind='line', ax=ax1)
# w_df['u'].plot(kind='line', ax=ax1)
# plt.legend(loc='best')
# plt.show()
#
# ax2 = plt.gca()
# s_df['X Wind Speed (m/s)'].plot(kind='line', ax=ax2)
# w_df['v'].plot(kind='line', ax=ax2)
# plt.legend(loc='best')
# plt.show()
#
# ax3 = plt.gca()
# w_df['wdir'].hist(ax=ax3)
# plt.show()
#
#
# ax4 = plt.gca()
# s_df['Wind direction'].plot(kind='line', ax=ax4)
# w_df['wdir'].plot(kind='line', ax=ax4)
# plt.legend(loc='best')
# plt.show()
#
# ax5 = WindroseAxes.from_ax()
# ax5.bar(s_df['Wind direction'], s_df['Horizontal wind speed'], normed=True, opening=0.8, edgecolor='white')
# ax5.set_legend()
#
# ax5 = WindroseAxes.from_ax()
# ax5.bar(w_df['wdir'], w_df['wspd'], normed=True, opening=0.8, edgecolor='white')
# ax5.set_legend()

