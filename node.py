import time, math
import threading
import packet, interface

HELLO_MESSAGE_PERIOD= 1
HELLO_SIZE= 17
EPS= 2
DEBUG_FLAG= False

def debug(string):
	if(DEBUG_FLAG):
		print(string)

class Node(object):

	def __init__(self, id, loc):
		self.id = id
		self.loc = loc
		print(id, ": ", loc[0], loc[1])
		self.interfaces = []
		self.RTTs= {}
		self.bandwidths = {}
		self.time = {}
		self.run()

	def add_interface(self,interface):
		# initializing interface
		debug("Adding interface between %d %d" % (interface.node_1.id, interface.node_2.id))
		self.interfaces.append(interface)
		self.bandwidths[interface]= [0, 0, 0]
		self.time[interface]= [0, 1, 2]
		self.RTTs[interface]= None


	def send_hello_message(self):
		while(True):
			pkt = packet.make_pckt(self.id, 0, 0, 0, packet.HELLO_MESSAGE)
			for interface in self.interfaces:
				
				### for debugging
				to_node= interface.node_1
				if(self.id == interface.node_1.id):
					to_node= interface.node_2
				###

				debug("%d sending HELLO to %d" % (self.id, to_node.id))
				if(self.RTTs[interface] == None): # save the time of the first send only
					self.RTTs[interface] = time.time()
					interface.send(pkt, self.id)
			time.sleep(HELLO_MESSAGE_PERIOD)


	def recv_ack_message(self, interface, message):
		
		### for debugging
		from_node= interface.node_1
		if(self.id == interface.node_1.id):
			from_node= interface.node_2
		
		debug("%d received ACK from %d" % (self.id, from_node.id))
		###

		t= time.time()
		bandwidth= HELLO_SIZE/(t - self.RTTs[interface])
		if(math.fabs(bandwidth - self.bandwidths[interface][2]) > EPS):
			self.bandwidths[interface][0]= self.bandwidths[interface][1]
			self.bandwidths[interface][1]= self.bandwidths[interface][2]
			self.bandwidths[interface][2]= bandwidth
			self.time[interface][0]= self.time[interface][1]
			self.time[interface][1]= self.time[interface][2]
			self.time[interface][2]= t
		self.RTTs[interface]= None


	def send_ack(self, interface):
		
		### for debugging
		node= interface.node_1
		if(self.id != interface.node_2.id):
			node= interface.node_2

		debug("%d received HELLO from %d" % (self.id, node.id))
		###

		pkt = packet.make_pckt(self.id, 0, 0, 0, packet.ACK_MESSAGE)
		debug("%d sent ACK message to %d" % (self.id, node.id))
		interface.send(pkt, self.id)


	def recv(self, interface, message):
		if packet.isACK(message):
			debug("%d received ACK from %d" % (self.id, packet.get_src(message)))
			self.recv_ack_message(interface, message)
		elif packet.isHello(message):
			debug("%d received HELLO from %d" % (self.id, packet.get_src(message)))
			self.send_ack(interface)
		else :
			debug("%d received NORM from %d" % (self.id, packet.get_src(message)))
			self.recv_message(message)


	def recv_message(self, message):
		dst = packet.get_dst(message)
		dst_x= packet.get_x(message)
		dst_y= packet.get_y(message)
		if (dst == self.id):
			print("%d received NORM from %d message: %s" %(self.id, packet.get_src(message), message))
		else:
			print("Routing point: %d from: %d to: %d" %(self.id, packet.get_src(message), dst))
			interface = self.route(dst, dst_x, dst_y)
			if(interface != None):
				interface.send(message, self.id)

	def send(self, dst_node_id, dst_x, dst_y):
		print("%d sending NORM to %d" % (self.id, dst_node_id))

		pkt = packet.make_pckt(self.id, dst_node_id, dst_x, dst_y, packet.NORM_MESSAGE)
		
		interface = self.route(dst_node_id, dst_x, dst_y)
		if(interface != None):
			interface.send(pkt, self.id)

	def route(self, dst_id, dst_x, dst_y):#added
		max_interface = None
		maxBW = -(1<<20)
		for interface in self.interfaces:
			if(interface.get_end_point(self).id == dst_id):
				return interface
			node = interface.get_end_point(self)
			debug("%d %s %d %d %d %d %d %d" % (self.id, "inQuad:",self.loc[0],self.loc[1],dst_x,dst_y,node.loc[0],node.loc[1]))
			if(self.inQuad(self.loc[0],self.loc[1],dst_x,dst_y,node.loc[0],node.loc[1])):
				futureBW = self.get_bandwidth(self.bandwidths[interface][0],self.bandwidths[interface][1],self.bandwidths[interface][2],time.time(),self.time[interface][2],self.time[interface][1],self.time[interface][0])
				debug('--------------------- %d' % futureBW)
				if(futureBW > maxBW):
					maxBW = futureBW
					max_interface = interface
		if(max_interface == None):
			print("Destination %d unreachable from %d" % (dst_id, self.id))
			return None

		print("%d chose interface connected to %d" % (self.id, max_interface.get_end_point(self).id))
		return max_interface


	def inQuad(self,src_x,src_y,dst_x,dst_y,point_x,point_y):
		debug("%d %d %s %d %d %d %d %d %d" % (self.loc[0], self.loc[1], "noooooooooooorm", self.norm_vec(src_x,src_y,dst_x,dst_y), self.norm_vec(src_x,src_y,point_x,point_y), src_x, src_y, point_x, point_y))
		theta = round(math.degrees(math.acos(self.dot_product(src_x,src_y,dst_x,dst_y,point_x,point_y)/(self.norm_vec(src_x,src_y,dst_x,dst_y)*self.norm_vec(src_x,src_y,point_x,point_y)))),3)
		if(theta <= 45):
			return True
		return False

	def dot_product(self,src_x,src_y,dst_x,dst_y,point_x,point_y):
		return (dst_x-src_x)*(point_x-src_x)+(dst_y-src_y)*(point_y-src_y)

	def norm_vec(self,src_x,src_y,dst_x,dst_y):
		return ((src_x-dst_x)**2+(src_y-dst_y)**2)**(.5)

	def get_bandwidth(self,bij0,bij1,bij2,tp,t2,t1,t0):#added
		bijp = bij0+((bij0/(t0-t1))+(bij1/(t1-t0)))*(tp-t0)+((bij0/((t0-t1)*(t0-t2)))+(bij1/((t1-t0)*(t1-t2)))+(bij2/((t2-t0)*(t2-t1))))*(tp-t1)*(tp-t0)
		return bijp

	def run(self):
		threading.Thread(target=self.send_hello_message).start()
