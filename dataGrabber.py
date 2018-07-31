#!/usr/bin/env python
import matplotlib.pyplot as plt
import csv
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt


imu_data = genfromtxt('imuData.csv', delimiter=',')
lidar_data = genfromtxt('lidarData.csv', delimiter=',')
x,y=zip(*imu_data)
x1,y1=zip(*lidar_data)
plt.scatter(*zip(*imu_data),color='red')
plt.scatter(*zip(*lidar_data),color='blue')
#plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
#plt.plot(np.unique(x1), np.poly1d(np.polyfit(x1, y1, 1))(np.unique(x1)))
plt.show()


# imuX = genfromtxt('imuXData.csv', delimiter=',')
# imuY = genfromtxt('imuYData.csv', delimiter=',')
# lidarX = genfromtxt('lidarXData.csv', delimiter=',')
# lidarY = genfromtxt('lidarYData.csv', delimiter=',')

# # x,y=zip(*imuX)
# # x1,y1=zip(*imuY)
# # x2,y2=zip(*lidarX)
# # x3,y3=zip(*lidarY)

# #plt.scatter(*zip(*imuX),color='red')
# plt.scatter(*zip(*imuY),color='blue')
# #plt.scatter(*zip(*lidarX),color='green')
# plt.scatter(*zip(*lidarY),color='black')
# plt.show()
