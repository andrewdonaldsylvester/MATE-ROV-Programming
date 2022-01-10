from pi_hat_motor_control import PiHat
import time

my_hat = PiHat()
for _ in range(5):
    for motor_vel in range(-100, 100, 2):
        print(motor_vel/100)
        my_hat.drive_motor(0, motor_vel/100)
        #my_hat.drive_motor(1, motor_vel/100)
        my_hat.drive_motor(2, motor_vel/100)
        #my_hat.drive_motor(3, motor_vel/100)

        time.sleep(0.1)
    
my_hat.stop_all_motors()

