from node import Node
import interface, packet
import math, random, time, sys


RADIUS= 10
NETWORK_SIZE= 20
LAMBDA= 1
# random.seed(2)

def polar_to_cart(point, radius, theta):
	theta_radian= math.radians(theta)
	return [math.floor(point[0]+radius*math.cos(theta_radian)), math.floor(point[1]+radius*math.sin(theta_radian))]

def generate_nodes(node_number= 5):
	nodes= [Node(0, [100,100])]
	for i in range(1,node_number):
		radius= random.uniform(5, RADIUS-1)
		theta= random.randint(0, 360)
		print('Radius:', radius, 'theta:', theta)
		nodes.append(Node(i, polar_to_cart(nodes[i-1].loc, radius, theta)))

	return nodes

def dist(pt1, pt2):
	return math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)




nodes= generate_nodes(NETWORK_SIZE)
edges= 0
for i in range(0, NETWORK_SIZE):
	for j in range(i+1, NETWORK_SIZE):
		if(dist(nodes[i].loc, nodes[j].loc) <= RADIUS):
			interface_tmp= interface.Interface(nodes[i], nodes[j])
			nodes[i].add_interface(interface_tmp)
			nodes[j].add_interface(interface_tmp)
			edges+= 1

print("EDGES:", edges)


# node1 = node.Node(1, [1, 2])
# node2 = node.Node(2, [2, 3])
# node3 = node.Node(3, [3, 4])

# interface1= interface.Interface(node1, node2)
# interface2= interface.Interface(node2, node3)

# node1.add_interface(interface1)
# node2.add_interface(interface1)
# node2.add_interface(interface2)
# node3.add_interface(interface2)

while(True):
	num_packets_to_send= round(-math.log(random.random()) / LAMBDA)

	for i in range(num_packets_to_send):
		id1= random.randint(0, NETWORK_SIZE-1)
		id2= id1
		while(id1 == id2):
			id2= random.randint(0, NETWORK_SIZE-1)

		nodes[id1].send(id2, nodes[id2].loc[0], nodes[id2].loc[1])


# while(True):
# 	condition= input('[n] for new packet, [t] for new topology\n')
# 	if(condition == 't'):
# 		break
# 	id1= int(input('Enter source node ID: '))
# 	id2= int(input('Enter destination node ID: '))	
# 	nodes[id1].send(id2, nodes[id2].loc[0], nodes[id2].loc[1])
