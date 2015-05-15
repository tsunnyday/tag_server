import socket

def send_a_msg(conn, msg):
	length = len(msg)
	sent = 0
	while sent < length:
		sent += conn.send(msg[sent:])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1338))
server.listen(1)
print "LISTENING..."

messages = []

while 1:

	connection, address = server.accept()
	print "received a connection from " + str(address)
	send_a_msg(connection, "Welcome to the legendary tagged wall!  Anything you write here will be preserved forever.  Keep all messages under 64 characters though.\n")
	
	data = connection.recv(64)
	if data:
		print "Added:" + data
		messages.append(data)
		send_a_msg(connection, "Thanks, your words will be engraved here for all of eternity.\n  Look at your tag among everyone else's:\n")
		for message in messages:
			send_a_msg(connection, message + "\n")
	else:
		print "Client disconnected"
	connection.close()



print "shutting down"

