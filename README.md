# 2D-Lidar-Leg-Tracking-Static-Background

The purpose of this project was to track and log position and velocity information of a person walking in a static environment using a Hokuyo lidar while simultaneously logging imu data from an NGIMU strapped to the persons shoe, and afterwords syncronizing the logged data.

Hardware:
NGIMU (http://x-io.co.uk/ngimu/)
Hokuyo UXM-30LX-EW (https://www.hokuyo-aut.jp/search/single.php?serial=171)

Software:
Python3 was used for imuListener.py in order to integrate python-osc
Python2 was used for everything else

Notes:
-A python-osc folder has been included because modifications are necessary to the original source code, for this application to work

!!!The log files will just overwrite eachother the way they are currently being implmented!!!


!!!These steps are for linux users only!!!

This is the version being used here:
Description:	Ubuntu 16.04.4 LTS
Release:	16.04
Codename:	xenial

Step 1: 
        Install ROS (For this application ros-kinetic is being used)
Step 2: 
        Install all python dependencies (Probably easiest to create a python3 virtualenv for python3 dependencies)
Step 3: 
        Modify python-osc (Reference python-osc folder in this project)
Step 4: 
        Power up the Hokuyo UXM-30LX-EW and connect it to the computer
Step 5:  
        Map wired connection IP (This is the Lidar)
        Go to your network connections,
        Click "Edit Connections..."
        Click on the Lidar connection
        Click "Edit"
        Click "IPv4 Settings"
        Select Method "Manual"
        And enter into "Addresses" as seen below:
        Address=192.168.0.15
        Netmask=24
        Gateway=192.168.0.1
Step 6:
        Setup network so that you can receive data from ethernet port and over wifi
Step 5:
        Power on the NGIMU
        Connect to it and the Hokuyo UXM-30LX-EW 
Step 6:
        Run roscore
Step 7:
        Run rosrun urg_node urg_node _ip_address:=192.168.0.10
Step 8:
        Run rosrun rviz rviz
Step 9:
        create a catkin workspace
        cd to your catkin workspace
        clone files (excluding python-osc folder) into that workspace
Step 10:
        Make sure you are in your workspace
        Run python3 imuListener.py
Step 11:
        Make sure you are in your workspace
        Make sure the lidar is positioned properly and won't "see" any movement upon running mark.py
        Run rosrun <Workspace> mark.py
Step 12:
        Click the button on the NGIMU
        Then walk into the lidar's view
        !!Stand still for 3 seconds or so, there is a running average of your location being taken to reduce outliers!!
Step 13:
        Ctrl+C mark.py
        Ctrl+C imuListener.py (Pressing the button will stop data logging but this will write all the necessary CSV's)
Step 14:
        Make sure you are in your workspace
        Run rosrun <Workspace> dataGrabber.py
        (Modify dataGrabber.py to visualize different data)
