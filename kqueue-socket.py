#!/usr/bin/env python
import socket, select

HOST = 'localhost'
PORT = 5000
ADDR = (HOST, PORT)


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(ADDR)
serversocket.listen(1)
serversocket.setblocking(0)

kqueue = select.kqueue()
kevents = [select.kevent(serversocket.fileno(), filter=select.KQ_FILTER_READ, flags=select.KQ_EV_ADD|select.KQ_EV_ENABLE), ]

try:
    connections = {}; adds={}
    while True:
        events = kqueue.control(kevents, 1)
        if events:
            for event in events:
                if event.ident == serversocket.fileno():
                    connection, address = serversocket.accept()
                    print "...connect from ", address
                    connection.setblocking(0)
                    connections[connection.fileno()] = connection
                    adds[connection.fileno()]=address
                    kevents.append(select.kevent(connections[connection.fileno()].fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD, udata=connection.fileno()))
                elif event.udata in connections:
                    print event.udata
                    data = connections[event.udata].recv(1024)
                    if data.startswith('\n'):
                        kevents.remove(select.kevent(connections[event.udata].fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD, udata=event.udata))
                        print "...close connection from", adds[event.udata]
                        del connections[event.udata]
                        del adds[event.udata]
                    else:
                        connections[event.udata].send(data)
finally:
    kqueue.close()
    serversocket.close()
