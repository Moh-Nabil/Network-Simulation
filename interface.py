import socket, threading, sys, time
import node, packet


class Interface(object):
	def __init__(self, node_1, node_2):
		self.lock= threading.Lock()
		self.node_1 = node_1
		self.node_2 = node_2
		self.socket_1 = self.createSocket(node_1.id)
		self.socket_2 = self.createSocket(node_2.id)
		threading.Thread(target=self.recv,args=(self.socket_1,)).start()
		threading.Thread(target=self.recv,args=(self.socket_2,)).start()



	def createSocket(self, port):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind(('', 0))
			return s
		except socket.error as msg :
			print ('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
			sys.exit()
		return

	def get_end_point(self, node):#added
		if node.id == self.node_1.id:
			return self.node_2
		return self.node_1


	def send(self, pkt, id):
		time.sleep(0.1)
		if(id == self.node_1.id):
			socket_src= self.socket_1
			socket_dst= self.socket_2
		else:
			socket_src= self.socket_2
			socket_dst= self.socket_1

		
		self.lock.acquire()
		port_num= socket_dst.getsockname()[1]
		socket_src.sendto(pkt, ('localhost', port_num))
		self.lock.release()
		# while(socket_src.sendto(pkt, ('localhost', socket_dst.getsockname()[1])) == 0):
		# 	pass

	def recv(self, socket):
		if socket == self.socket_1:
			node = self.node_1
		else:
			node = self.node_2

		while True:
			# print("Receiving %d" % node.id)
			pckt, addr = socket.recvfrom(2048)
			node.recv(self, pckt)