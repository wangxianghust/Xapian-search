#server.py

import socket

port = 8080
s = socket.socket()
host = socket.gethostname()
s.bind((host, port))
s.listen(5)

print 'Server listening'

while True:
    conn, addr = s.accept()
    print 'Got connection from', addr
    data = conn.recv(1024)
    print('Server received', repr(data))

    filename = 'search1.py'
    f = open(filename, 'rb')
    line = f.read(1024)
    while(line):
        conn.send(line)
        print('Sent ', repr(line))
        line = f.read(1024)
    f.close()

    print('Done sending')
    conn.send('Thank you for connecting')
conn.close()