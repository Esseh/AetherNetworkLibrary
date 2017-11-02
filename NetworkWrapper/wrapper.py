import socket
import json

UDP = {}
TCP = {}
	
# Accepts JSON Input...
# Category:<str> ,  an identifier that ties a port to a group.
# portNumber:<int>, the actual port number to register.
def registerUDPPort(input):
	global UDP
	parsedInput = json.loads(input)
	category,portNumber = parsedInput["category"], parsedInput["portNumber"]
	try:
		UDP[category].append(socket.socket(socket.AF_INET,socket.SOCK_DGRAM))
	except:
		UDP[category] = []
		UDP[category].append(socket.socket(socket.AF_INET,socket.SOCK_DGRAM))
	(UDP[category][-1]).bind(("localhost",portNumber))
	(UDP[category][-1]).settimeout(0.0001)
	return ""

# Accepts JSON Input...
# Category:<str> ,  an identifier that can be used to access the port.
# portNumber:<int>, the actual port number to register.
# connections:<int>, the maximum amount of connections to hold onto.
def registerTCPPort(input):
	global TCP
	parsedInput = json.loads(input)
	name,portNumber,connections = parsedInput["category"], parsedInput["portNumber"], parsedInput["connections"]
	TCP[name] = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	TCP[name].bind(("localhost",portNumber))
	TCP[name].settimeout(0.0001)
	TCP[name].listen(connections)
	return ""
	
# Accepts JSON Input...
# ipAddress:<str>,  The ip address of the receiver
# portNumber:<int>, The port number of the receiver
# message:<str>,    The message to send to the receiver
def sendUDP(input):
	parsedInput = json.loads(input)
	ipAddress,portNumber,msg = parsedInput["ipAddress"], parsedInput["portNumber"], parsedInput["message"]
	udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	udpsocket.sendto(msg,(ipAddress,portNumber))
	return ""

# Accepts JSON Input...
# ipAddress:<str>,  The ip address of the receiver
# portNumber:<int>, The port number of the receiver
# message:<str>,    The message to send to the receiver
def sendTCP(input):
	parsedInput = json.loads(input)
	ipAddress,portNumber,msg = parsedInput["ipAddress"], parsedInput["portNumber"], parsedInput["message"]
	tcpsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	tcpsocket.settimeout(0.0001)
	tcpsocket.connect((ipAddress,portNumber))
	tcpsocket.send(msg)
	return ""

# Outputs JSON Array
# ipAddress:<str>,  address of sender
# portNumber:<int>, port number of sender
# message:<str>,    message sent by sender
def receiveUDP(category):
	global UDP
	result = []
	for port in UDP[category]:
		try: 
			data, addr = port.recvfrom(1024)
			result += [{"data":str(data),"ip":str(addr[0]),"port":addr[1]}]
		except socket.timeout:
			pass
	return json.dumps(result)

# Outputs JSON
# ipAddress:<str>,  address of sender
# portNumber:<int>, port number of sender
# message:<str>,    message sent by sender
def receiveTCP(name):
	try:
		conn, addr = TCP[name].accept()
		data = conn.recv(1024)
		return json.dumps({"data":str(data),"ip":str(addr[0]),"port":addr[1]})
	except socket.timeout:
		pass
	return ""	

def flushUDPPorts(category):
	global UDP
	for port in UDP:
		port.close()
	UDP[category] = []
	return ""
	
def closeTCPPort(name):
	global TCP
	TCP[name].close()
	del TCP[name]
	return ""
