import socket
import numpy
import re
import sys
import os

#if len(sys.argv)>1:
    #url = sys.argv[1]
#url = 'http://portquiz.net:8080/'




#url='http://airbedandbreakfast.com/'
#url='http://stevetarzia.com/index.php'
#url='http://thefacebook.com'
#url = 'http://portquiz.net:8080 '

if len(sys.argv)>1:
    url = sys.argv[1]
redir_count=0
def http_client(url):
    print 'input url is'+url
    url=url.strip()
    if url[0:8] == 'https://':
        print('this is a https url not a http one')
        sys.exit(1)
        url = url[8:]
    if url[0:7] == 'http://':
        url = url[7:]
    else:
        sys.exit(1)
    if url[-1] != '/':
        url += '/'
    HOST = re.search(r'.*?/', url).group()
    REQ = re.search(r'/.*', url).group()
    if REQ[-1]=='/':
        REQ=REQ[:-1]
    PORT = re.search(r':\d*/', url)
    if PORT:
        # print PORT
        PORT = PORT.group()
        PORT = PORT[1:-1]
        len_port = len(PORT)
        HOST = HOST[0:len(HOST) - len_port - 1]
    else:
        PORT = 80
    if not REQ:
        REQ='/'
    HOST = HOST[:-1]

    #print 'url is ' + url
    #print 'host is ' + HOST
    #print 'request is ' + REQ
    #print 'port is ' + str(PORT)
    PORT = int(PORT)

    global redir_count
    if redir_count>=10:
        print 'Warning: Too much redirects'
        sys.exit(1)
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #create connection
    s.connect((HOST, PORT))
    #send data
    command='GET '+REQ+' HTTP/1.1\r\n'+'Host:' +HOST+'\r\nConnection: close\r\n\r\n'
    s.send(command)
    #receive data
    buff=[]
    while True:
        data=s.recv(1024)
        if data:
            buff.append(data)
        else:
            break
    data=''.join(buff)
    s.close()
    header, html = data.split('\r\n\r\n', 1)
    state = int(re.search('\d\d\d', header).group())
    is_text=header.find('text/html')
    #print 'status code is '+str(state)
    if state==200:
        print '200 OK\n'
        #print header
        if is_text:
            print html
        sys.exit(0)
    if state==301:
        print '301\n'
        redir_count+=1
        print 'This is the '+str(redir_count+1)+' time of 301 redirect'
        redir_addr = re.search(r'Location:.*\r?',header)
        print(redir_addr.group())
        next = redir_addr.group()[9:]
        next.lstrip()
        print next
        http_client(next)
    if state==302:
        print '302\n'
        redir_count+=1
        print 'This is the ' + str(redir_count + 1) + ' time of 302 redirect'
        redir_addr = re.search(r'Location:.*\r?', header)
        print(redir_addr.group())
        next = redir_addr.group()[9:]
        next.lstrip()
        print next
        http_client(next)

        http_client(HOST)

    if state>=400:
        print '400+\n'
        sys.exit(1)

    print 'state code is :'+str(state)
    print '\n'
    print header
    print '------------'
    print html
http_client(url)



#with open('123.html', 'wb') as f:
 #   f.write(html)
