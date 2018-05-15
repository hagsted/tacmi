from TACoE_write import *

UDP_IP = "192.168.2.50"
UDP_IPs = "192.168.2.32"
UDP_PORT = 5441

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

outo = TACoE_read("192.168.2.32", 2)

while True:
    data, addr = sock.recvfrom(14)  # buffer size is 1024 bytes
    outo.get_message(data)
    print(outo.analog_value[0], ':', outo.analog_unit[0], ':', type(data[0]))
