import socket  
import sys
import csv
import time

class SockClient:

	def __init__(self, socketType, host, port, msg, delay): #konsturktor
		self.socketType = socketType
		self.host = host
		self.port = port
		self.msg = msg
		self.delay = float(delay) / 1000
		
		self.dataSend()
		self.dataRecieve()
		self.close()

	def dataSend(self):
		time.sleep(self.delay)

		if self.socketType.lower() == "tcp":
			self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.clientSocket.connect((self.host, int(self.port)))
			self.clientSocket.send(self.msg.encode())
			
		elif self.socketType.lower() == "udp":
			self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.clientSocket.sendto(self.msg.encode(),(self.host, int(self.port)))
			
	def dataRecieve(self):
		print (self.clientSocket.recv(1024).decode())
	
	def close(self):
		self.clientSocket.close

class InputData: 
	def __init__(self):
		self.importFile =  open("testValues.csv", "r")
		self.importValues = csv.reader(self.importFile)
		self.valueArray = []

		for row in self.importValues:
			self.valueArray.append(row)

	def tryConnect(self):
		for item in self.valueArray:
			num= item[0]
			host = item[1]
			port = item[2]
			protocol = item[3]
			time = item[4]
			msg = item[5]

			if not(num == '#'):
				socketSend = SockClient(protocol, host, port, msg, time)

	def fileClose(self):
		self.importFile.close()


file1 = InputData()
file1.tryConnect()
file1.fileClose()
