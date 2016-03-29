import time
import binascii
from hashlib import *
import platform


class CoreInfo(object):
	
	def __init__(self, GroupID, ClientID, Name, Logging):
		self.gid = GroupID
		self.cid = ClientID
		self.name = Name
		self.logging = Logging


class Client(object):

	def __init__(self, ):

		"""
		client_id 	ID completely unique to the client sending the token
		ip		Internal IP Address of the client sending the token (Behind NAT)
		cmd		An array of detailed Command objects
		err		An array of python exceptions that were encountered
		info		Used on the first beacon to update client information, can be left blank
		"""

		self.client_id = client_id 
		self.ip = ip
		self.cmd = cmd
		self.err = err
		if not info:
			self.info = [ platform.platform(), platform.release(), platform.machine(), platform.python_version() ]
		else:
			self.info =  []

	def __str__(self):

		response =  "<Response_Token>"+\
			"\n\tClient_ID: "+self.client_id+\
			"\n\tIP Address: "+self.ip+\
			"\n\n\tInfo: \n"
			
		for element in self.info:
			response+="\n\t"+str(element)
		response+="\n"
		for element in self.cmd:
			response+="\n"+str(element)
	
		return response + "\n\n</Reponse_Token>\n"


class Reply_Token(object):

	def __init__(self, client_id, ip, cmd, err=[], info=[]):

		"""
		client_id 	ID completely unique to the client sending the token
		ip		Internal IP Address of the client sending the token (Behind NAT)
		cmd		An array of detailed Command objects
		err		An array of python exceptions that were encountered
		info		Used on the first beacon to update client information, can be left blank
		"""

		self.client_id = client_id 
		self.ip = ip
		self.cmd = cmd
		self.err = err
		if info == [0]:
			self.info = [ platform.platform(), platform.release(), platform.machine(), platform.python_version() ]
		else:
			self.info =  []

	def __str__(self):

		response =  "<Response_Token>"+\
			"\n\tClient_ID: "+self.client_id+\
			"\n\tIP Address: "+self.ip+\
			"\n\n\tInfo: \n"
			
		for element in self.info:
			response+="\n\t"+str(element)
		response+="\n"
		for element in self.cmd:
			response+="\n"+str(element)
	
		return response + "\n\n</Reponse_Token>\n"


class Exec_Token(object):

	def __init__(self, client_id, cmd):

		"""
		client_id 	ID completely unique to the client sending the token
		cmd		An array of detailed Command objects
		"""

		self.client_id = client_id 
		self.cmd = cmd

	def __str__(self):

		token =  "<Exec_Token>"+\
			"\n\tClient_ID: "+self.client_id

		for element in self.cmd:
			response+="\n"+str(element)
	
		return response + "\n\n</Exec_Token>\n"


class Set_Token(object):

	def __init__(self, client_id, ip, cmd, err=[], info=[]):

		"""
		client_id 	ID completely unique to the client sending the token
		ip		Internal IP Address of the client sending the token (Behind NAT)
		cmd		An array of detailed Command objects
		err		An array of python exceptions that were encountered
		info		Used on the first beacon to update client information, can be left blank
		"""

		self.client_id = client_id 
		self.ip = ip
		self.cmd = cmd
		self.err = err
		if not info:
			self.info = [ platform.platform(), platform.release(), platform.machine(), platform.python_version() ]
		else:
			self.info =  []

	def __str__(self):

		response =  "<Response_Token>"+\
			"\n\tClient_ID: "+self.client_id+\
			"\n\tIP Address: "+self.ip+\
			"\n\n\tInfo: \n"
			
		for element in self.info:
			response+="\n\t"+str(element)
		response+="\n"
		for element in self.cmd:
			response+="\n"+str(element)
	
		return response + "\n\n</Reponse_Token>\n"


class Command(object):
	
	def __init__(self, start, end, cmd, out, err=""):

		self.start = start
		self.end = end
		self.cmd = cmd
		self.out = out
		self.err = err
		
		hasher = sha512()
		hashed = hasher.update(
					  str(self.start).encode('utf-8') +\
					  str(self.end).encode('utf-8') +\
					  str(self.cmd).encode('utf-8') +\
					  str(self.out).encode('utf-8') +\
					  str(self.err).encode('utf-8') 
					)
		self.uid = str(binascii.hexlify(hasher.digest())).encode('utf-8')

	def __str__(self):

		return "\t<Command>"+\
			"\n\t\tUID: "+self.uid+\
			"\n\t\tStart: "+self.start+\
			"\n\t\tEnd: "+self.end+\
			"\n\t\tCommand Executed: "+self.cmd+\
			"\n\t\tOutput: "+self.out+\
			"\n\t\tError(s): "+self.err+\
			"\n\t</Command>\n"



def setDebug():
	token = Set_Token("SAM_PC", "129.0.0.1", [Command("Now","Eventually","ls","No Files","Hacked"), Command("Later", "ProbsNot","cat /dev/urandom", "HAHAHA", "So many")], [0])
	print(str(token))

def replyDebug():
	token = Reply_Token("SAM_PC", "129.0.0.1", [Command("Now","Eventually","ls","No Files","Hacked"), Command("Later", "ProbsNot","cat /dev/urandom", "HAHAHA", "So many")], [0])
	print(str(token))

def execDebug():
	token = Exec_Token("SAM_PC", [Command("Now","Eventually","ls","No Files","Hacked"), Command("Later", "ProbsNot","cat /dev/urandom", "HAHAHA", "So many")], [0])
	print(str(token))

if __name__ == "__main__":
	execDebug()
	replyDebug()
	setDebug()

