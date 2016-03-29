import mysql.connector


def runQuery (user, host, database, query, mode="fetchone"):

	cnx = mysql.connector.connect(user='botnet-app', host='127.0.0.1', database='botnet')
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

def checkTable (user, host, database, table_name, fields):

	#sanitize(table_name)
	#sanitize(fields)

	if runQuery(user, host, database, "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = "+table_name)[0] != 1:
		runQuery(user, host, database, "CREATE TABLE"+table_name+" ( "+fields+" );"
	
	

def checkDatabase (user, host, database):
	
	#Check if database exists
	runQuery(user, host, database
	
	#Check if tables exist 
	#TODO: Figure out appropriate size varchar
	checkTable(user, host, database, "Bots", 
						"GroupID VARCHAR(255),"+\
						"ClientID VARCHAR(255),"+\
						"ClientName VARCHAR(20),"+\
						"NetworkName VARCHAR(20),"+\
						"NetworkID VARCHAR(255),"+\
						"IPAddress VARCHAR(20),"+\
						"Gateway VARCHAR(20),"+\
						"ExternalIP VARCHAR(20),"+\
						"Architecture VARCHAR(20),"+\
						"Platform VARCHAR(20),"+\
						"KernelVersion VARCHAR(20),"+\
						"PythonVersion VARCHAR(20),"+\
						"Logging VARCHAR(20)" )

	checkTable(user,host,database, "Networks",
						 "NetworkID VARCHAR(255),"+\
					 	 "NetworkName VARCHAR(20),"+\
						 "Gateway VARCHAR(20),"+\
						 "Clients VARCHAR(65535)" ) #Client IDs
	
	checkTable(user,host,database, "Groups",
						 "GroupID VARCHAR(255),"+\
						 "Clients VARCHAR(65535)" ) #Client IDs 
						 

	checkTable(user,host,database, "Queue", 
						 "ClientID VARCHAR(255),"+\
						 "Token JSON")


