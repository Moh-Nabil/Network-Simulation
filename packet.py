import random


HELLO_MESSAGE = 0
ACK_MESSAGE = 1
NORM_MESSAGE= 2

random.seed(0)

def intToBytes(num, size):
    return num.to_bytes(size, byteorder='big')

def bytesToInt(byte):
    return (int.from_bytes(byte, byteorder='big'))

def isACK(pckt):
    return bytesToInt(pckt[8:9]) == ACK_MESSAGE

def isHello(pckt):
    return bytesToInt(pckt[8:9]) == HELLO_MESSAGE

def isNorm(pckt):
    return bytesToInt(pckt[8:9]) == NORM_MESSAGE

def get_dst(pckt):
    return bytesToInt(pckt[4:8])

def get_src(pckt):
    return bytesToInt(pckt[0:4])

def get_x(pckt):
    return bytesToInt(pckt[9:13])

def get_y(pckt):
    return bytesToInt(pckt[13:17])

def make_pckt(src,dst,dst_x,dst_y,messType):
    if(messType == NORM_MESSAGE):
        mess = gen_mess()
        pckt = intToBytes(src,4) + intToBytes(dst,4) + intToBytes(NORM_MESSAGE,1) + intToBytes(dst_x,4)  + intToBytes(dst_y,4) + mess.encode()
    elif(messType == ACK_MESSAGE):
        pckt = intToBytes(src,4) + intToBytes(dst,4) + intToBytes(ACK_MESSAGE,1) + intToBytes(dst_x,4)  + intToBytes(dst_y,4)
    elif(messType == HELLO_MESSAGE):
        pckt = intToBytes(src,4) + intToBytes(dst,4) + intToBytes(HELLO_MESSAGE,1) + intToBytes(dst_x,4)  + intToBytes(dst_y,4)
    return pckt

def gen_mess():
    return chr(random.randrange(ord('A'),ord('z')))+chr(random.randrange(ord('A'),ord('z')))+chr(random.randrange(ord('A'),ord('z')))
 
