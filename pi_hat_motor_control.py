import time
import pi_servo_hat
import atexit


def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class PiHat:
    def __init__(self):
        self.hat = pi_servo_hat.PiServoHat()
        self.hat.restart()
        
        atexit.register(self.stop_all_motors) # this only works when run in terminal

    def send_pwm(self, channel, signal):
        # signal (in microseconds for PWM)
        
        angle = (signal - 922) / 10.8
        
        self.hat.move_servo_position(channel, angle)


    def drive_motor(self, channel, velocity):
        # velocity is a float between -1 and 1.
        # -1 corresponds to full backwards,
        # 1 corresponds to full forwards,
        # 0 corresponds to stopped
        
        velocity = max(min(velocity, 1), -1)
        velocity = map_value(velocity, -1, 1, 1000, 2000)
        
        self.send_pwm(channel, velocity)
    
    def stop_all_motors(self):
        for channel in range(16):
            self.drive_motor(channel, 0)

if __name__ == "__main__": 
    my_hat = PiHat()
    

    for motor_vel in range(-100, 100, 2):
        print(motor_vel/100)
        my_hat.drive_motor(0, motor_vel/100)
        time.sleep(0.1)
        
    my_hat.stop_all_motors()

