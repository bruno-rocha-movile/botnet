import platform
from command import Command

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


def debug():
	token = Set_Token("SAM_PC", "129.0.0.1", [Command("Now","Eventually","ls","No Files","Hacked"), Command("Later", "ProbsNot","cat /dev/urandom", "HAHAHA", "So many")], [0])

	print(str(token))

if __name__ == "__main__":
	debug()
