#!/usr/bin/python3
import socket
import threading
import curses
import pickle
import os.path
from string import printable

class ServerInfo():
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.addr = (ip, port)

# Use a class for these & save to a file
NICK = "elusive" # Enter nick
USERNAME = "elusive" # Enter username
REALNAME = "Elusive Bear" # Enter real name

#PRINTABLE = list(map(ord, printable))
PRINTABLE = [ord(x) for x in printable]

sockets = []
servers = {}
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
    stdscr.move(Y, X)    # Move the cursor back to the start position
    stdscr.refresh()

# Displays the help listing
def help(stdscr):
    output(stdscr, "------------------------------------------------------------")
    output(stdscr, "List of commands (not case sensitive):")
    output(stdscr, "\t/SERVER (save|delete|list) [<name> <ip> <port>]")
    output(stdscr, "\t\tName, IP, and port are required if the save option is used")
    output(stdscr, "\t\tName is required if the delete option is used")
    output(stdscr, "\t/CONNECT <name> | Connect to the saved server")
    output(stdscr, "\t/DISCONNECT | Disconnect from the current server")
    output(stdscr, "\t/JOIN #<channel name> | Join a channel")
    output(stdscr, "\t/NICK <new nick> | Changes your nick")
    output(stdscr, "\t/NAMES [#<channel name>]")
    output(stdscr, "\t\tList all visible channels & users if no arguments are given")
    output(stdscr, "\t\tIf channel name is given, list all visible names in that channel")
    output(stdscr, "\t/QUIT | Closes the connection & exits the program")
    output(stdscr, "\t/EXIT | Same as /QUIT")
    output(stdscr, "\t/HELP | Display this help dialog")
    output(stdscr, "------------------------------------------------------------")
    output(stdscr, "While in a channel:")
    output(stdscr, "\t/NAMES | List all visible nicknames in the current channel")
    output(stdscr, "\t/PART [<part message>] | Leaves the current channel")
    output(stdscr, "\t/PRIVMSG <nick> :<message> | Send a private message to a user")
    output(stdscr, "------------------------------------------------------------")

# Listens for messages from the server
def listen(stdscr):
    while True:
        messages = sockets[0].recv(4096).decode().split("\r\n")
        for message in messages:
            if message != "": # Dismiss empty lines
                # Trim the fat
                message = message.split(" ")
                if message[0] != "PING" and message[1][0].isdigit():
                    message = " ".join(message[2:])
                elif message[0] != "PING":
                    message = " ".join(message[1:])
                else:
                    message = " ".join(message)
                output(stdscr, message)
                
                # Automatically reply to PING messages to prevent being disconnected
                if message.split(" ")[0] == "PING":
                    pong = "PONG" + message[4:]
                    sockets[0].sendall(pong.encode())
                    output(stdscr, pong)

