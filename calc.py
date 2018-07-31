#!/usr/bin/env python
import rospy, math, time, csv
import numpy as np
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry

numMsgs=0
pt1=Point()
pt2=Point()
start=0
end=0
odom=Odometry()
global outfile, writer
outfile=open('lidarData.csv','w')
writer = csv.writer(outfile)

pub = rospy.Publisher('/lidarOdom',Odometry, queue_size=1000)

def distanceTo(pt1,pt2):
	return math.hypot(pt1.x-pt2.x,pt1.y-pt2.y)

def callback(data):
	global numMsgs, start, end, odom, outfile, writer
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
		writer.writerow([end,speed])
		print([end,speed])
		d=math.sqrt((pt2.x-pt1.x)**2+(pt2.y-pt1.y)**2)
		odom.header.stamp=rospy.Time.now()
		odom.pose.pose.position.x=pt2.x
		odom.pose.pose.position.y=pt2.y
		if(d>0):
			odom.twist.twist.linear.x=(speed/d)*(pt2.x-pt1.x)
			odom.twist.twist.linear.y=(speed/d)*(pt2.y-pt1.y)
		pub.publish(odom)
		pt1.x=pt2.x
		pt1.y=pt2.y
		start=time.time()
		
#Initialize node and subscriber
def calc():
	rospy.init_node('calc', anonymous=True) 
	rospy.Subscriber('/visualization_marker2', Marker, callback)
	rospy.spin()
if __name__ == '__main__':
    calc()
