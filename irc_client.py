#!/usr/bin/python3
import socket, argparse, threading, curses
from string import printable

SRV_IP = "" # Enter server here
SRV_PORT = 6667
SRV_ADDR = (SRV_IP, SRV_PORT)
SRV_NAME = "" # Enter server name here
NICK = "" # Enter nick
USERNAME = "" # Enter username
REALNAME = "" # Enter real name
PRINTABLE = list(map(ord, printable))
UTF = "utf-8"

sockets = []
lines = []

# Display whatever string is passed to it
def output(stdscr, msg):
	Y, X = stdscr.getyx()
	max_lines = stdscr.getmaxyx()[0] - 3
	
	# Scrolling (if necessary)
	if len(lines) > max_lines:
		del lines[0]
		stdscr.clear()
		for i, line in enumerate(lines):
			stdscr.addstr(i, 0, line)

	stdscr.addstr(len(lines), 0, msg)
	lines.append(msg)
	stdscr.move(Y, X)	# Move the cursor back to the start position
	stdscr.refresh()

# Listens for messages from the server
def listen(stdscr):
	while True:
		messages = sockets[0].recv(4096).decode(UTF).split("\r\n")
		for message in messages:
			if message != "": # Dismiss empty lines
				output(stdscr, message)
			# Automatically reply to PING messages to prevent being disconnected
			if message.split(" ")[0] == "PING":
				pong = message[0] + "O" + message[2:]
				sockets[0].sendall(pong.encode(UTF))
				output(stdscr, pong)

def user_input(stdscr):
	send = True
	inchannel = False
	channel = ""
	Ymax, Xmax = stdscr.getmaxyx()
	
	while True:
		stdscr.move(Ymax-1, 0)
		stdscr.clrtoeol()
		stdscr.addstr("> ")
		Y, X = stdscr.getyx()
		eol = X
		txt = []
		
		while True:
			y, x = stdscr.getyx()
			c = stdscr.getch()
			
			if c == 10: # Pressing Enter (\r)
				break
			elif c == curses.KEY_BACKSPACE:
				if x > X:
					eol -= 1
					del txt[x-X-1]
					stdscr.move(y, x-1)
					stdscr.clrtoeol()
					stdscr.insstr("".join(txt[x-X-1:]))
			elif c == curses.KEY_LEFT:
				if x > X:
					stdscr.move(y, x-1)
			elif c == curses.KEY_RIGHT:
				if x < eol:
					stdscr.move(y, x+1)
			elif c == curses.KEY_END:
				stdscr.move(y, eol)
			elif c == curses.KEY_HOME:
				stdscr.move(y, X)
			elif c == curses.KEY_DC: # Delete key
				if x < eol:
					eol -= 1
					del txt[x-X]
					stdscr.clrtoeol()
					stdscr.insstr("".join(txt[x-X:]))
			elif c in PRINTABLE and len(txt) < 510:
			# Each line cannot exceed 512 characters in length, including \r\n
				eol += 1
				if x < eol:
					txt.insert(x-X, chr(c))
					stdscr.insch(c)
				else:
					txt.append(chr(c))
					stdscr.addch(c)
				stdscr.move(y, (x+1))
		
		msg = "".join(txt)
		output(stdscr, "{} > {}".format(NICK, msg))
		
		if msg and msg[0] == "/" and len(msg) > 1:
			param = ""
			msg = msg[1:]
			params = len(msg.split(" ")) - 1
			if params > 0:
				param = msg.split(" ")[1]
			command = msg.split(" ")[0].upper()
			
			if command == "JOIN" and params > 0:
				if param[0] == "#":
					channel = param
					msg = "JOIN {}".format(channel)
					inchannel = True
				else:
					send = False
					output(stdscr, "Improper channel name")
			elif command == "NICK" and params > 0:
				msg = "NICK {}".format(msg.split(" ")[1])
			elif command == "PART" and inchannel == True:
				msg = "PART {}".format(channel)
				inchannel = False
			elif command == "NAMES":
				msg = "NAMES {}".format(param)
			elif command == "QUIT":
				sockets[0].sendall("QUIT\r\n".encode(UTF))
				break
			elif command == "PRIVMSG" and params > 0:
				msg = msg.split(" ")
				text = msg[2:]
				" ".join(text)
				if text[0] == ":":
					text = text[1:]
				msg = "PRIVMSG {} :{}".format(param, text)
			else:
				send = False
				output(stdscr, "Invalid command or parameter...")
				
		elif msg and msg[0] == "/" and len(msg) == 1:
			send = False
			output(stdscr, "Invalid command")
		elif msg and inchannel == True:
			msg = "PRIVMSG {} :{}".format(channel, msg)
		elif msg and inchannel == False:
			output(stdscr, "You need to be in a channel to send a message")
			send = False
			
		if send == True and msg:
			msg += "\r\n"
			sockets[0].sendall(msg.encode(UTF))
			
		send = True	# Reset the send flag
	
def main(stdscr):
	try:
		sock = socket.create_connection(SRV_ADDR)
	except socket.error in exc:
		print("Caught exception socket.error : {}".format(exc))
	sockets.append(sock)
	sockets[0].sendall("NICK {}\r\n".format(NICK).encode(UTF))
	sockets[0].sendall("USER {} 0 * :{}\r\n".format(USERNAME, REALNAME).encode(UTF))
	t = threading.Thread(target=listen,args=(stdscr,))
	t.daemon = True
	t.start()
	
	user_input(stdscr)
	
	sockets[0].shutdown(socket.SHUT_RDWR)
	sockets[0].close()
	stdscr.erase()
	#stdscr.refresh()
	del stdscr

if __name__ == "__main__":
	curses.wrapper(main)
