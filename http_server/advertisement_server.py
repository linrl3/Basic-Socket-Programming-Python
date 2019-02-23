from socket import *
import struct
import sys
import os
def generate_html(getmessage):
    text = '<html><head><a>'+'You may want to visit '+getmessage+'. While we suggest browsing www.amazon.com. '+'</a></body></html>'
    return text
serverSocket = socket(AF_INET, SOCK_STREAM)
header = 'HTTP/1.1 200 OK\r\n'
serverSocket.bind(('', 80))
serverSocket.listen(5)
def main():
    while True:
        print('Server is ready...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024)
            message = message.decode()
            if len(message) > 1:
                data = message.split()
            else:
                sys.exit(1)
            print(message)
            start=message.find('Host')
            end=message.find('Connection')
            hostname=message[start+5:end-2]
            # re to obtain the get message in query
            html = generate_html(hostname)
            connectionSocket.send(header.encode())
            connectionSocket.send('Content-Type:text/html\r\n'.encode())
            connectionSocket.send('\r\n'.encode())
            connectionSocket.send(html.encode())
            connectionSocket.send('\r\n'.encode())
            connectionSocket.close()
            
        except:
            print('')
    serverSocket.close()
if __name__ == '__main__':
    main()



