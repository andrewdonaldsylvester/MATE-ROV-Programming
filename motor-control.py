import time
import pi_servo_hat
test = pi_servo_hat.PiServoHat()
test.restart()
test.move_servo_position(0, 0)

# Pause 1 sec
time.sleep(1)

# Moves servo position to 90 degrees (2ms), Channel 0
test.move_servo_position(0, 0)

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def send_pwm(channel, signal):
    # signal (in microseconds for PWM)
    #print(signal)
    
    angle = (signal - 922) / 10.8
    
    test.move_servo_position(channel, angle)


def drive_motor(channel, velocity):
    # velocity is a float between -1 and 1.
    # -1 corresponds to full backwards,
    # 1 corresponds to full forwards,
    # 0 corresponds to stopped
    
    velocity = max(min(velocity, 1), -1)
    velocity = map_value(velocity, -1, 1, 1000, 2000)
    
    send_pwm(channel, velocity)
    
def stop_all_motors():
    for channel in range(16):
        drive_motor(channel, 0)
    

# Pause 1 sec
time.sleep(0.1)
#angle = (pwm-922)/10.8.
for motor_vel in range(-100, 100, 2):
    print(motor_vel/100)
    drive_motor(0, motor_vel/100)
    time.sleep(0.1)
    
stop_all_motors()

#     for i in range(0, 90):
#         print(i)
#         test.move_servo_position(0, i)
#         time.sleep(2)
#     for i in range(90, 0, -1):
#         print(i)
#         test.move_servo_position(0, i)
#         time.sleep(2)
