import socket  
import csv
from threading import Thread
import logging
import time
import datetime
import sys

class SockClient(Thread):

	def __init__(self, host, port, socketType, delay, msg):
		self.host = host
		self.port = port
		self.socketType = socketType
		self.msg = msg
		self.delay = float(delay) / 1000

	def msgSend(self):
		time.sleep(self.delay)
		#if TCP
		if self.socketType.lower() == "tcp":
			self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.clientSocket.connect((self.host, int(self.port)))
			#if txt
			if type(self.msg) is str:
				self.clientSocket.send(self.msg.encode())
				self.dataLog("SEND", self.msg)
			#if file
			else:
				dataBuffer = self.msg.read(1024)
				while (dataBuffer):
					print ("Sending...")
					self.clientSocket.send(dataBuffer)
					dataBuffer = self.msg.read(1024)

				print ("Done sending")
				self.clientSocket.shutdown(socket.SHUT_WR)
				self.msg.close()
				self.dataLog("SENT", "File was sent!")
				
		#if UDP
		elif self.socketType.lower() == "udp":
			self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			#if txt
			if type(self.msg) is str:
				self.clientSocket.sendto(self.msg.encode(),(self.host, int(self.port)))
				self.dataLog("SENT", self.msg)
			#if file
			else:
				dataBuffer = self.msg.read(1024)
				while (dataBuffer):
					print ("Sending...")
					self.clientSocket.sendto(dataBuffer,(self.host, int(self.port)))
					dataBuffer = self.msg.read(1024)

				print ("Done sending")
				self.clientSocket.shutdown(socket.SHUT_WR)
				self.msg.close()
				self.dataLog("SENT", "File was sent!")

	def msgRecieve(self):
		repaly = self.clientSocket.recv(1024).decode()
		print(repaly)
		self.clientSocket.close()
		self.dataLog("RECIEVED", repaly)

	def dataLog (self, direction, msg):
		self.direction = direction
		self.msg = msg

		logging.info(str(datetime.datetime.now())+ "|" + str(self.socketType) + "| MSG: " + str(self.msg) + " | FROM: " + str(self.host) + "| " + str(self.direction))

def inputData():
	#inputVariablesFile = input("Enter input file (messages and destinations)  name: ") 
	#outputLogFile =  input("Enter output file (log) name: ") 		

	inputVariablesFile = "testValues"
	outputLogFile = "clientLogTest"

	logging.basicConfig(filename=str(outputLogFile) + ".log",level=logging.INFO)

	importFile =  open(str(inputVariablesFile) + ".csv", "r")
	importValues = csv.reader(importFile)
	valueArray = []

	for row in importValues:
		valueArray.append(row)
	importFile.close()
	
	return valueArray

def checkString(sendMsg):
	msgLen = len(sendMsg) - 1
	if (sendMsg[0] is 'f') and (sendMsg[1] is '"') and (sendMsg[msgLen] is '"'):
		fileName = sendMsg[2:-1]
		f = open(fileName, "rb")
		return f

def Main():
	dataArray = inputData()

	for item in dataArray[1:]:
		isFile = checkString(item[5])
		if isFile:
			print("sendFile")
			socketTry = SockClient(item[1], item[2], item[3], item[4], isFile) #host/port/protocol/delayTime/msg

		else:
			#normalSend
			socketTry = SockClient(item[1], item[2], item[3], item[4], item[5]) #host/port/protocol/delayTime/msg

		try:
			threadSend = Thread(target=socketTry.msgSend, args=())
			threadRecv = Thread(target=socketTry.msgRecieve, args=())

			threadSend.start()
			threadSend.join()
			threadRecv.start()
			threadRecv.join()
		except Exception as e:
			print (e)
Main()