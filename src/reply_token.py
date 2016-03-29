import platform
from command import Command

class Reply_Token(object):

	def __init__(self, client_id, password, ip, cmd, info=[]):

		"""
		client_id 	ID completely unique to the client sending the token
		password	Password used to authenitcate communication
		ip		Internal IP Address of the client sending the token (Behind NAT)
		cmd		An array of detailed Command objects
		info		Used on the first beacon to update client information, can be left blank
		"""

		self.client_id = client_id 
		self.password = password
		self.ip = ip
		self.cmd = cmd
		if not info:
			self.info = [ platform.platform(), platform.release(), platform.machine(), platform.python_version() ]

	def __str__(self):
		response =  "<Response_Token>"+\
			"\n\tClient_ID: "+self.client_id+\
			"\n\tPassword: "+self.password+\
			"\n\tIP Address: "+self.ip+\
			"\n"
	
		for element in self.cmd:
			response+="\n"+str(element)
	
		return response + "\n\n</Reponse_Token>\n"


def debug():
	token = Reply_Token("SAM_PC", "Passw0rd", "129.0.0.1", [Command("Now","Eventually","ls","No Files","Hacked"), Command("Later", "ProbsNot","cat /dev/urandom", "HAHAHA", "So many")], [0])

	print(str(token))

debug()
