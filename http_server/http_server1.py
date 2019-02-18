# Import socket module
from socket import *
import sys
import os


if len(sys.argv)>1:
    port = sys.argv[1]
port=int(port)
def server1(port):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    #Prepare a sever socket
    #Fill in start
    serverPort = port
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)
    #Fill in end
    Correctstatus = 'HTTP/1.1 200 OK\r\n'
    Errorstatus404 = 'HTTP/1.1 404 Not Found\r\n\r\n'
    Errorstatus403 = 'HTTP/1.1 403 Forbidden\r\n\r\n'
    while True:
        print('Server is ready now...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024)
            message = message.decode()
            if len(message)>1:
                filename = message.split()[1]
                filename=filename[1:]
            else:
                sys.exit(1)
            #check if the file end with html or htm
            findhtml=filename.find(".html")
            findhtm=filename.find(".htm")
            if os.path.isfile(filename)==0:
                #file not exist
                connectionSocket.send(Errorstatus404.encode())
                body = "<html><head><title>" + Errorstatus404 + "</title></head><body><h1>" + Errorstatus404 + "</h1></body></html>"
                connectionSocket.send(body.encode())
                connectionSocket.send('\r\n'.encode())
            elif (findhtml==-1|findhtm==-1):
                #file not end with html or htm
                connectionSocket.send(Errorstatus403.encode())
                print filename+" cannot access"
                body = "<html><head><title>" + Errorstatus403 + "</title></head><body><h1>" + Errorstatus403 + "</h1></body></html>"
                connectionSocket.send(body.encode())
                connectionSocket.send('\r\n'.encode())
            else:
                #file exist and end with html or hml
                f = open(filename)
                outputdata = f.read()
                connectionSocket.send(Correctstatus.encode())
                connectionSocket.send('Content-Type:text/html\r\n'.encode())
                connectionSocket.send('\r\n'.encode())
                for i in range(0, len(outputdata)):
                    connectionSocket.send(outputdata[i].encode())
                connectionSocket.send('\r\n'.encode())
                connectionSocket.close()
        except:
            print ''
    serverSocket.close()

server1(port)
