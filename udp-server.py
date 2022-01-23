import socket
import time
import json
localIP = "127.0.0.1"

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
while True:

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    if (count % 1000) == 0:
        print(clientMsg)
        print(clientIP)
        data = json.loads(message.decode('utf-8'))
        print(data)



    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)
