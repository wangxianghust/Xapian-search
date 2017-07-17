#echo_client.py

import socket

host = socket.gethostname()

port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

s.sendall(b'Hello, world')
data = s.recv(1024)
s.close()

print('Received ', repr(data))
