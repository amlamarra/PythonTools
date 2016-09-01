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
	
def listen(stdscr):
	while True:
		messages = sockets[0].recv(4096).decode(UTF)
		if messages.split(" ")[0] == "PING":
			pong = messages[0] + "O" + messages[2:]
			sockets[0].sendall(pong.encode(UTF))
			output(stdscr, pong)
		messages = messages.split("\r\n")
		for message in messages:
			if message != "":
				output(stdscr, message)

def main(stdscr):
	send = True
	inchannel = False
	channel = ""
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
			
			if c in (13, 10): # \r or \n
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
			elif c in PRINTABLE:
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
			msg = msg[1:]
			params = len(msg.split(" ")) - 1
			command = msg.split(" ")[0].upper()
			if command == "JOIN" and params > 0:
				if msg.split(" ")[1][0] == "#":
					channel = msg.split(" ")[1]
					msg = "JOIN {}".format(channel)
					inchannel = True
				else:
					send = False
			elif command == "NICK" and params > 0:
				msg = "NICK {}".format(msg.split(" ")[1])
			elif command == "PART" and inchannel == True:
				msg = "PART {}".format(channel)
				inchannel = False
			elif command == "QUIT":
				sockets[0].sendall("QUIT\r\n".encode(UTF))
				break
		elif msg and msg[0] == "/" and len(msg) <= 1:
			send = False
		elif msg:
			if inchannel == True:
				msg = "PRIVMSG {} :{}\r\n".format(channel, msg)
		
		if send == True and msg:
			msg += "\r\n"
			sockets[0].sendall(msg.encode(UTF))
		elif send == False and msg:
			output(stdscr, "Invalid command or parameter...")
			send = True	# Reset the send flag
	
	sockets[0].shutdown(socket.SHUT_RDWR)
	sockets[0].close()
	stdscr.erase()
	#stdscr.refresh()
	del stdscr

if __name__ == "__main__":
	curses.wrapper(main)
