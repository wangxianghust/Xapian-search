#echo_client.py

import socket
import sys
from format import input_format

HOST = '127.0.0.1'
PORT = 8080
ADDR = (HOST, PORT)
BUF_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

while 1:
	inp = input("Client-Please enter the statment: ")
	if len(inp) < 2 :
		print("No enough parameter")
		sys.exit(1)

	data = input_format(inp)
	print data
	client.sendall(data)
	res = client.recv(1024).split('\n')
	print('Retrive results:')
	for line in res:
		print(line)

client.close()