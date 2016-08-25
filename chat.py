#!/usr/bin/python3
# A simple chat server/client

import socket, argparse, threading, curses

IP = "127.0.0.1"
PORT = 6665
sockets = []

def server_listen(sc, sname):
	msg = "0"
	while True:
		try:
			msg = sc.recv(1024).decode('utf-8')
		except Exception as ex:
			print(ex)
			break
		if msg == "exit" or msg == "":
			break
		for sock in sockets:
			if sock != sockets[0]:
				sock.sendall("{}:{} > {}".format(sname[0], sname[1], msg).encode('utf-8'))
		print("{}:{} > {}".format(sname[0], sname[1], msg))
	sockets.remove(sc)
	sc.close()
	print("{} socket closed".format(sname))

def server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((IP, PORT))
	s.listen(10)
	sockets.append(s)
	
	print("Server is now listening for a connection...")
	while True:
		sc, sockname = s.accept()
		sockets.append(sc)
		print("Connection accepted from {}".format(sockname))
		t = threading.Thread(target=server_listen, args=(sc,sockname,))
		t.start()

def client_listen():
	while True:
		srv_msg = sockets[0].recv(1024).decode('utf-8')
		if srv_msg == "":
			break
		print("\r{}\n> ".format(srv_msg), end="")

#def client_send(sock):

def client():
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP, PORT))
	sockets.append(s)
	t = threading.Thread(target=client_listen)
	t.start()
	msg = ""
	print("> ", end="")
	while msg != "exit":
		msg = input()
		sockets[0].sendall(msg.encode('utf-8'))
	sockets[0].close()

if __name__ == "__main__":
	#choice = {"server":server, "client":client}
	parser = argparse.ArgumentParser(description="This is a simiple chat server/client")
	#parser.add_argument('role', choices=choice, help="Client or Server")
	parser.add_argument('role', choices=["server", "client"], help="Run as server or client")
	args = parser.parse_args()
	#choice[args.role]()
	if args.role == "server":
		server()
	elif args.role == "client":
		curses.wrapper(client)
