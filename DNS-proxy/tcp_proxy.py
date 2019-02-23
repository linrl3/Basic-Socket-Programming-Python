# !/usr/bin/env python

from socket import *
import struct
dns_port = 53
dns_query = 3154
google_host = "8.8.4.4"
srev_client = socket(AF_INET, SOCK_DGRAM)#rec
srev_server = socket(AF_INET, SOCK_DGRAM)#send
srev_client.bind(('',dns_port))
srev_server.bind(('',dns_query))
def forward_query(sock,data,host,port):
    sock.sendto(data,(host,port))
    flag = 0
    while not flag:
        new,fro = sock.recvfrom(1568)
        if new:
            flag = 1
    return new
def send_res(sock,data,add):
    sock.sendto(data,add)
def main():
    while True:
        print('Proxy is running.')
        data,addr = srev_client.recvfrom(1568)
        if data:
            print('get query from',addr)
            ans = forward_query(srev_server,data,google_host,dns_port)
            if ans:
                flag = ans[2:4]
                flag = ''.join(format(ord(x),'b') for x in flag)
                if flag[6]!='1':
                    print('Normal udp can handle.')
                    send_res(srev_client,ans,addr)
                else:
                    print('Swithing to tcp model.')
                    send_res(srev_client, ans, addr)
                    #srev_client.close()
                    #srev_server.close()
                    stcp_client = socket(AF_INET,SOCK_STREAM)#from client
                    stcp_server = socket(AF_INET,SOCK_STREAM)#with google server
                    stcp_client.bind(('',53))
                    stcp_client.listen(5)
                    try:
                        tcpsock, addr = stcp_client.accept()
                        print('waiting data')
                        tcpdata = tcpsock.recv(2048)
                        if tcpdata:
                            print('getting data')
                            stcp_server.connect(('8.8.8.8', 53))
                            stcp_server.send(tcpdata)
                            res = stcp_server.recv(4096)
                            print(res)
                            if res:
                                tcpsock.send(res)
                            stcp_client.close()
                    except:
                        continue

                    stcp_server.close()
    return 0
if __name__ == '__main__':
    main()



