import time
import binascii
from hashlib import *

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

