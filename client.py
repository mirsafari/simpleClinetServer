import socket  
import sys

class SockClient:
	
	def __init__(self, socketType, port, msg ): #konsturktor
		self.socketType = socketType
		self.port = port
		self.msg = msg
		host = socket.gethostname()
		if socketType == "tcp":
			self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.clientSocket.connect((host, port))
			self.clientSocket.send(msg.encode())

		elif socketType == "udp":
			self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.clientSocket.sendto(msg.encode(),(host, port))
	
	def dataRecieve(self):
		return self.clientSocket.recv(1024).decode()
	
	def close(self):
		self.clientSocket.close

def inputVariables():
	socketType = input ("Type TCP or UDP to choose connection type: ").lower()
	if not(socketType == "tcp" or socketType == "udp") :
		sys.exit("Wrong input! Enter TCP or UDP")

	port = int(input ("Port number (between 1 and 65535): "))
	if not ((port > 0) and (port < 65534)):
		sys.exit("Wrong input! Enter a number between 1 and 65535")

	msg = input("Input message: ")

	return socketType, port, msg

socketInfo = inputVariables()

socketA = SockClient(socketInfo[0],socketInfo[1],socketInfo[2])
print(socketA.dataRecieve())
socketA.close()