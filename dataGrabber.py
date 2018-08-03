#!/usr/bin/env python
import csv, scipy.signal
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

csvNumber='3'

imu_freq = genfromtxt('imuFreq' + csvNumber + '.csv')
lidar_freq = genfromtxt('lidarFreq' + csvNumber + '.csv')
imu_data = genfromtxt('imuData' + csvNumber + '.csv' , delimiter=',')
lidar_data = genfromtxt('lidarData' + csvNumber + '.csv', delimiter=',')
x,y=zip(*imu_data)
x1,y1=zip(*lidar_data)

l=0
new_data=lidar_data.tolist()
for l in range(0,len(lidar_data)-1):
	if(lidar_data[l][0]<=imu_data[0][0]):
		del new_data[l]
lidar_data=np.asarray(new_data)

avgY=sum(y)/len(y)
avgY1=sum(y1)/len(y1)
totalAvg=(avgY+avgY1)/2
diff=totalAvg-avgY
diff1=totalAvg-avgY1

i=0
for i in range(0,len(imu_data)-1):
	imu_data[i][1]+=diff
j=0
for j in range(0,len(lidar_data)-1):
	lidar_data[j][1]+=diff1

avgOffset=lidar_freq - imu_freq
k=0
for k in range(0,len(lidar_data)-1):
	lidar_data[k][0]-=avgOffset

plt.plot(*zip(*imu_data),color='red')
plt.plot(*zip(*lidar_data),color='blue')
plt.show()
