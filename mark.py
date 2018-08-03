#!/usr/bin/env python
import rospy, math, time, csv
import numpy as np
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

#This code was designed to track a single moving person, walking in a static environment
#using a Hokuyo lidar.

#In order for this method of tracking to work, the lidar must first scan the room without
#any movement to set the baseline for what isn't considered movement. After the first frame
#is acquired it will be used to visualize any change(ie the person being tracked)

#Rostopics
#Subscribed: /scan (LaserScan)
#Publishing: /visualization_marker (Marker)
#			 /visualization_marker2 (Marker)

numMsgs=0				#Keeps track of how many scan messages have been received
f1=[]					#The first scan frame on startup

#Thresholds
#!!!These values worked for our application but may need modified for yours!!!
movementThreshold=0.5	#How far should a point be from where it was in frame 1 before its considered a moving object (Helps filter out sensor noise)
legsThreshold=0.6		#How far away from the average of all moving points should a persons legs be (Helps filter out sensor noise)

#Publishers
pubMarker = rospy.Publisher('visualization_marker',Marker, queue_size=1000)#Publisher for moving points
pubMarker2 = rospy.Publisher('visualization_marker2',Marker, queue_size=1000)#Publisher for average of moving points

#Average moving position points
pt1=Point()
pt2=Point()

#Used to calculate speed of moving person
moveCnt=0
start=0
end=0
speedTotal=0
prevSpeed=0

#Used to calculate average frequency of recorded data
totalTimeBtwn=0
avgTimeBtwn=0			
timeBtwnCnt=0

#CSV file for recording lidar data into
csvNumber='3'
outfile=open('lidarData' + csvNumber + '.csv','w')
writer = csv.writer(outfile)

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
	global numMsgs, f1, movementThreshold, pubMarker, pubMarker2, moveCnt, pt1, pt2, start, end, speedTotal, totalTimeBtwn, timeBtwnCnt, writer ,legsThreshold, prevSpeed
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
		if(len(positionsXY)>0):					#Make sure that something is moving in the frame
			moveCnt+=1		

			#Calculate the speed of the person in the frame
			#Take average of all moving points as the position of the person
			#Current average position - Previous average position
			#End time - Start time to determine how fast the distance between positions was traveled					
			if(moveCnt==1):
				pt1.x = xTot/len(positionsXY)
				pt1.y = yTot/len(positionsXY)
				start=time.time()
				prevSpeed=0
			else:
				pt2.x=xTot/len(positionsXY)
				pt2.y=yTot/len(positionsXY)
				end=time.time()
				timeBtwn=end-start
				distanceBtwn=distanceTo(pt1,pt2)
				speed=distanceBtwn/timeBtwn
				print([end,(speed-prevSpeed)/timeBtwn])
				totalTimeBtwn+=timeBtwn
				timeBtwnCnt+=1
				speedTotal+=speed
				avgSpeed=(speedTotal/timeBtwnCnt)
				if(abs(speed-avgSpeed)<5): #Filter out large spikes in speed
					writer.writerow([end,(speed-prevSpeed)/timeBtwn])
				pt1.x=pt2.x
				pt1.y=pt2.y
				start=time.time()
				prevSpeed=speed
			pubMarker2.publish(makeMarker(1,1,1,1,pt1.x,pt1.y))

			# Calculate what movement should be classified as 
			# the legs based on the distance a moving point is 
			# from the average movement point
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

	#Write what the average recording frequency was for the lidar data collected to a CSV (Used for syncronization)
	f=open('lidarFreq' + csvNumber + '.csv','w')
	w = csv.writer(f)
	w.writerow([totalTimeBtwn/timeBtwnCnt])

if __name__ == '__main__':
    mark()
