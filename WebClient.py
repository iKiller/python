#**************************************************************
#    File Name: WebClient.py
#       Author: JiangTao
#       E-mail: jt_2010@hust.edu.cn
#  Description: WebClient.py
# Created Time: 2012/12/5 10:16:36
#**************************************************************
#import socket module
import sys
import socket
import string
serverHost = '127.0.0.1'
serverPort = 80
filename = 'hello.html'
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) > 1:
    serverHost = sys.argv[1]
if len(sys.argv) >2:
    serverPort = string.atoi(sys.argv[2], 10)
if len(sys.argv) >3:
    filename = sys.argv[3]

#Prepare a server socket
clientSocket.connect((serverHost, serverPort))
print "Connected to the server..."
data = 'GET /' + filename
clientSocket.sendall(data)
print "Send:", data
responce = clientSocket.recv(8192)
print "Received:", responce
clientSocket.close()
