#echo_client.py

import socket
import sys
from format import input_format

host = socket.gethostname()

port = 8080
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))
"""
s = socket.create_connection(("127.0.0.1", port))
###

#test
if len(sys.argv) < 2 :
	print("No enough parameter")
	sys.exit(1)
#data = sys.argv[1]
data = input_format(sys.argv[1:])
data = data.encode()
print data
#test
s.sendall(data)
#s.sendall(b'Hello, world')
data = s.recv(1024).split('\n')
#data = data.decode()
s.close()

#print('Received ', repr(data))
print('Retrive results : \n')
for line in data:
	print(line)