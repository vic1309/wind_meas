"""
This is the file for the sonic data.
"""

__author__ = "Astrid Myren, UiB"
__email__ = "astrid.myren@student.uib.no"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

sonic = r'C:\Users\astri\.PyCharm2019.2\wind_meas\SPcombined.csv'
station = r'C:\Users\astri\.PyCharm2019.2\wind_meas\pickled_data\wsd.pkl'
s_df = pd.read_csv(sonic)
w_df = pd.read_pickle(station)

s_df = s_df.set_index('datetime')
s_df = s_df.drop(columns=['Unnamed: 0'])

print(s_df.head())

w_df['datetime'] = pd.to_datetime(w_df["time"], unit='s',
                                       origin='unix')
w_df = w_df.set_index('datetime')
w_df = w_df.drop(columns=["time"])
print(w_df.head())

w_df = w_df.shift(-65, axis=0, freq='1T')

ax = plt.gca()
s_df['Horizontal wind speed'].plot(kind='line', ax=ax)
w_df['wspd'].plot(kind='line', ax=ax)
plt.legend(loc='best')
plt.show()


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


