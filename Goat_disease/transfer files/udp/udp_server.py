# socket udp
#The socket constructor expects two parameters: the address family (in this case, Internet addresses) and the socket type (in this case, UDP).
# udp server which will connect and communicate via the local port port.
'''UDP is fast but not very reliable and WebSockets (TCP) is reliable but not very fast. Use UDP for high-speed games and TCP for everything else.

As you mentioned, WebSockets and UDP are on different network layers. Since WebSockets is built on TCP with a bit of overhead during connection setup, this is more of a comparison between TCP and UDP.

Between TCP and UDP, UDP is lower latency as you mentioned, but that comes at the cost of reliability'''

#Libraries
import socket    #https://wiki.python.org/moin/UdpCommunication

#Parameters
localPort=8888
bufferSize=1024

#Objects
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  ## Internet,UDP

# function init 
def init():
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #enable broadcasting mode
    sock.bind(('', localPort))
    print("UDP server : {}:{}".format(get_ip_address(),localPort))

# function main 
def main():
    while True:
        data, addr = sock.recvfrom(1024) # get data
        print("received message: {} from {}\n".format(data,addr))
    
        sock.sendto("RPi received OK",addr)  # write data
  

# function get_ip_address 
def get_ip_address():
    """get host ip address"""
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address




if __name__ == '__main__':
    init()
    main()


#The get_ip_address() function implements a method for obtaining the Raspberry Pi’s IP address by opening a socket temporarily. It is also possible to use the os library with the ifconfig command.

#Make a note of the Raspberry Pi’s IP address and port, and copy them into the client code:

#IP address: 192.168.1.46
#Port number: 8888