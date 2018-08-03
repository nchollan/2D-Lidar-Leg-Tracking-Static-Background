#!/usr/bin/env python
import csv, scipy.signal
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

imu_freq = genfromtxt('imuFreq1.csv')
lidar_freq = genfromtxt('lidarFreq1.csv')
imu_data = genfromtxt('imuData1.csv', delimiter=',')
lidar_data = genfromtxt('lidarData1.csv', delimiter=',')
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


# x,y=zip(*imu_data)
# x1,y1=zip(*lidar_data)
# indexes=scipy.signal.find_peaks_cwt(y, np.arange(1, 4))#,max_distances=np.arange(1, 4)*2
# indexes1=scipy.signal.find_peaks_cwt(y1, np.arange(1, 4))#,max_distances=np.arange(1, 4)*2
# i=[]
# for i in indexes:
# 	plt.plot(imu_data[i][0],imu_data[i][1],'ro',color='green')
# j=[]
# for j in indexes1:
# 	plt.plot(lidar_data[j][0],lidar_data[j][1],'ro',color='black')
# print('Imu: ',len(indexes))
# print('Lidar: ',len(indexes1))
#x,y=zip(*imu_data)
#x1,y1=zip(*lidar_data)
#indexes=scipy.signal.find_peaks_cwt(y, np.arange(1, 2))#,max_distances=np.arange(1, 4)*2
#indexes1=scipy.signal.find_peaks_cwt(y1, np.arange(1, 2))#,max_distances=np.arange(1, 4)*2
#total=(lidar_data[indexes1[5]][0]-imu_data[indexes[7]][0])+(lidar_data[indexes1[9]][0]-imu_data[indexes[9]][0])+(lidar_data[indexes1[22]][0]-imu_data[indexes[21]][0])+(lidar_data[indexes1[24]][0]-imu_data[indexes[23]][0])+(lidar_data[indexes1[25]][0]-imu_data[indexes[24]][0])+(10*0.0966977834701)
#avgOffset=total/15
# avgOffset=0.0988938967387
# avgOffset=0.0988938967387



avgOffset=lidar_freq - imu_freq
k=0
for k in range(0,len(lidar_data)-1):
	lidar_data[k][0]-=avgOffset




# plt.plot(imu_data[indexes[115]][0],imu_data[indexes[115]][1],'ro',color='brown')
# plt.plot(lidar_data[indexes1[97]][0],lidar_data[indexes1[97]][1],'ro',color='pink')


plt.plot(*zip(*imu_data),color='red')
plt.plot(*zip(*lidar_data),color='blue')
# x,y=zip(*imu_data)
# x1,y1=zip(*lidar_data)
# plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color='orange')
# plt.plot(np.unique(x1), np.poly1d(np.polyfit(x1, y1, 1))(np.unique(x1)),color='black')
plt.show()
