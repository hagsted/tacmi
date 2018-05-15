import socket
from read_message import TACoE_read

UDP_IP = "192.168.2.50"
UDP_IPs = "192.168.2.32"
UDP_PORT = 5441

MESSAGE = b'\x02\x01\x00\x00\x00\x00\x00\x00^\x00\x00\x00\x01\x01'
  
print ("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)
  
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IPs, UDP_PORT))
 
sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
    
units = ['', '°C', 'W/m²', 'l/h', 'sec', 'min', 'l/Imp', 'K', '%', '','kW', 'kWh', 'MWh', 'V', 'mA', 'hr','Days', 'Imp', 'kΩ', 'l', 'km/h', 'Hz', 'l/min', 'bar', '','km', 'm', 'mm', 'm³', 'l/d', 'm/s', 'm³/min', 'm³/h', 'm³/d', 'mm/min', 'mm/h', 'mm/d', 'ON/OFF', 'NO/YES', '°C', '€', '$', 'g/m³', '','°', '°', 'sec', '','%', 'h', 'A', 'mbar', 'Pa', 'ppm']
scaling = [0, 1, 0, 0,0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0 ]
outo = TACoE_read()
while True:
    data, addr = sock.recvfrom(14) # buffer size is 14 bytes
    outo.get_message(data)
    print("can_node:",outo.can_node, ':',outo.analog_value, ':',outo.analog_unit)
