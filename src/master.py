import mysql.connector
import jsonpickle
import simplejson

from data_types import *

## Fields
sql_user = "botnet-app"
sql_host = "127.0.0.1"
sql_db = "botnet"
queryDebug = True

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

	if queryDebug:
		print("\nQuery Executed as "+User+" on "+Host+" --> "+Database+"  with mode: "+mode)
		print("\t"+query+"\n")
	
	return result


def updateNetwork (NetworkID, NetworkName, Clients):
	runQuery("CREATE TABLE IF NOT EXISTS networks "+\
		 "(NetworkID VARCHAR(255), NetworkName VARCHAR(50), Clients JSON);")
	runQuery("REPLACE INTO bots VALUES ( '"+NetworkID+"','"+NetworkName+"','"+Clients+"' );")


def checkNetwork (NetworkID):
	return runQuery("SELECT EXISTS (SELECT NetworkID FROM networks WHERE NetworkID = "+NetworkID+";")


def removeNetwork (NetworkID):
	runQuery("DELETE FROM networks WHERE NetworkID = "+NetworkID+";")


def updateGroup (GroupID, GroupName, Clients):
	runQuery("CREATE TABLE IF NOT EXISTS groups "+\
		 "(GroupID VARCHAR(255), GroupName VARCHAR(50), Clients JSON)")
	runQuery("REPLACE INTO bots VALUES ( '"+GroupID+"','"+GroupName+"','"+Clients+"' );")
	

def checkGroup (GroupID):
	return runQuery("SELECT EXISTS (SELECT GroupID FROM groups WHERE GroupID = "+GroupID+";")


def removeGroup (GroupID):
	runQuery("DELETE FROM groups WHERE GroupID = "+GroupID+";")



def updateClient (ClientID, NetworkID, GroupID, Client):
	runQuery("CREATE TABLE IF NOT EXISTS bots "+\
		 "(ClientID VARCHAR(255), NetworkID VARCHAR(255),"+\
		 "GroupID VARCHAR(255), Client JSON, PRIMARY KEY (ClientID));")
	runQuery("REPLACE INTO bots VALUES ( '"+ClientID+"','"+NetworkID+"','"+GroupID+"','"+Client+"' );")

def checkClient (ClientID):
	return runQuery("SELECT EXISTS (SELECT ClientID FROM networks WHERE ClientID = "+ClientID+";")


def removeClient (ClientID):
	runQuery("DELETE FROM networks WHERE ClientID = "+ClientID+";")




def init ():
	if not checkNetwork ( "0" ):
		updateNetwork( "0", "Default", None )
	if not checkGroup ( "0" ):
		updateGroup( "0", "Default", None )
	
