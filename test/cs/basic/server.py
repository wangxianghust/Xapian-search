#echo_server.py
import socket

host = ''
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

s.listen(1)

conn, addr = s.accept()

print('Connected by', addr)

while True:
    #data is a string received from socket.
    data = conn.recv(1024)
    if not data:break
    data = '%s%s' % (data, ' handled by server')
    conn.sendall(data)
conn.close()

