#!/usr/bin/env python
import rospy, math, time, csv
import numpy as np
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

numMsgs=0
pt1=Point()
pt2=Point()
start=0
end=0
allData=[]

def distanceTo(pt1,pt2):
	return math.hypot(pt1.x-pt2.x,pt1.y-pt2.y)

def callback(data):
	global numMsgs, start, end, allData
	numMsgs+=1
	if(numMsgs==1):
		pt1.x=data.pose.position.x
		pt1.y=data.pose.position.y
		start=time.time()
	else:
		pt2.x=data.pose.position.x
		pt2.y=data.pose.position.y
		end=time.time()
		timeBtwn=end-start
		distanceBtwn=distanceTo(pt1,pt2)
		speed=distanceBtwn/timeBtwn
		allData.append([[pt1.x,pt1.y],[pt2.x,pt2.y],timeBtwn,distanceBtwn,speed])
		pt1.x=pt2.x
		pt1.y=pt2.y
		start=time.time()
		
#Initialize node and subscriber
def calc():
	rospy.init_node('calc', anonymous=True) 
	rospy.Subscriber('/visualization_marker2', Marker, callback)
	rospy.spin()
	with open('movement.csv', 'wb') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		wr.writerow(allData)
if __name__ == '__main__':
    calc()
