import socket
import json

# Receives JSON input and may provide output based on the parameters.
# instruction:<str>, determines which instruction of the port api to use...
#	open: open a TCP/UDP port to be used
#	close:closes a TCP port or UDP category.
#   put:  sends data to a remote TCP/UDP port
#	get:  receives data sent to a local TCP port or UDP category.
# protocol:<str>, UDP | TCP
# category:<str>, the unique name to be used when referring to a local port.
#	required for open,close,get
# portNumber:<int>, the local or remote port number to refer to.
#	required for open,put
# connections:<int>, the amount of possible connections servable from a TCP port.
#	required for TCP open
# ipAddress:<str>, the destination ip address
#	required for put
# message:<str>, the message to send to the destination.
#	required for put.
#
# Cheat Sheet
#	open:	protocol,instruction,category,portNumber,connections(TCP only)
#	close:	protocol,instruction,category
#	put:	protocol,instruction,portNumber,ipAddress,message
#	get:	protocol,instruction,category
def cppInterface(input):
	parsedInput = json.loads(input)
	p,i = parsedInput["protocol"],parsedInput["instruction"]
	if p == "UDP":
		if i == "open":
			return registerUDPPort(input)
		if i == "close":
			return flushUDPPorts(parsedInput["category"])
		if i == "put":
			return sendUDP(input)
		if i == "get":
			return receiveUDP(parsedInput["category"])
		return "bad instruction"
	if p == "TCP":
		if i == "open":
			return registerTCPPort(input)
		if i == "close":
			return closeTCPPort(parsedInput["category"])
		if i == "put":
			return sendTCP(input)
		if i == "get":
			return receiveTCP(parsedInput["category"])
		return "bad instruction"
	return "bad protocol"

UDP = {}
TCP = {}
	
# Accepts JSON Input...
# category:<str> ,  an identifier that ties a port to a group.
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
# category:<str> ,  an identifier that can be used to access the port.
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
	udpsocket.sendto(msg.encode(),(ipAddress,portNumber))
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
	tcpsocket.send(msg.encode())
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
			result += [{"data":data.decode(),"ip":str(addr[0]),"port":addr[1]}]
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
		return json.dumps({"data":data.decode(),"ip":str(addr[0]),"port":addr[1]})
	except socket.timeout:
		pass
	return ""	

# Closes an entire UDP category.
def flushUDPPorts(category):
	global UDP
	for key in UDP:
		for port in UDP[key]:
			port.close()
	del UDP[category]
	return ""

# Closes a TCP port	
def closeTCPPort(name):
	global TCP
	TCP[name].close()
	del TCP[name]
	return ""
