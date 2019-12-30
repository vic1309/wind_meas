"""
This is the file for the sonic data.
"""

__author__ = "Astrid Myren, UiB"
__email__ = "astrid.myren@student.uib.no"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

sonic = r'C:\Users\astri\.PyCharm2019.2\wind_meas\sonic.pkl'
station = r'C:\Users\astri\.PyCharm2019.2\wind_meas\pickled_data\wsd.pkl'
s_df = pd.read_pickle(sonic)
w_df = pd.read_pickle(station)


w_df['datetime'] = pd.to_datetime(w_df["time"], unit='s', origin='unix')
w_df = w_df.set_index('datetime')
w_df = w_df.drop(columns=["time"])

print(w_df.head())
print(s_df.head())
# print(s_df.dtypes)
# print(w_df.dtypes)
# print(s_df.isnull().sum())
# print(w_df.isnull().sum())
print(len(s_df.index))
print(len(w_df.index))

w_df = w_df.shift(-65, axis=0, freq='1T')
w_df['v']= - w_df['v']

ax = plt.gca()
s_df['Horizontal wind speed'].plot(kind='line', ax=ax)
w_df['wspd'].plot(kind='line', ax=ax)
plt.legend(loc='best')
plt.show()


plt.scatter(s_df['Horizontal wind speed'].loc['2019-11-06 00:00:00':'2019-11-07 23:59:00'], w_df['wspd'].loc['2019-11-06 00:00:00':'2019-11-07 23:59:00'])

# ax = plt.gca()
# s_df['x_vel'].plot(kind='line', ax=ax)
# w_df['u'].plot(kind='line', ax=ax)
# plt.legend(loc='best')
# plt.show()
#
# ax = plt.gca()
# s_df['y_vel'].plot(kind='line', ax=ax)
# w_df['v'].plot(kind='line', ax=ax)
# plt.legend(loc='best')
# plt.show()
#
# ax1 = plt.gca()
# w_df['wspd'].hist(ax=ax1)
# plt.legend(loc='best')
# plt.show()


