import socket # network connection
import threading # multiple tasks

# Connection
host = '192.168.1.20'
port = 55555

# Starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists for clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages To All Connected Clients
def broadcast(message):
	for client in clients:
		client.send(message)


#Handling Messages from Clients
def handle(client):
	while True:
		try:
			# Broadcasting Mesage
			message = client.recv(1024)
			broadcast(message)
		except:
			# Removing and Closing Clients
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			broadcast('{} left!'.format(nickname).encode('ascii'))
			nicknames.remove(nickname)
			break


# Receiving / Listening function

def receive():
	while True:
		# Accept connection
		client, address = server.accept()
		print("Connected with {}".format(str(address)))

		#Request and store nickname
		client.send('NICK'.encode('ascii'))
		nickname = client.recv(1024).decode('ascii')
		nicknames.append(nickname)
		clients.append(client)

		#Print and broadcast nickname
		print("Nickname is {}".format(nickname))
		broadcast("{} has joined the chat!".format(nickname).encode('ascii'))
		client.send("Connected to a server!".encode('ascii'))

		#Start handling thread for client
		thread = threading.Thread(target = handle, args=(client,))
		thread.start()

receive()