import socket
import select
import sys
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

print("Enter the username ")
name=input()
print("Enter the password ")
pasw=input()

server.sendmsg([name.encode(), '\n'.encode(), pasw.encode()])
message = server.recv(1024)
if(message.decode() == "Authorisation failed\n"):
	print(message.decode())
	server.close()
#
else:
	#print("hii")
	print(message.decode())
	#print(server.recv(2048).decode())
	answer = input().encode()
	server.send(answer)
	msg=server.recv(2048).decode()
	print(msg)
	if(msg=="oops..there are no chatrooms to join\n"):
		server.close()
		exit(0)	
	name = input()
	code = input()
	server.sendmsg([name.encode(), '\n'.encode(), code.encode()])
	
	message = server.recv(2048)
	if(message.decode() == "Authentication failed\n"):
		print(message.decode())
		server.close()
		
	else:	
		
		#message = server.recv(2048)
		print(message.decode())
		while True:
		 
			# maintains a list of possible input streams
			sockets_list = [sys.stdin, server]
		 
			
			read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
		 
			for socks in read_sockets:
				if socks == server:
					message = socks.recv(2048)
					print (message.decode())
				    
				else:
					message = sys.stdin.readline()
					if(message == "FSEND\n"):
						server.send("FS".encode())
						filename = input("Enter filename: ")
						f = open(filename, 'rb')
						l = f.read(1024)
						while l:
							server.send(l)
							l = f.read(1024)
						f.close()
						server.send(b"DONE")
						sys.stdout.write("<You>")
						sys.stdout.write("Successfully sent file")
						sys.stdout.flush()
					else:
						server.send(message.encode())
						sys.stdout.write("<You>")
						sys.stdout.write(message)
						sys.stdout.flush()
		server.close()
