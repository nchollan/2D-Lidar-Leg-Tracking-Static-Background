#!usr/bin/env python3
import os, signal, subprocess, time, socket, threading, sys, argparse, csv, math #,rospy
import numpy as np
from pythonosc import udp_client, dispatcher, osc_server
#from sensor_msgs.msg import Imu

global proc




def process_arguments(argv):
	parser = argparse.ArgumentParser(description="NGIMU python example")
	parser.add_argument(
		"--ip",
		default="192.168.1.1",
		help="NGIMU IP Address")
	parser.add_argument(
		"--port",
		type=int,
		default=9000,
		help="NGIMU Port")
	parser.add_argument(
		"--receive_port",
		type=int,
		default=8001,
		help="Port to receive messages from NGIMU to this computer")

	return parser.parse_args(argv[1:])
#https://ubuntuforums.org/showthread.php?t=821325
def get_address():
    try:
        address = socket.gethostbyname(socket.gethostname())
        # On my system, this always gives me 127.0.1.1. Hence...
    except:
        address = ''
    if not address or address.startswith('127.'):
        # ...the hard way.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('4.2.2.1', 0))
        address = s.getsockname()[0]
    return address
def main(argv):
	#rospy.init_node('imuListener', anonymous=True)
	#pub = rospy.Publisher('/imuReadings',Imu, queue_size=1000)
	args = process_arguments(argv)

	# Set the NGIMU to send to this machine's IP address
	client = udp_client.SimpleUDPClient(args.ip, args.port)
	client.send_message('/wifi/send/ip', get_address())
	client.send_message('/wifi/send/port', args.receive_port)
	
	#CSV file setup
	global flag, outfile, writer, proc
	outfile=open('imuData.csv','w')
	writer = csv.writer(outfile)
	flag=False

	#Imu
	#global imu
	#imu = Imu()

	def sensorsHandler(t, add, gx, gy, gz, ax, ay, az, mx, my, mz, b):
		global flag#,imu
		if(flag):
			writer.writerow([t,math.sqrt(ax**2+ay**2+az**2)])
			#print('{} {} g[{},{},{}] a[{},{},{}] m[{},{},{}] b[{}]'.format(t, add, gx, gy, gz, ax, ay, az, mx, my, mz, b))
			# imu.header.stamp=rospy.Time.now()
			# imu.angular_velocity.x=gx
			# imu.angular_velocity.y=gy
			# imu.angular_velocity.z=gz
			# imu.linear_acceleration.x=ax
			# imu.linear_acceleration.y=ay
			# imu.linear_acceleration.z=az
			#pub.publish(imu)

	
	# def quaternionHandler(t, add, x, y, z, w):
	# 	global flag,imu
	# 	if(flag):
	# 		imu.orientation.x=x
	# 		imu.orientation.y=y
	# 		imu.orientation.z=z
	# 		imu.orientation.w=w
	# 		#writer.writerow([t, add, x, y, z, w])
	# 		#print('{} {} [{},{},{},{}]'.format(t, add, x, y, z, w))

	def setFLag(add, time):
		global flag, proc
		flag = not flag
		if(flag):
			print("Made it")
			proc=subprocess.Popen('rosrun mypkg1 mark.py',shell=True)
		else:
			proc.kill()
		print('Flag', flag)

	dispatch = dispatcher.Dispatcher()
	dispatch.map('/sensors', sensorsHandler)
	#dispatch.map('/quaternion',quaternionHandler)
	dispatch.map('/button',setFLag)

	# Set up receiver
	receive_address = get_address(), args.receive_port
	server = osc_server.ThreadingOSCUDPServer(receive_address, dispatch)
	print("Serving on {}".format(server.server_address))
	print("\nUse ctrl-C to quit.")
	print("\nTap button on NGIMU to begin data logging")

	# Start OSCServer
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.start()

	# Loop while threads are running
	try :
		while 1 :
			time.sleep(1)

	except KeyboardInterrupt :
		server.shutdown()
		server_thread.join()
		return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
