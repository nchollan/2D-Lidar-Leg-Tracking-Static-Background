#!/usr/bin/env python
import rospy, math, time, csv
import numpy as np
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

numMsgs=0				#Keeps track of how many scan messages have been received
f1=[]					#The first scan frame on startup
movementThreshold=0.5	#How far should a point be from where it was in frame 1 before its considered a moving object
legsThreshold=0.6		#How far away from the average of all moving points should a persons legs be
pubMarker = rospy.Publisher('visualization_marker',Marker, queue_size=1000)#Publisher for the markers
pubMarker2 = rospy.Publisher('visualization_marker2',Marker, queue_size=1000)
pt1=Point()
pt2=Point()
moveCnt=0
start=0
end=0
# avgPos = Point()
# prevAvgPos=Point()

outfile=open('lidarData.csv','w')
# outfile1=open('lidarYData.csv','w')
writer = csv.writer(outfile)
# writer1 = csv.writer(outfile1)

#Input:  Point(), Point()
#		pt1 = The first Point()
#		pt2 = The second Point()
#Output: Distance from pt1 to pt2
def distanceTo(pt1,pt2):
	
	return math.hypot(pt1.x-pt2.x,pt1.y-pt2.y)

#Input: int, int, int, int, dbl, dbl
#		markerId = integer to represent a unique Marker()
#		r = integer to represent red color
#		g = integer to represent green color
#		b = integer to represent blue color
#		x = double to represent x position
#		y = integer to represent y position
#Output: Marker()
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

# Input: int, int, int, int, Points[]
# 		markerId = integer to represent a unique Marker()
# 		r = integer to represent red color
# 		g = integer to represent green color
# 		b = integer to represent blue color
# 		pts = list of Points() to represent x and y positions
# Output: Marker()
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

#Input: LaserScan
#		data = LaserScan Data
#Output: None
def callback(data):
	global numMsgs, f1, movementThreshold, pubMarker, pubMarker2, moveCnt, pt1, pt2, start, end #,legsThreshold
	numMsgs+=1	 								#Keeps track of how many scan messages have been received
	if(numMsgs==1):
		f1=data.ranges 							#Grab the first frame on startup to use 
	else:
		f2=data.ranges 							#Grab frames to compare to f1 to search for movement
		i=0
		positionsXY=[] 							#Points of movement in scan
		xTot=0 									#Total of all x movement positions
		yTot=0 									#Total of all y movement positions
		k=-1.65806281567 						#Lowest radian angle measurement of lidar 
		for i in range(0,1520): 				#1521 is len(data.ranges)
			if(abs(f2[i]-f1[i])>movementThreshold):
				movePoint=Point() 				#Represent distance and angle as a point
				movePoint.x=f2[i]*(math.cos(k)) #Calculate x position
				movePoint.y=f2[i]*(math.sin(k))	#Calculate y position
				xTot+=movePoint.x 				
				yTot+=movePoint.y
				positionsXY.append(movePoint)
			k+=0.00218022723 					#Lidar range = -1.65806281567 to 1.65806281567
							 					#k = 2*1.65806281567/len(data.ranges)
		if(len(positionsXY)>0):
			moveCnt+=1
			#Calculate the average x,y position of all movement
			# avgPos.x = xTot/len(positionsXY)
			# avgPos.y = yTot/len(positionsXY)
			# start = time.time()
			# if(numMsgs%2==0):
			# 	end=time.time()
			# 	timeBtwn=end-start
			# 	distanceBtwn=distanceTo(avgPos,prevAvgPos)
			# 	speed=distanceBtwn/timeBtwn
			# 	prevAvgPos = avgPos
			if(moveCnt==1):
				pt1.x = xTot/len(positionsXY)
				pt1.y = yTot/len(positionsXY)
				start=time.time()
			else:
				pt2.x=xTot/len(positionsXY)
				pt2.y=yTot/len(positionsXY)
				end=time.time()
				timeBtwn=end-start
				distanceBtwn=distanceTo(pt1,pt2)
				speed=distanceBtwn/timeBtwn
				writer.writerow([end,speed])
				#print([end,speed])
				# d=math.sqrt((pt2.x-pt1.x)**2+(pt2.y-pt1.y)**2)
				# odom.header.stamp=rospy.Time.now()
				# odom.pose.pose.position.x=pt2.x
				# odom.pose.pose.position.y=pt2.y
				# if(d>0):
				# 	odom.twist.twist.linear.x=(speed/d)*(pt2.x-pt1.x)
				# 	odom.twist.twist.linear.y=(speed/d)*(pt2.y-pt1.y)
				# pub.publish(odom)
				pt1.x=pt2.x
				pt1.y=pt2.y
				start=time.time()
			pubMarker2.publish(makeMarker(1,1,1,1,pt1.x,pt1.y))

			# Calculate what movement should be classified as 
			# the legs based on the distance a moving point is 
			#from the average movement point
			j=Point()
			legs=[]
			for j in positionsXY:
				if(distanceTo(j,pt1)<legsThreshold):
					legs.append(j)
			pubMarker.publish(makeSphereList(4,0,0,1,legs))

#Initialize node and subscriber
def mark():
	rospy.init_node('mark', anonymous=True) 
	rospy.Subscriber('/scan', LaserScan, callback)
	rospy.spin()
if __name__ == '__main__':
    mark()
