#!/usr/bin/env python
import rospy, math
import numpy as np
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
numMsgs=0
f1=[]
movementThreshold=0.5
legsThreshold=0.6
perLegThreshold=0.2#0.1
pubMarker = rospy.Publisher('visualization_marker',Marker, queue_size=1000)
pubMarker2 = rospy.Publisher('visualization_marker2',Marker, queue_size=1000)

def distanceTo(pt1,pt2):

	return math.hypot(pt1.x-pt2.x,pt1.y-pt2.y)
def makeMarker(markerId,r,g,b,x,y):
	marker = Marker()
	marker.header.frame_id = "laser"
	marker.lifetime = rospy.Duration(0.5)
	marker.id=markerId
	marker.type = marker.SPHERE
	marker.action = marker.ADD
	marker.scale.x = 0.1
	marker.scale.y = 0.1
	marker.scale.z = 0.1
	marker.color.a = 1.0
	marker.color.r = r
	marker.color.g = g
	marker.color.b = b
	marker.pose.position.x=x
	marker.pose.position.y=y
	return marker
def makeSphereList(markerId,r,g,b,pts):
	marker = Marker()
	marker.type = marker.SPHERE_LIST
	marker.action = marker.ADD
	marker.header.frame_id = "laser"
	marker.id=markerId
	marker.scale.x = 0.1
	marker.scale.y = 0.1
	marker.scale.z = 0.1
	marker.color.r = r
	marker.color.g = g
	marker.color.b = b
	marker.color.a = 1.0
	marker.lifetime = rospy.Duration(0.5)
	marker.points=pts
	return marker
def callback(data):
	global numMsgs, f1, movementThreshold, legsThreshold, perLegThreshold, pubMarker, pubMarker2
	numMsgs+=1
	if(numMsgs==1):
		f1=data.ranges
	else:
		f2=data.ranges
		i=0
		positionsXY=[]
		xTot=0
		yTot=0
		k=-1.65806281567
		for i in range(0,1520):
			if(abs(f2[i]-f1[i])>movementThreshold):
				movePoint=Point()
				movePoint.x=f2[i]*(math.cos(k))
				movePoint.y=f2[i]*(math.sin(k))
				xTot+=movePoint.x
				yTot+=movePoint.y
				positionsXY.append(movePoint)
			k+=0.00218022723
		if(len(positionsXY)>0):
			avgPos= Point()
			avgPos.x=xTot/len(positionsXY)
			avgPos.y=yTot/len(positionsXY)
			pubMarker.publish(makeMarker(1,1,1,1,avgPos.x,avgPos.y))
			j=Point()
			ft1=[]
			ft2=[]
			leg1Avg=Point()
			leg2Avg=Point()
			leg1xTot=0
			leg1yTot=0
			leg2xTot=0
			leg2yTot=0
			for j in positionsXY:
				if(distanceTo(j,avgPos)<legsThreshold):
					if(distanceTo(positionsXY[0],j)<perLegThreshold):
						leg1xTot+=j.x
						leg1yTot+=j.y
						ft1.append(j)
					else:
						leg2xTot+=j.x
						leg2yTot+=j.y
						ft2.append(j)
			# if(len(ft1)>0 and len(ft2)>0):
			# 	leg1Avg.x=leg1xTot/len(ft1)
			# 	leg1Avg.y=leg1yTot/len(ft1)
			# 	leg2Avg.x=leg2xTot/len(ft2)
			# 	leg2Avg.y=leg2yTot/len(ft2)
			# 	pubMarker.publish(makeMarker(2,1,0,1,leg1Avg.x,leg1Avg.y))
			# 	pubMarker.publish(makeMarker(3,0,1,1,leg2Avg.x,leg2Avg.y))
			pubMarker.publish(makeSphereList(4,0,0,1,ft1))
			pubMarker2.publish(makeSphereList(5,0,1,0,ft2))
def mark():
	rospy.init_node('mark', anonymous=True)
	rospy.Subscriber('/scan', LaserScan, callback)
	rospy.spin()
if __name__ == '__main__':
    mark()
