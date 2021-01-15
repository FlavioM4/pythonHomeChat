import socket
import threading


nickname = input("Choose your nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.20', 55555))

# Listening to Server and Sending Nickname
def receive():
	while True:
		try:
			# Receive Message From Server
			# If 'NICK' Send Nickname
			message = client.recv(1024).decode('ascii')
			if message == 'NICK':
				client.send(nickname.encode('ascii'))
			else:
				print(message)
		except:
			# Close Connection When Error
			print("An error has occured!")
			client.close()
			break

# Sending messages to server
def write():
	while True:
		message = '{}: {}'.format(nickname, input(''))
		client.send(message.encode('ascii'))

# Starting threads
receive_thread = threading.Thread(target = receive)
receive_thread.start()
write_thread = threading.Thread(target = write)
write_thread.start()