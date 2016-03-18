"""
Created by Kyle Carretto with the wonderful help of the Impacket Framwork:
                                        https://github.com/CoreSecurity/impacket/tree/master/impacket
"""
import socket
import os
import sys
import select
import time
import threading
import Queue

from impacket import ImpactDecoder
from impacket import ImpactPacket
from impacket import crypto

def getlocalip():
	"""
		Thanks to Alexander @ stackoverflow for a quick, portable way to get an IP.
	"""
	return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

localhost = getlocalip()
ENCRYPTION_KEY = "PleaseEncryptStuffBecauseIt'sNiceToDo"
recvQ = Queue.Queue()

def crypt(string,password):
    try:
    	return crypto.encryptSecret(password,string)
    except Exception as e:
	print e

def decrypt(string,password):
    try:
    	return crypto.decryptSecret(password,string)
    except Exception as e:
	print e


def socket_init():
    """
    Returns an initialized ICMP raw socket
    :return: Socket
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.bind((localhost, 0))

    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    return s


def send_icmp(src, dst, data):
    """
    Build an ICMP Packet with specified data, and send it
    """

    try:
	s = socket_init()
	dataQ = Queue.Queue()
	dataQ.put("!DATAGRAM-START-SEQUENCE!")
	if data.startswith("!DATAGRAM-"):
		data += "!"

	if sys.getsizeof(data) < 1000:
		dataQ.put(data)
	else:
		segment = ""
		
		for ch in data:
			if sys.getsizeof(segment+ch) > 1000:
				dataQ.put(segment)
				segment = ""
			segment += ch
		if segment != "":
			dataQ.put(segment)
	dataQ.put("!DATAGRAM-END-SEQUENCE!")
	
	while not dataQ.empty():
		segdata = dataQ.get()
		ip = ImpactPacket.IP()
    		ip.set_ip_src(src)
    		ip.set_ip_dst(dst)
	
    		icmp = ImpactPacket.ICMP()
    		icmp.set_icmp_type(icmp.ICMP_ECHOREPLY)

  	  	icmp.contains(ImpactPacket.Data(crypt(segdata,ENCRYPTION_KEY)))
    		ip.contains(icmp)
    		icmp.set_icmp_id(1)
    		icmp.set_icmp_cksum(0)
    		icmp.auto_checksum = 1
	
    		s.sendto(ip.get_packet(), (dst, 0))
    	s.close()
    except Exception as e:
	print(e)
	print "Error Encountered - Sending ICMP"

def snif_icmp():
    """
        returns the next available ICMP Data
    :return: data
    """
    try:
	    s = socket_init()
	    if s in select.select([ s ], [], [])[0]:
		data = s.recvfrom(65535)[0]

		decoder = ImpactDecoder.IPDecoder()
		rip = decoder.decode(data)
		ricmp = rip.child()
		encrypted_data = ricmp.get_data_as_string()
		real_data = decrypt(encrypted_data, ENCRYPTION_KEY)	
	        s.close()
		return real_data 
    except Exception as e:
	print "Error Encountered - Sniffing ICMP"
	print e

class TrafficHandler (threading.Thread):
    def __init__(self, outQ):
	self.outQ = outQ
        threading.Thread.__init__(self)

    def run(self):
	
	recv = False
	data = ""
        while True:
	    try:
	    	raw = recvQ.get(True,5)
	    	if raw == None or raw == "":
		    continue;
	    	else:
	    		if raw.startswith("!DATAGRAM-START-SEQUENCE!"):
				if recv:
			    	    self.outQ.put("Warning: Missed end of sequence, displaying partial data:")
		    	    	    self.outQ.put(data)
		    		data = ""
				recv = True
	    		elif raw.startswith("!DATAGRAM-END-SEQUENCE!"):
				recv = False
				self.outQ.put(data)
				data = ""
	    		else:
				data += raw
	    except Exception as e:
		pass

	

class Listener (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
	    recvQ.put(snif_icmp())
