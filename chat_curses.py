#!/usr/bin/python3
import socket, argparse, threading, curses
from string import printable

IP = "127.0.0.1"
PORT = 6665
sockets = []
PRINTABLE = list(map(ord, printable))
lines = []

####################### SERVER CODE #######################
def server_listen(sc, sname):
	while True:
		try:
			msg = sc.recv(1024).decode('utf-8')
		except Exception as ex:
			print(ex)
			break
		if msg == "":
			break
		for sock in sockets[1:]:
			if sock != sc:
				sock.sendall("{}:{} > {}".format(sname[0], sname[1], msg).encode('utf-8'))
		print("{}:{} > {}".format(sname[0], sname[1], msg))
	sockets.remove(sc)
	sc.close()
	print("[*] {} socket closed".format(sname))
	for sock in sockets[1:]:
		sock.sendall("[*] {} has left the conversation".format(sname).encode('utf-8'))

def server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((IP, PORT))
	s.listen(10)
	sockets.append(s)
	
	print("[*] Server is now listening for a connection...")
	while True:
		sc, sockname = s.accept()
		sockets.append(sc)
		print("[*] Connection accepted from {}".format(sockname))
		for sock in sockets[1:]:
			if sock != sc:
				sock.sendall("[*] ({}:{}) has joined the conversation.".format(sockname[0], sockname[1]).encode('utf-8'))
		t = threading.Thread(target=server_listen, args=(sc,sockname,))
		t.start()

####################### CLIENT CODE #######################
def client_print(stdscr, msg):
	max_lines = stdscr.getmaxyx()[0] - 3
	
	if len(lines) > max_lines:
		del lines[0]
		stdscr.clear()
		for i, line in enumerate(lines):
			stdscr.addstr(i, 0, line)

	stdscr.addstr(len(lines), 0, msg)
	lines.append(msg)
	
def client_listen(stdscr):
	while True:
		msg = sockets[0].recv(1024).decode('utf-8')
		Y, X = stdscr.getyx()
		if msg == "":
			break
		i = 0
		for letter in msg:
			if letter == ">":
				msg = msg[:i-1] + "\t" + msg[i:]
				break
			i += 1
		client_print(stdscr, msg)
		stdscr.move(Y, X)
		stdscr.refresh()

def client(stdscr):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP, PORT))
	sockets.append(s)
	t = threading.Thread(target=client_listen,args=(stdscr,))
	t.start()
	Ymax, Xmax = stdscr.getmaxyx()
	
	while True:
		stdscr.move(Ymax-1, 0)
		stdscr.clrtoeol()
		stdscr.addstr("> ")
		Y, X = stdscr.getyx()
		eol = X
		s = []
		
		while True:
			y, x = stdscr.getyx()
			c = stdscr.getch()
			
			if c in (13, 10): # \r or \n
				break
			elif c == curses.KEY_BACKSPACE:
				if x > X:
					eol -= 1
					del s[x-X-1]
					stdscr.move(y, x-1)
					stdscr.clrtoeol()
					stdscr.insstr("".join(s[x-X-1:]))
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
			elif c == curses.KEY_DC: # Delete
				if x < eol:
					eol -= 1
					del s[x-X]
					stdscr.clrtoeol()
					stdscr.insstr("".join(s[x-X:]))
			elif c in PRINTABLE:
				eol += 1
				if x < eol:
					s.insert(x-X, chr(c))
					stdscr.insch(c)
				else:
					s.append(chr(c))
					stdscr.addch(c)
				stdscr.move(y, (x+1))
		
		msg = "".join(s)
		if msg == "q":
			break
		sockets[0].sendall(msg.encode('utf-8'))
		msg = "Me\t\t> " + msg
		client_print(stdscr, msg)
	
	sockets[0].shutdown(socket.SHUT_RDWR)
	sockets[0].close()
	del stdscr

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="This is a simiple chat server/client")
	parser.add_argument('role', choices=["server", "client"], help="Run as server or client")
	args = parser.parse_args()

	if args.role == "server":
		server()
	elif args.role == "client":
		curses.wrapper(client)
