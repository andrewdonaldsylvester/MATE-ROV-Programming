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


ip = "192.168.1.2"

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

        BINARY_SWITCH = int(channels[4])
        BINARY_SWITCH = map_value(BINARY_SWITCH, 1100, 1900, 1000, 2000)

        TERNARY_SWITCH = int(channels[5])

        # print("L_X {} L_Y {} R_X {} R_Y {} BINARY_SWITCH {} TERNARY_SWITCH {}"
        #       .format(L_X, L_Y, R_X, R_Y, BINARY_SWITCH, TERNARY_SWITCH))

        # forward = R_Y
        # strafe = R_X
        # turn = L_X
        # altitude = L_Y

        forward = R_Y
        strafe = L_X
        turn = R_X
        altitude = L_Y

        # speed_modifier = {"LO": 3, "MID": 2, "HI": 1}

        M1 = forward - strafe - shrink_channel(turn, 2) + 3000
        M2 = forward + strafe + shrink_channel(turn, 2) - 3000
        M3 = forward + strafe - shrink_channel(turn, 2)
        M4 = forward - strafe + shrink_channel(turn, 2)

        # if abs(altitude - 1500) <= 100:
        #     altitude = 1500

        M5 = altitude
        M6 = altitude

        M1 = clamp(M1, 1100, 1900)
        M2 = clamp(M2, 1100, 1900)
        M3 = clamp(M3, 1100, 1900)
        M4 = clamp(M4, 1100, 1900)
        M5 = clamp(M5, 1100, 1900)
        M6 = clamp(M6, 1100, 1900)

        # M1 = map_value(M1, 1100, 1900, 1100, 1900)
        # M2 = map_value(M2, 1100, 1900, 1100, 1900)
        # M3 = map_value(M3, 1100, 1900, 1100, 1900)
        M4 = map_value(M4, 1100, 1900, 1900, 1100)
        # M5 = map_value(M5, 1100, 1900, 1100, 1900)
        # M6 = map_value(M6, 1100, 1900, 1100, 1900)

        M1 = map_value(M1, 1100, 1900, 1250, 1750)
        M2 = map_value(M2, 1100, 1900, 1250, 1750)
        M3 = map_value(M3, 1100, 1900, 1250, 1750)
        M4 = map_value(M4, 1100, 1900, 1250, 1750)
        M5 = map_value(M5, 1100, 1900, 1250, 1750)


        # M6 = map_value(M6, 1100, 1900, 1750, 1250)
        M6 = map_value(M6, 1100, 1900, 1250, 1750)

        M1 = clamp(M1, 1250, 1750)
        M2 = clamp(M2, 1250, 1750)
        M3 = clamp(M3, 1250, 1750)
        M4 = clamp(M4, 1250, 1750)
        M5 = clamp(M5, 1250, 1750)
        M6 = clamp(M6, 1250, 1750)

        send_message = pickle.dumps([M1, M2, M3, M4,
                                     M5, M6, 0, 0,
                                     0, 0, 0, 0,
                                     0, 0, 0, BINARY_SWITCH - 80])

        try:
            UDPClientSocket.sendto(send_message, serverAddressPort)
        except:
            print("Connection Lost, reconnecting...")
            UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            print("Reconnected!")

        print("M1 = {:5} \t M2 = {:5} \t M3 = {:5} \t M4 = {:5} \t M5 = {:5} \t M6 = {:5} \t S1 = {:5}"
              .format(M1, M2, M3, M4, M5, M6, BINARY_SWITCH))

ser.close()
