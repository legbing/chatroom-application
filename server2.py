# Python program to implement server side of chat room.
import socket
import select


from _thread import *

users = {
'ABC': 'abc',
'DEF': '123',
'XYZ': 'xyz',
'GHI': '456',
'PQR': '789'}
counts = {'ABC':1, 'DEF':1, 'XYZ':1,'GHI':1,'PQR':1}

chatrooms = dict()
IP_address=input("enter the ip address: ")
Port=3456

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP_address, Port))
server.listen(100)

				
passwords = dict()
def broadcast(message, connection,list_of_clients):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(message.encode())
			except:
				clients.close()
				remove(clients)
def clientthread(conn, addr,list_of_clients, username):
	
	while True:
		try:
			message = conn.recv(2048).decode()
			
			if message:
				print ("<" + addr[0] + "> " + message)
				message_to_send = "<" + addr[0] + "> " + message
				broadcast(message_to_send, conn,list_of_clients)
				
			else:
				counts[username] = 1
				remove(conn)
				
		except:
			continue

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)
while True:
	
		conn, addr = server.accept()
		data=conn.recvmsg(2048)
		#print(data)
		data = data[0].decode().split('\n')
		#print(data)
		username = data[0]
		password = data[1]

		if(username in users.keys() and password == users[username] and counts[username]>0):
			#conn.send("Authorisation successful!".encode())
			conn.send(("Do you want to create a chatroom?").encode())
			answer = conn.recv(1024)
			if(answer.decode() == "yes"):
				conn.send("Enter the name of chatroom and authentication code: ".encode())
				data = conn.recvmsg(2048)
				data = data[0].decode().split('\n')
				chatrooms[data[0]] = list()
				passwords[data[0]] = data[1]
				chatrooms[data[0]].append(conn)
				conn.send("Chatroom created successfully! ".encode())
				print (addr[0] + " connected")
				counts[username] = 0
				msg = "Welcome to this chatroom!"
				conn.send(msg.encode())
				start_new_thread(clientthread,(conn,addr,chatrooms[data[0]], username))
				
			else:
				if(len(chatrooms.keys())==0):
					conn.send("oops..there are no chatrooms to join\n".encode())
				else:
					conn.send(("Enter the name and authentication code of the chatroom you want to join: "+('\n'.join(chatrooms.keys()))).encode())
					data = conn.recvmsg(2048)
					data = data[0].decode().split('\n')
					if(passwords[data[0]] == data[1]):
						chatrooms[data[0]].append(conn)
						print (addr[0] + " connected")
						msg = "Welcome to this chatroom!"
						conn.send(msg.encode())
						counts[username] = 0
						start_new_thread(clientthread,(conn,addr,chatrooms[data[0]], username))
					else:
						msg = "Authentication failed\n"
						conn.send(msg.encode())
			
		else:
			msg = "Authorisation failed\n"
			conn.send(msg.encode())
			
	 
		


