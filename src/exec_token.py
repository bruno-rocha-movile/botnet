from command import Command

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


def debug():
	token = Exec_Token("SAM_PC", [Command("Now","Eventually","ls","No Files","Hacked"), Command("Later", "ProbsNot","cat /dev/urandom", "HAHAHA", "So many")], [0])

	print(str(token))

if __name__ == "__main__":
	debug()
