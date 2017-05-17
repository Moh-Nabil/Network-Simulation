import node, interface, packet

node1 = node.Node(1, [1, 2])
node2 = node.Node(2, [2, 3])
node3 = node.Node(3, [3, 4])

interface1= interface.Interface(node1, node2)
interface2= interface.Interface(node2, node3)

node1.add_interface(interface1)
node2.add_interface(interface1)
node2.add_interface(interface2)
node3.add_interface(interface2)

pkt= packet.make_pckt(1,3,3,4,packet.NORM_MESSAGE)
node1.send(3, 3, 4, pkt)