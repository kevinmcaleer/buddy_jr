import board
import busio
from adafruit_servokit import ServoKit
from time import sleep

# Specify the number of channels on the PCA9685 module
kit = ServoKit(channels=16)

# Initialize I2C bus
i2c = busio.I2C(scl=board.SCL, sda=board.SDA)

# pca = adafruit_pca9685.PCA9685(i2c)
# pca.frequency = 50
# pca.channels[0].duty_cycle = 1500
# pca.channels[1].duty_cycle = 500

# Define servos on specific channels
servo1 = kit.servo[0]
servo2 = kit.servo[1]
servo3 = kit.servo[2]
servo4 = kit.servo[3]

print("Moving the servos")
# Example to set servo to 180 degrees
servo1.angle = 180
servo2.angle = 90
servo3.angle = 90
servo4.angle = 90

sleep(1)

servo1.angle = 0
servo2.angle = 0
servo3.angle = 0
servo4.angle = 0
# Adjust as necessary for your specific servos and desired positions
print("done.")
