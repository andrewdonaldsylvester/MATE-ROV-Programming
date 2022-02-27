mport socket
import time
import json
import pickle
import math
import qwiic_pca9685


PCA9685 = qwiic_pca9685.QwiicPCA9685(0x40, 0)
PCA9685.soft_reset()
PCA9685.restart()
PCA9685.set_pre_scale(50)


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def write_micros(channel, microseconds):
    value = map_value(microseconds, 1000, 2000, 204.8 + 12, 409.6 + 24)
    value = round(value)

    PCA9685.set_channel_word(channel, 1, 0)
    PCA9685.set_channel_word(channel, 0 , value)


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

# Listen for incoming datagrams
count = 0
while (True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    data = pickle.loads(message)

    for c in range(16):
        write_micros(c, data[c])

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
    
