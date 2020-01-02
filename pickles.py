"""
This is the file for the sonic data.
"""

__author__ = "Astrid Myren, UiB"
__email__ = "astrid.myren@student.uib.no"

import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib
import matplotlib.cm as cm
import numpy as np
import os


def rot_aws(wd):
    #Rotate wind direction with 180 degrees.
    wd = wd + 230 # 230
    # Make sure no wind direction value exeeds 360 or falls below 0
    if wd >= 360:
        wd = wd - 360
    elif wd < 0:
        wd = wd + 360
    return wd


def rot_sonic(wd):
    #Rotate wind direction with 110 degrees.
    wd = wd + 160 #160
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


def power_law(z, u_ref, z_ref, alpha):
    """
    power law approach to estimate the wind profile from a reference wind speed measurement

    Parameters
    ----------
    z : float
       chosen height levels the wind speed will be extrapolated to
    u_ref : float
        reference value of wind speed measured on reference level z_ref
    z_ref : float
        reference level
    alpha :float
       (alpha)-exponent value of power law

    Results
    -------
    u :float
        array of wind speed values corresponding to chosen height levels (z)
    """
    u = u_ref * (z / z_ref) ** alpha

    return u


def get_power_output(d, u_0, rho=1.3):
    """
    Estimate of power output from wind

    Parameters
    ----------
    cp : float
        power coefficient
    d : float
       rotor diameter
    u_0 : float
        wind speed (undisturbed flow)
    rho : float
        air density
    cut_in : float
        cut-in wind speed
    rated : float
        rated wind speed
    cut_out : float
        cut-out wind speed

    Results
    -------
    P : float
        power output from wind
    """
    # Estimate the Rotor Area from rotor diameter
    A = np.pi * (d / 2) ** 2

    P = 0.5 * A * rho * u_0 ** 3/1000

    # # cut-in speed
    # P[u_0 < cut_in] = 0
    # # cut-out speed
    # P[u_0 >= cut_out] = 0
    # # rated speed
    # P[(u_0 > rated) & (u_0 < 25)] = 0.5  * A * rho * rated ** 3

    return P


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

w_df.to_pickle('./rotated_aws.pkl')

# Sonic data
s_df = pd.read_pickle(sonic)

s_df['Wind direction'] = s_df.apply(lambda row: rot_sonic(row['Wind direction']), axis=1)
s_df = s_df.drop(columns=['X Wind Speed (m/s)', 'Y Wind Speed (m/s)'])
s_df['u']= s_df.apply(lambda row: get_u(row['Horizontal wind speed'], row['Wind direction']), axis=1)
s_df['v']= s_df.apply(lambda row: get_v(row['Horizontal wind speed'], row['Wind direction']), axis=1)

# Power law
alpha = 1/7
z= 120 #m
z_ref = 2 #m
s_df['wspd 120 m'] = s_df.apply(lambda row: power_law(z, row['Horizontal wind speed'], z_ref, alpha), axis=1)

d = 90 #m
s_df['Power'] = s_df.apply(lambda row: get_power_output(d, row['wspd 120 m']), axis=1)

s_df['Max power'] = s_df['Power']*.59




# n = 10 #10 min rolling mean
# u_mean = s_df['u'].mean()
# v_mean = s_df['v'].mean()
# w_mean = s_df['Z Wind Speed (m/s)'].mean()
#
# s_df['u prim'] = s_df['u'] - u_mean
# s_df['v prim'] = s_df['v'] - v_mean
# s_df['w prim'] = s_df['Z Wind Speed (m/s)'] - w_mean
#
# s_df['uw prim']



#w_df = w_df.shift(-65, axis=0, freq='1T')

# # Compare sonic and aws u and v wind
# ax = plt.gca()
# s_df['u'].plot(kind='line', ax=ax)
# w_df['u'].plot(kind='line', ax=ax)
# plt.legend(loc='best')
# plt.show()
#
# ax = plt.gca()
# s_df['v'].plot(kind='line', ax=ax)
# w_df['v'].plot(kind='line', ax=ax)
# plt.legend(loc='best')
# plt.show()

plt.rcParams.update({'font.size': 22})

# Plots of sonic data
s_df['Wind direction'].plot(kind='line', linewidth=2)
plt.title('Sonic Anemometer: Wind direction')
plt.ylabel('Degrees from North')

plt.show()

s_df['Horizontal wind speed'].plot(kind='line', linewidth=2)
plt.title('Sonic Anemometer: Horizontal wind speed (m/s)')
plt.ylabel('Wind speed (m/s)')
plt.show()


# Plot of available power in wind
ax = plt.gca()
s_df['Power'].plot(kind='line', ax=ax)
s_df['Max power'].plot(kind='line', ax=ax)
plt.title('Sonic Anemometer: Power Output (kW)')
plt.ylabel('Power (kW)')
plt.legend(loc='best')
plt.show()

ax3 = plt.gca()
s_df['wspd 120 m'].hist(ax=ax3)
plt.show()


plt.scatter(s_df['Horizontal wind speed'].loc['2019-11-05 00:00:00':'2019-11-10 23:59:00'], w_df['wspd'].loc['2019-11-05 00:00:00':'2019-11-10 23:59:00'])


plt.scatter(s_df['Wind direction'].loc['2019-11-05 00:00:00':'2019-11-10 23:59:00'], w_df['wdir'].loc['2019-11-05 00:00:00':'2019-11-10 23:59:00'])
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

ax = WindroseAxes.from_ax()
ax.bar(s_df['Wind direction'], s_df['Horizontal wind speed'], normed=True, opening=0.8, edgecolor='white')
ax.set_legend()


ax = WindroseAxes.from_ax()
ax.bar(w_df['wdir'], w_df['wspd'], normed=True, opening=0.8, edgecolor='white')
ax.set_legend()
