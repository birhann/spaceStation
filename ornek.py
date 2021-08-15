import socket

UDP_IP_ADDRESS = "192.168.137.173"
ESP_IP_ADDRESS = "192.168.137.135"
UDP_PORT_NO = 44444

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
Message = "START"
Message2 = "@@@engineL"

serverSock.sendto(bytes(Message, encoding='utf8'),
                  (ESP_IP_ADDRESS, UDP_PORT_NO))
print("Gitti")

while True:
    data, addr = serverSock.recvfrom(1024)
    #telemetry = data.split(b",")
    print("Message: ", data)
