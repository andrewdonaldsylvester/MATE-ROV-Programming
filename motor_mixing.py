from pi_hat_motor_control import PiHat
import time

my_hat = PiHat()


def drive(forward_vel, strafe_vel, turn_vel):
    motor1_vel =  forward_vel - strafe_vel - turn_vel
    motor2_vel =  forward_vel + strafe_vel - turn_vel
    motor3_vel = -forward_vel - strafe_vel - turn_vel
    motor4_vel = -forward_vel + strafe_vel - turn_vel

    my_hat.drive_motor(0, motor1_vel)
    my_hat.drive_motor(1, motor2_vel)
    my_hat.drive_motor(2, motor3_vel)
    my_hat.drive_motor(3, motor4_vel)

for _ in range(10):
    drive(1, 0, 0)
    time.sleep(1)
    drive(0, 0, 0.7)
    time.sleep(2.5)
    drive(0, 1, 0)
    time.sleep(1)
    drive(0, 0, 0.7)
    time.sleep(2)
    drive(0.6, 0.1, 0.3)
    time.sleep(4)

    
my_hat.stop_all_motors()