def connect(stdscr, srv_addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect(srv_addr)
    except socket.error as exc:
        output(stdscr, "Connection error: {}".format(exc))
        return False
    
    sockets.append(sock)
    sockets[0].sendall("NICK {}\r\n".format(NICK).encode())
    sockets[0].sendall("USER {} 0 * :{}\r\n".format(USERNAME, REALNAME).encode())
    t = threading.Thread(target=listen,args=(stdscr,))
    t.daemon = True
    t.start()
    
    return True

def user_input(stdscr):
    global NICK
    send = True
    inchannel = False
    connected = False
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
            # Each line cannot exceed 512 characters in length, including \r\n
            elif c in PRINTABLE and len(txt) < 510:
                eol += 1
                if x < eol:
                    txt.insert(x-X, chr(c))
                    stdscr.insch(c)
                else:
                    txt.append(chr(c))
                    stdscr.addch(c)
                stdscr.move(y, (x+1))

        message = "".join(txt)
        output(stdscr, "{} > {}".format(NICK, message))

        if message and message[0] == "/" and len(message) > 1:
            param = ""
            text = ""
            msg = message[1:]
            params = len(msg.split(" ")) - 1

            if len(msg.split(":")) > 1:
                text = " :" + msg.split(":")[1]

            if params > 0:
                param = msg.split(" ")[1]

            command = msg.split(" ")[0].upper()

            if command == "SERVER" and params:
                if param.lower() == "list":
                    for server in servers:
                        output(stdscr, "Server Name: {}  |  Address: {}"
                               .format(server, servers[server].addr))
                elif param.lower() == "save" and params > 3:
                    name = msg.split(" ")[2]
                    ip = msg.split(" ")[3]
                    port = int(msg.split(" ")[4])
                    server = ServerInfo(name, ip, port)
                    servers[name] = server
                    # Now save to file
                    with open("servers.db", "wb") as f:
                        pickle.dump(servers, f)
                elif param.lower() == "save" and params < 4:
                    output(stdscr, "Saving a server requires 3 parameters:")
                    output(stdscr, "\t/SERVER save <server name> <ip> <port>")
                elif param.lower() == "delete" and params > 1:
                    name = msg.split(" ")[2]
                    if name in servers:
                        del servers[name]
                        with open("servers.db", "wb") as f:
                            pickle.dump(servers, f)
                        output(stdscr, "Server '{}' has been deleted."
                               .format(name))
                    else:
                        output(stdscr, "Server name does not exist.")
                elif param.lower() == "delete" and params < 2:
                    output(stdscr, "Specify the server name to delete it.")
                send = False
            elif command == "CONNECT":
                if params and param in servers:
                    connected = connect(stdscr, servers[param].addr)
                    if not connected:
                        output(stdscr, "Unable to connect to the server")
                elif param not in servers:
                    output(stdscr, "Must specify the name of a saved server")
                send = False
            elif command == "JOIN" and params:
                send = False
                if param[0] == "#" and connected:
                    channel = param
                    msg = "JOIN {}".format(channel)
                    inchannel = True
                    send = True
                elif connected:
                    output(stdscr, "Improper channel name")
                else:
                    output(stdscr, "You must be connected to a server.")
            elif command == "NICK" and params:
                msg = "NICK {}".format(param)
                NICK = param
            elif command == "PART" and inchannel == True:
                msg = "PART {}{}".format(channel, text)
                inchannel = False
            elif command == "NAMES":
                if inchannel and not params:
                    msg = "NAMES {}".format(channel)
                elif params and param[0] == "#":
                    msg = "NAMES {}".format(param)
                else:
                    send = False
                    output(stdscr, "You must specify a channel name " \
                                   "if you're not in one")
            elif command == "HELP":
                help(stdscr)
                send = False
            elif command == "QUIT":
                if sockets:
                    sockets[0].sendall("QUIT\r\n".encode())
                break
            elif command == "EXIT":
                if sockets:
                    sockets[0].sendall("QUIT\r\n".encode())
                break
            elif command == "PRIVMSG" and params > 1:
                msg = msg.split(" ")
                text = msg[2:]
                text = " ".join(text)
                if text[0] == ":":
                    text = text[1:]
                msg = "PRIVMSG {} :{}".format(param, text)
            else:
                send = False
                output(stdscr, "Invalid command or parameter...")

        elif message and message[0] == "/" and len(message) == 1:
            send = False
            output(stdscr, "Invalid command")
        elif message and inchannel == True:
            msg = "PRIVMSG {} :{}".format(channel, message)
        elif message and inchannel == False:
            output(stdscr, "You need to be in a channel to send a message")
            send = False

        if send and message:
            msg += "\r\n"
            sockets[0].sendall(msg.encode())

        send = True # Reset the send flag

def main(stdscr):
    global servers
    # Display the help dialog first
    help(stdscr)
    
    if os.path.isfile("servers.db"):
        with open("servers.db", "rb") as f:
            servers = pickle.load(f)

    user_input(stdscr)
    
    if sockets:
        sockets[0].shutdown(socket.SHUT_RDWR)
        sockets[0].close()
    stdscr.erase()
    stdscr.refresh()
    del stdscr

if __name__ == "__main__":
    curses.wrapper(main)

'''
Features to add:
    - Color! (colorama module?)
    - Menus & such
    - List users in the channel on the right
    - Command buffer
'''
