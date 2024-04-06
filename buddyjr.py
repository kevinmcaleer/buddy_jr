import board
import busio
import adafruit_pca9685
from time import sleep
import adafruit_motor.servo 
from adafruit_servokit import ServoKit


i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

# Set the PWM frequency to 50hz
pca.frequency = 50

# Set the duty cycle for channel 0 to 50%
pca.channels[1].duty_cycle = 150
pca.channels[2].duty_cycle = 1000

kit = ServoKit(channels=16)
channel = 1

servo = adafruit_motor.servo.Servo(pca)
servo.actuation_range = 135

# servo = adafruit_motor.servo.Servo(channel)

kit.servo[channel].angle = 45

kit.servo[2].angle = 90  
sleep(1)

kit.servo[channel].angle = 90

