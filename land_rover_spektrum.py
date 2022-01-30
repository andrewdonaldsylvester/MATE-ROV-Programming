from serial import Serial
import socket
import pickle
import glob
# Look up serial port for ardunio
# Connect to Pi first, then run app


def invert_channel(value):
    return 3000 - value


def shrink_channel(value, scale):
    return 1500 + (value - 1500) / scale


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def clamp(x, in_min, in_max):
    return max(in_min, min(x, in_max))


ip = "10.1.10.160"

serverAddressPort = (ip, 20001)

bufferSize = 128

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

arduino_port = glob.glob('/dev/cu.usbmodem*')[0]
ser = Serial(arduino_port, 115200)


if ser.is_open:
    while True:
        values = ser.readline()
        channels = values.split()

        if len(channels) < 6:
            continue

        L_X = invert_channel(int(channels[3]))
        L_Y = int(channels[0])
        R_X = invert_channel(int(channels[1]))
        R_Y = invert_channel(int(channels[2]))

        # print("L_X {} L_Y {} R_X {} R_Y {} BINARY_SWITCH {} TERNARY_SWITCH {}"
        #       .format(L_X, L_Y, R_X, R_Y, BINARY_SWITCH, TERNARY_SWITCH))

        # forward = R_Y
        # strafe = R_X
        # turn = L_X
        # altitude = L_Y

        forward = R_Y
        strafe = L_X
        turn = R_X

        # speed_modifier = {"LO": 3, "MID": 2, "HI": 1}

        M1 = (forward -1500 + turn -1500 - strafe + 1500)/3 + 1500
        M2 = (forward -1500 + turn -1500 + strafe -1500)/3 + 1500
        M3 = (-forward + 1500 + turn -1500 - strafe +1500)/3 + 1500
        M4 = (-forward +1500 + turn -1500 + strafe -1500)/3 + 1500
        print("{} {} {} {}".format(M1, M2, M3, M4))

        M1 = clamp(M1, 1000, 2000)
        M2 = clamp(M2, 1000, 2000)
        M3 = clamp(M3, 1000, 2000)
        M4 = clamp(M4, 1000, 2000)


        M1 = map_value(M1, 1100, 1900, 1000, 2000)
        M2 = map_value(M2, 1100, 1900, 1000, 2000)
        M3 = map_value(M3, 1100, 1900, 1000, 2000)
        M4 = map_value(M4, 1100, 1900, 1000, 2000)

        send_message = pickle.dumps([M1, M2, M3, M4,
                                     0, 0, 0, 0,
                                     0, 0, 0, 0,
                                     0, 0, 0, 0])

        # send_message = pickle.dumps([1700, 1700, 1700, 1700,
        #                              0, 0, 0, 0,
        #                              0, 0, 0, 0,
        #                              0, 0, 0, 0])

        try:
            UDPClientSocket.sendto(send_message, serverAddressPort)
        except:
            print("Connection Lost, reconnecting...")
            UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            # print("Reconnected!")

        print("M1 = {:5} \t M2 = {:5} \t M3 = {:5} \t M4 = {:5}"
              .format(M1, M2, M3, M4))

ser.close()
