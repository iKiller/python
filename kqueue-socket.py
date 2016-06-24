#!/usr/bin/env python
import socket, select

HOST = 'localhost'
PORT = 5000
ADDR = (HOST, PORT)

EOL1 = '\n'
EOL2 = '\n\r'
response = 'Hello, world!'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(ADDR)
serversocket.listen(1)
serversocket.setblocking(0)

kqueue = select.kqueue()
kevents = [select.kevent(serversocket.fileno(), filter=select.KQ_FILTER_READ, flags=select.KQ_EV_ADD|select.KQ_EV_ENABLE), ]

try:
    connections = {}; requests = {}; responses = {}
    while True:
        events = kqueue.control(kevents, 1)
        for event in events:
            if event.ident == serversocket.fileno():
                connection, address = serversocket.accept()
                print "...connect from ", address
                connection.setblocking(0)
                connections[connection.fileno()] = connection
                requests[connection.fileno()] = ''
                responses[connection.fileno()] = response
                kevents.append(select.kevent(connections[connection.fileno()].fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD, udata=connection.fileno()))
            else
                requests[event.udata] = connections[event.udata].recv(1024)
                print('-'*40 + '\n' + requests[event.udata])
                connections[event.udata].send(responses[event.udata])
                kevents.remove(select.kevent(connections[event.udata].fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD, udata=event.udata))
                connections[event.udata].shutdown(socket.SHUT_RDWR)
                connections[event.udata].close()
                print "...close connection from", address
                del connections[event.udata]
                del requests[event.udata]
                del responses[event.udata]
finally:
    kqueue.close()
    serversocket.close()
