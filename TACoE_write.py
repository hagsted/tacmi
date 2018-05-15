from units import units_dict
import socket
class  TACoE_read():
    def __init__(self, ip_addrs, can_node):
        self.ip_address = ip_addrs
        self.port = 5441
        self.can_node = can_node        
        self.digital = [False] * 32
        self.analog_value = [0]*32
        self.analog_unit = [0]*32

    def get_message(self, data):
        self.can_node = data[0]
        pod_number = data[1]
        if pod_number in [0, 9]:
            self.get_digital(pod_number, data)
        elif pod_number < 9:
            self.get_analog(pod_number, data)
    
    def get_digital(self, pod_number, data):
        digital_data =int.from_bytes(data[2:4], byteorder = 'little') 
        for i in range(15, -1, -1):
            if  digital_data >= 2**i:
                self.digital[i + 16*(pod_number==9)] =True
                digital_data -= 2**i
                
    def get_analog(self, pod_number, data):
        for i in range(0, 4):
            if units_dict[data[10+i]][1] >= 0:
                self.analog_value[(pod_number-1)*4 + i] = int.from_bytes(data[i*2+2:i*2+4], byteorder = 'little', signed=True)  / \
                    10**units_dict[data[10+i]][1]
                self.analog_unit[(pod_number-1)*4 + i] = data[10 + i]

class  TACoE_write():
    def __init__(self, ip_addrs, can_node):
        self.ip_address = ip_addrs
        self.port = 5441
        self.can_node = can_node
        self.digital = [False] * 32
        self.analog_value = [0]*32
        self.analog_unit = [0]*32

    def digital(self,  output, value):
        self.digital[output-1] = value
        if output <= 16:
            pod_number = 0
            pod_correction = 0
        elif output <= 32:
            pod_number = 9
            pod_correction = 16
        data = 0
        for i in range(0, 15):
            if self.digital[i+pod_correction]:
                data += 2**i
        message = bytes([self.can_node, pod_number, data, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.send_message(message)
        
    def  analog(self, output, value, unit):
        pod_number = (output -1) // 4 + 1
        self.analog_unit[output-1] = unit
        self.analog_value[output-1] = int(value * 10**units_dict[self.analog_unit[output-1]][1])
        message = bytes([self.can_node, pod_number])\
            + self.analog_value[(pod_number - 1)  * 4].to_bytes(2, byteorder='little', signed=True) \
            + self.analog_value[(pod_number - 1) * 4 + 1].to_bytes(2, byteorder='little', signed=True)\
            + self.analog_value[(pod_number - 1) * 4 + 2].to_bytes(2, byteorder='little', signed=True)\
            + self.analog_value[(pod_number - 1) * 4 + 3].to_bytes(2, byteorder='little', signed=True)\
            + bytes(self.analog_unit[(pod_number - 1) * 4:(pod_number - 1) * 4 + 4]) 
        self.send_message(message)
        
    def send_message(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, (self.ip_address, self.port))
