# Import socket module
from socket import *
import select
import Queue
import sys
import os
if len(sys.argv)>1:
    port = sys.argv[1]
port=int(port)
Correctstatus = 'HTTP/1.1 200 OK\r\n'
Errorstatus404 = 'HTTP/1.1 404 Not Found\r\n\r\n'
Errorstatus403 = 'HTTP/1.1 403 Forbidden\r\n\r\n'
contenttype = 'Content-Type:text/html\r\n'
def returnresult(message):#sendinfotoclient
	filename = message.split()[1]
	filename=filename[1:]
	print filename
	if os.path.isfile(filename) == 0:
		data=Errorstatus404.encode()
		body = "<html><head><title>" + Errorstatus404 + "</title></head><body><h1>" + Errorstatus404 + "</h1></body></html>"
		data+=body.encode()
		data+='\r\n'.encode()
	elif (findhtml == -1 | findhtm == -1):
		data+=Errorstatus403.encode()
		body = "<html><head><title>" + Errorstatus403 + "</title></head><body><h1>" + Errorstatus403 + "</h1></body></html>"
		data+=body.encode()
		data+='\r\n'.encode()
	else:
		f = open(filename)
	#print('openfile',filename[1:])
		outputdata = f.read()
		data = Correctstatus.encode()
		#print('data1', data)
		data += 'Content-Type:text/html\r\n'.encode()
		#print('data2', dat a)
		data +=  '\r\n'.encode()
		#print('data3', data)
		for i in range(0, len(outputdata)):
			#print('data4', data)
			data+=outputdata[i].encode()
		data+='\r\n'.encode()
	#print(data)
	return data

ss = socket(AF_INET, SOCK_STREAM)
serverPort = port
ss.bind(('', serverPort))#LOCAL HOST
ss.listen(5)
print "The server is ready now."
input= [ss]
response = []
message = {}
client_info={}
while True:
	read,write,err = select.select(input,response,input)
	#print(read,write,err)
	for ele in read:
		if ele is ss:
			connect,addr = ele.accept()
			#print('new client',addr)
			connect.setblocking(1)
			input.append(connect)
			message[connect] = Queue.Queue()
		else:
			data = ele.recv(1024)
			#print('receving...',data)
			if data:
				#print(type(data))
				info = returnresult(data)
				#print(info)
				message[ele].put(info)
				if ele not in response:
					response.append(ele)
			else:
				if ele in response:
					response.remove(ele)
				input.remove(ele)
				ele.close()
	for ele in write:
		try:
			nex = message[ele].get_nowait()
		except Queue.Empty:
			response.remove(ele)
		else:
			ele.send(nex)
	for ele in err:
		input.remove(ele)
		if ele in response:
			response.remove(ele)
		ele.close()




