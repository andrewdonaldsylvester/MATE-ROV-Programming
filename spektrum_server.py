import socket
import time
import json
import pickle
import math
from pi_hat_motor_control import PiHat


localIP = "0.0.0.0"

localPort = 20001

bufferSize = 128

msgFromServer = "Hello UDP Client"

bytesToSend = str.encode(msgFromServer)

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

hat = PiHat()

# Listen for incoming datagrams
count = 0
while (True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)
    
    if clientIP == "192.168.1.47":
      print("from main computer")
      
    data = pickle.loads(message)

    for c in range(16):
        hat.send_pwm(c, data[c])

    print(data)

    #count += 1
    #if count == 1:
        #start_time = time.time()
    #if (count % 10) == 0:
        #rate = count / (time.time() - start_time)
        #print("Rate == {} qps count: {}".format(rate, count))
        #print(clientMsg)
        #print(clientIP)



    # Sending a reply to client

    UDPServerSocket.sendto(str.encode("test"), address)
    
