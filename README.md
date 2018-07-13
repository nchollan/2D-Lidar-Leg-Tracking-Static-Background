# 2D-Lidar-Leg-Tracking-Static-Background
Tracks leg movement in an otherwise static environment
Hokuyo Laser Scanner

Step 1:
  Run roscore
  
Step 2:
  Map wired connection IP
  Address=192.168.0.15
  Netmask=24
  Gateway=192.168.0.1
  
Step 3:
Run rosrun urg_node urg_node _ip_address:=192.168.0.10

Step 4:
Run rosrun rviz rviz

Step 5:
Run rosrun <Workspace Location> mark.py
