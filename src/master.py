import mysql.connector
import jsonpickle
import simplejson

from data_types import *

## Fields
sql_user = "botnet-app"
sql_host = "127.0.0.1"
sql_db = "botnet"


def runQuery (query, mode="fetchone", User=sql_user, Host=sql_host, Database=sql_db):

	cnx = mysql.connector.connect(user=User, host=Host, database=Database)
	cursor = cnx.cursor()

	cursor.execute(query)
	result = None

	if mode == "fetchall":
		result = cursor.fetchall()
	elif mode.startswith("fetchmany:")
		s = int(mode.strip("fetchmany:"))
		result = cursor.fetchmany(size=s)
	else:
		result =  cursor.fetchone()
	cursor.close()
	cnx.close()
	return result

def addNetwork(NetworkID, NetworkName, Gateway, Clients):
	pass #TODO
def addGroup(GroupID, GroupName, Clients):
	pass


def checkEntry (table_name, entry):
	if runQuery(table_name, "SELECT COUNT(*) FROM "+table_name+" WHERE "+entry+";")[0] < 1:
		return False
	else:
		return True

def checkTable (user, host, database, table_name, fields):

	#sanitize(table_name)
	#sanitize(fields)

	if runQuery("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = "+table_name)[0] != 1:
		runQuery("CREATE TABLE"+table_name+" ( "+fields+" );")
		return False
	else:
		return True
	

def checkDatabase (user, host, database):
	
	#Check if database exists
	#runQuery(user, host, database
	
	#Check if tables exist 
	#TODO: Figure out appropriate size varchar
	bots = checkTable(user, host, database, "Bots", 
						"GroupID VARCHAR(255),"+\
						"GroupName VARCHAR(20)"+\
						"ClientID VARCHAR(255),"+\
						"ClientName VARCHAR(20),"+\
						"NetworkName VARCHAR(20),"+\
						"NetworkID VARCHAR(255),"+\
						"IPAddress VARCHAR(20),"+\
						"Client JSON")

	nets = checkTable(user,host,database, "Networks",
						 "NetworkID VARCHAR(255),"+\
					 	 "NetworkName VARCHAR(20),"+\
						 "Gateway VARCHAR(20),"+\
						 "Clients JSON)" ) #Clients Object, contains array of Client ID's
	
	groups = checkTable(user,host,database, "Groups",
						 "GroupID VARCHAR(255),"+\
						 "GroupName VARCHAR(20),"+\
						 "Clients JSON" ) #Clients Object, contains array of Client ID's
						 

	q = checkTable(user,host,database, "Queue", 
						 "ClientID VARCHAR(255),"+\
						 "Token JSON")

	if not nets:
		addNetwork(0, "Default", "0.0.0.0", None)
	if not groups:
		addGroup(0, "Default", None) 	
