
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 

path = r'/home/victor/Downloads/AWS_processed.csv'

#################
### Open file ###
#################

# Redefine variables for the sake of simplicity

fle = pd.read_csv(path, skiprows=1, names=['time','press','temp','hum','wspd','wdir','prec','rad'])

# conver time since epoch to datetime
import datetime
time = [datetime.datetime.fromtimestamp(i) for i in fle.time]

#################
### MAKE PLOT ###
#################


fig, axs = plt.subplots(3, 2, figsize=(15,20)) # 3x3 frame 

plt.subplot(321)
plt.plot(fle.press)
plt.title('Pressure')

plt.subplot(322)
plt.plot(fle.temp)
plt.title('Temperature')

plt.subplot(323)
plt.plot(fle.hum)
plt.title('Humidity')

plt.subplot(324)
plt.plot(fle.prec)
plt.title('Precipitation')

plt.subplot(325)
plt.plot(fle.rad)
plt.title('Radiation')

### Decompose wind speed in U and V ###
from metpy.units import units
from metpy import calc 

wspeed = [i*(units.meter/units.second) for i in fle.wspd]
wdir = [i*(units.deg) for i in fle.wdir]

ux = []
vy = []

def decompose(speed, dir):
    ux_, vy_ = calc.wind_components(speed=speed, wdir=dir)
    
    ux.append(ux_.magnitude)
    vy.append(vy_.magnitude)

    return ux, vy

a = list(map(decompose, wspeed, wdir))

fle['u'], fle['v'] = ux, vy

# speed = list(map(lambda x, y: (x**2 + y**2)**0.5, ux, vy)) # test if speed and the speed observed are the same


plt.subplot(326)
plt.plot(fle.wspd)
plt.title('Wind Speed')

'''
from cmocean import cm as cm1
ax = plt.subplot(326, polar=True)
ax.scatter(fle.wdir, fle.wspd, c=fle.wspd, cmap=cm1.speed, s=1)
#plt.title('Axis [2,1]')
'''

### Adjust plot ###
top = 0.935
bottom = 0.11
left = 0.11
right = 0.9
hspace = 0.47
wspace = 0.2

fig.subplots_adjust(bottom=bottom, top=top, right=right, left=left, hspace=hspace, wspace=wspace)