# botnet
A persistent and stealthy botnet using several methods of beaconing.


-- Source Files --

1. bot.py
	The client to install

2. master.py
	The command and control center for the botnet

3. exec_token.py
	Command Token sent from the master to the bots

4. set_token.py
	Token sent from the master to update bot settings

5. reply_token.py
	This is the beacon message the bot will send

6. command.py
	An object to represent and store information about a sent command


-- PIP Install Dependencies --

    shell> pip install -r requirements.txt
