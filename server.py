import socket
import datetime
import _thread
import logging

logging.basicConfig(filename='example.log',level=logging.INFO)

class MyServer():
	def __init__(self):
		self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def tcpConn (self):
		host = socket.gethostname()
		port = 12345                
		self.tcpSocket.bind((host, port))
		
		self.tcpSocket.listen(5)
		print("Lisening TCP...")

		while True:
			client, address = self.tcpSocket.accept()
			print ("Got new TCP connection from: ", address)
			client.send(("Thank you for connecting!").encode())

			data = client.recv(1024).decode()
			self.logging("TCP", data, address)
			client.close()

	def udpConn	(self):
		host = socket.gethostname()
		port = 12345                
		self.udpSocket.bind((host, port))
		print("Waiting for UDP...")
		while True:
			msg, address = self.udpSocket.recvfrom(1024)
			
			print ("Got new UDP message from: ", address)
			self.udpSocket.sendto("Thank your for sending!".encode(), address)
			self.logging("UDP", msg.decode(), address)

	def logging (self, connType, data, address):
		self.connType = connType
		self.data = data
		self.address = address
		logging.info(str(datetime.datetime.now())+ "|" + str(connType) + "| MSG: " + str(data) + " | FROM: " +str(address))

newServer = MyServer()
try:
	_thread.start_new_thread( newServer.tcpConn,())	
	_thread.start_new_thread( newServer.udpConn,())
except:
	print ("Error: unable to start thread")
while 1:
	pass