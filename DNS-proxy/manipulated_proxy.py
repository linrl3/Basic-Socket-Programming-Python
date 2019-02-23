#83is invalid
from socket import *
import struct
def changedata(data):
    print(data)
    da = list(data)
    index = len(data)
    da[2] = struct.pack('B',129)
    da[3] = struct.pack('B',128)
    da[7] = struct.pack('B', 1)#ans+1
    data = ''.join(da)
    data += struct.pack('B', 192)
    data += struct.pack('B', 12)
    data += struct.pack('B', 0)
    data += struct.pack('B', 1)
    data += struct.pack('B', 0)
    data += struct.pack('B', 1)
    data += struct.pack('B',0)
    data += struct.pack('B', 0)
    data += struct.pack('B', 1)
    data += struct.pack('B', 15)
    data += struct.pack('B', 0)
    data += struct.pack('B', 4)
    # hard code the fake addrss here
    data += struct.pack('B', 192)
    data += struct.pack('B', 168)
    data += struct.pack('B', 0)
    data += struct.pack('B', 191)
    print(data)
    return data
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
        new,fro = sock.recvfrom(4096)
        if new:
            flag = 1
    return new


def send_res(sock,data,add):
    sock.sendto(data,add)

def main():
    while True:
        print('Proxy is running')
        data,addr = srev_client.recvfrom(4096)
        if data:
            print('Get query from',addr)
            ans = forward_query(srev_server,data,google_host,dns_port)
            if ans:
                #tc = ord(ans[2])
                #valid = ord(ans[3])
                flag = ans[2:4]
                flag = ''.join(format(ord(x),'b') for x in flag)
                print flag
                if flag[-4:]!='0000':
                    print('Now we change to a fake answer.')
                    na = changedata(data)
                    send_res(srev_client, na, addr)
                elif flag[6]!='1':
                    print('Normal udp can hold')
                    send_res(srev_client,ans,addr)
                else:
                    print('Swithing to tcp model')
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
if __name__ == '__main__':
    main()




