import socket

s = socket.socket()
port = 0

s.connect(("api.logentries.com", port))
print 'Receiving..'
data = s.recv(1024)
print 'Finished Receiving..'
s.close()
print 'Received', repr(data)