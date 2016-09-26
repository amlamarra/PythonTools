#!/usr/bin/python3
################################################################################
# File:		pcap_convert.py
# Author:	Andrew M. Lamarra
# Modified:	9/26/2016
# Purpose:	PaloAlto provides the packets of the threats it detects in text form
#		The user will copy that text, save it to the same directory as this
#		script, and run it. The output will strip the packet headers and
#		show only the ASCII values of the packet data. This will make it
#		more readable and easier to find (ctrl+F) content.
################################################################################

# Read in the data
with open("example.txt", "r") as f:
	data = f.read()

# Remove any trailing tabs or newlines
while data[len(data)-1] == "\n" or data[len(data)-1] == "\t":
	data = data[:len(data)-1]

# Break the string up into a list of lines
lst = data.split("\n")

# Separate the data by the individual packets (this will be a 2D array)
packets = []
msg = ""
for line in lst:
	if line[0] != "\t":
		packets.append([])
	else:
		packets[len(packets)-1].append(line)
print("Number of packets = {}\n".format(len(packets)))
msg += "Number of packets = {}\n\n".format(len(packets))

# Strip out everything but the raw bytes
# As well as packet headers (first 54 bytes, 108 characters)
for x in range(len(packets)):
	temp = ""
	for y in range(len(packets[x])):
		temp += "".join(packets[x][y].split(" ")[2:-1])
	packets[x] = temp[108:]

# Print everything
for packet in packets:
	print("PACKET {}".format(packets.index(packet)+1))
	msg += "PACKET {}\n".format(packets.index(packet)+1)
	i = 0
	while i < len(packet):
		char = packet[i:i+2]
		if int(char, 16) > 127:
			char = "3f"
		print(chr(int(char, 16)), end="")
		msg += chr(int(char, 16))
		i += 2
	if packet[i-2:] != "0a" and packet[i-2:] != "0d":
		print("\n")
		msg += "\n"
	if packet[i-4:i-2] != "0a" and packet[i-4:i-2] != "0d":
		print("\n")
		msg += "\n"

# Also write it to a file
with open("cap_modified.txt", "w") as f:
	f.write(msg)
