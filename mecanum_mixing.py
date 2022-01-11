from pi_hat_motor_control import PiHat
import time

class MecanumLandRover:
    def __init__(self, m1_channel=0, m2_channel=1, m3_channel=2, m4_channel=3):
        self.hat = PiHat()
        self.m1_channel = m1_channel
        self.m2_channel = m2_channel
        self.m3_channel = m3_channel
        self.m4_channel = m4_channel

    def drive(self, forward_vel, strafe_vel, turn_vel):
        motor1_vel =  forward_vel - strafe_vel - turn_vel
        motor2_vel =  forward_vel + strafe_vel - turn_vel
        motor3_vel = -forward_vel - strafe_vel - turn_vel
        motor4_vel = -forward_vel + strafe_vel - turn_vel

        self.hat.drive_motor(self.m1_channel, motor1_vel)
        self.hat.drive_motor(self.m2_channel, motor2_vel)
        self.hat.drive_motor(self.m3_channel, motor3_vel)
        self.hat.drive_motor(self.m4_channel, motor4_vel)

    def stop(self):
        self.hat.stop_all_motors()

if __name__ == "__main__":

    rover = MecanumLandRover()

    for _ in range(10):
        rover.drive(1, 0, 0)
        time.sleep(1)
        rover.drive(0, 0, 0.7)
        time.sleep(2.5)
        rover.drive(0, 1, 0)
        time.sleep(1)
        rover.drive(0, 0, 0.7)
        time.sleep(2)
        rover.drive(0.6, 0.1, 0.3)
        time.sleep(4)

    rover.stop()
