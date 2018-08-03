#!usr/bin/env python3
import time, socket, threading, sys, argparse, csv, math #,rospy
import numpy as np
from pythonosc import udp_client, dispatcher, osc_server

#This code was designed to receive and log information from OSC packets
#being sent from an NGIMU(http://x-io.co.uk/ngimu/)

#In their documentation x-io has python example code, the OSC python
#package they used in this example is no longer supported, instead
#https://github.com/xioTechnologies/NGIMU-Python-Example/pull/1/files
#was referenced to make use of the python-osc package


#The original source code for python-osc pakage was modified to provide 
#additional utility

csvNumber='3'

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
	args = process_arguments(argv)
	# Set the NGIMU to send to this machine's IP address
	client = udp_client.SimpleUDPClient(args.ip, args.port)
	client.send_message('/wifi/send/ip', get_address())
	client.send_message('/wifi/send/port', args.receive_port)
	
	#CSV file setup
	global flag, outfile, writer, prevTime, totalTimeBtwn, timeBtwnCnt
	totalTimeBtwn=0						#Sums up the time between each message being recorded
	timeBtwnCnt=0						#Counts how many times a message has been recorded
	outfile=open('imuData' + csvNumber + '.csv','w')	#CSV for storing data recieved from the imu
	writer = csv.writer(outfile)
	flag=False							#Flag for a button press on the imu, used to start and stop recording data

	def sensorsHandler(t, add, gx, gy, gz, ax, ay, az, mx, my, mz, b):
		global flag,prevTime,totalTimeBtwn,timeBtwnCnt
		if(flag):
			#Used to calculate average frequency of messages being received
			if(timeBtwnCnt==0):
				prevTime=t
				timeBtwnCnt+=1
			else:
				timeBtwn=t-prevTime
				totalTimeBtwn+=timeBtwn
				timeBtwnCnt+=1
				prevTime=t
			#Record data to CSV
			writer.writerow([t,math.sqrt(ax**2+ay**2+az**2)])

	def setFLag(add, t):
		global flag
		flag = not flag
		print('Flag', flag)

	dispatch = dispatcher.Dispatcher()
	dispatch.map('/sensors', sensorsHandler)
	dispatch.map('/button',setFLag)

	# Set up receiver
	receive_address = get_address(), args.receive_port
	server = osc_server.ThreadingOSCUDPServer(receive_address, dispatch)
	print("Serving on {}".format(server.server_address))
	print("\nUse ctrl-C to quit.")
	print("\nTap button on NGIMU to begin data logging")

	# Start OSCServer
	server_thread = threading.Thread(target=server.serve_forever)
	prevTime=time.time()
	server_thread.start()

	# Loop while threads are running
	try :
		while 1 :
			time.sleep(1)

	except KeyboardInterrupt :
		f=open('imuFreq' + csvNumber + '.csv','w')
		w = csv.writer(f)
		w.writerow([totalTimeBtwn/timeBtwnCnt])
		server.shutdown()
		server_thread.join()
		return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
