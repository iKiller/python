#**************************************************************
#    File Name: WebServer.py
#       Author: JiangTao
#       E-mail: jt_2010@hust.edu.cn
#  Description: WebServer.py
# Created Time: 2012/12/4 23:29:45
#**************************************************************/
#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverSocket.bind(('',8000))
serverSocket.listen(5)
print("The server socket is ready...")
while True:
    #Establish the connection
    print 'Ready to serve...'
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(8192)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.readlines(-1)
        #Send one HTTP header line into socket
        
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send('404 Not found')
        #Close client socket
        connectionSocket.close()
serverSocket.close()
