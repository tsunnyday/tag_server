import socket, select, Queue

def send_a_msg(conn, msg):
	length = len(msg)
	sent = 0
	while sent < length:
		sent += conn.send(msg[sent:])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 1337))
server.listen(1)
print "LISTENING..."

messages = []
inputs = [server]
outputs = []

message_queues = {}  #socket:queue


while inputs:
	
	readable, writable, exceptional = select.select(inputs, outputs, inputs)
	for s in readable:
		if s is server:
			connection, address = server.accept()
			print "received a connection from " + str(address)
			connection.setblocking(0)
			inputs.append(connection)
			message_queues[connection] = Queue.Queue()
			message_queues[connection].put("Welcome to the legendary tagged wall!  Anything you write here will be preserved forever.  Keep all messages under 64 characters though.\n")
			if connection not in outputs:
					outputs.append(connection)
		else:
			data = s.recv(64)
			if data:
				print "Added:" + data
				messages.append(data)
				message_queues[s].put("Thanks, your words will be engraved here for all of eternity.\n  Look at your tag among everyone else's:\n")
				for message in messages:
					message_queues[s].put(message + "\n")
				if s not in outputs:
					outputs.append(s)
			else:
				print "Client disconnected"
				if s in outputs:
					outputs.remove(s)
				inputs.remove(s)
				s.close()
				del message_queues[s]
	for s in writable:
		if not message_queues[s].empty():
			next_msg = message_queues[s].get_nowait()
			sent = s.send(next_msg)
			print "Sent %d out of %d bytes of message" %(sent, len(next_msg))
		else:
			outputs.remove(s)
	for s in exceptional:
		inputs.remove(s)
		if s in outputs:
			outputs.remove(s)
		s.close()
		del message_queues[s]
		
	
				



print "shutting down"

