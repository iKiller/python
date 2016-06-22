#!/usr/bin/env python
import socket, select

HOST = 'localhost'
PORT = 5000
ADDR = (HOST, PORT)

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response= b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += b'Hello, world!'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(ADDR)
serversocket.listen(1)
serversocket.setblocking(0)

kqueue = select.kqueue()
kevents = [select.kevent(serversocket.fileno(), filter=select.KQ_FILTER_READ, flags=select.KQ_EV_ADD|select.KQ_EV_ENABLE), ]
index=1

try:
    connections = {}; requests = {}; responses = {}
    while True:
        events = kqueue.control(kevents, 0)
        for event in events:
            if event.ident == serversocket.fileno():
                connection, address = serversocket.accept()
                print ("...connect from " + address)
                connection.setblocking(0)
                connections[index] = connection
                requests[index] = b''
                responses[index] = response
                kevents.append(select.kevent(connections[index].fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD, udata=index))
                index += 1
            elif event.udata >= 1 and event.filter == select.KQ_FILTER_READ and event.flags == select.KQ_EV_ADD:
                requests[event.udata] += connections[event.udata].recv(1024)
                if EOL1 in requests[event.udata] or EOL2 in requests[event.udata]:
                    kevents.remove(select.kevent(connections[event.udata].fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD, udata=event.udata))
                    kevents.append(select.kevent(connections[event.udata].fileno(), select.KQ_FILTER_WRITE, select.KQ_EV_ADD, udata=event.udata))
                    print('-'*40 + '\n' + requests[event.udata].decode()[:-2])
            elif event.udata >= 1 and event.filter == select.KQ_FILTER_WRITE and event.flags == select.KQ_EV_ADD:
                byteswritten = connections[event.udata].send(responses[event.udata])
                responses[event.udata] = responses[event.udata][byteswritten:]
                if len(responses[event.udata]) == 0:
                    kevents.remove(select.kevent(connections[event.udata].fileno(), select.KQ_FILTER_WRITE, select.KQ_EV_ADD, udata=event.udata))
                    connections[event.udata].shutdown(socket.SHUT_RDWR)
                    connections[event.udata].close()
                del connections[event.udata]
                del requests[event.udata]
                del responses[event.udata]
                index -= 1
finally:
    kqueue.close()
    serversocket.close()
