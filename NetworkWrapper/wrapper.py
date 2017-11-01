import socket

UDP = {}

def flushUDPPorts(category):
	global UDP
	UDP[category] = []
	return ""
	
def registerUDPPort(category,portNumber):
	global UDP
	try:
		UDP[category].append(socket.socket(socket.AF_INET,socket.SOCK_DGRAM))
	except:
		UDP[category] = []
		UDP[category].append(socket.socket(socket.AF_INET,socket.SOCK_DGRAM))
	(UDP[category][-1]).bind(("localhost",portNumber))
	(UDP[category][-1]).settimeout(0.0001)
	return ""
	
def sendUDP(ipAddress,portNumber,msg):
	udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	udpsocket.sendto(msg,(ipAddress,portNumber))
	return ""
	
def receiveUDP(category):
	global UDP
	result = []
	for i in UDP[category]:
		try: 
			data, addr = i.recvfrom(1024)
			result += [str(data) + ";" + str(addr)]
		except socket.timeout:
			pass
	return "|".join(set(result))
	
TCP = {}

def registerTCPPort(name,connections,portNumber):
	global TCP
	TCP[name] = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	TCP[name].bind(("localhost",portNumber))
	TCP[name].settimeout(0.0001)
	TCP[name].listen(connections)
	return ""
	
def closeTCPPort(name):
	global TCP
	TCP[name].close()
	del TCP[name]
	return ""
	
def sendTCP(ipAddress,portNumber,retries,msg):
	global TCP
	tcpsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	tcpsocket.settimeout(0.0001)
	tcpsocket.connect((ipAddress,portNumber))
	tcpsocket.send(msg)
	return ""

def receiveTCP(name):
	try:
		conn, addr = TCP[name].accept()
		data = conn.recv(1024)
		return str(data) + ";" + str(addr)
	except socket.timeout:
		pass
	return ""