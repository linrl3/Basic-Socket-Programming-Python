# !/usr/bin/env python

from socket import *
import struct
dns_port = 53
dns_query = 3333
google_host = "8.8.4.4"#upstream resolver
srev_client = socket(AF_INET, SOCK_DGRAM)#socket for client who look up a domain
srev_server = socket(AF_INET, SOCK_DGRAM)#socket for proxy server
srev_client.bind(('',dns_port))
srev_server.bind(('',dns_query))
def forward_query(sock,data,host,port):
    #send to upstream like google
    sock.sendto(data,(host,port))
    flag = 0
    while not flag:
        new,frmo = sock.recvfrom(4096)
        if new:
            flag = 1
    return new
def send_res(sock,data,add):
    #send answer to the client
    sock.sendto(data,add)
def main():
    print 'Proxy is running.'
    while True:
        data,addr = srev_client.recvfrom(4096)
        if data:
            print('get query from',addr)
            ans = forward_query(srev_server,data,google_host,dns_port)
            if ans:
                send_res(srev_client,ans,addr)
    return 0
if __name__ == '__main__':
    main()
