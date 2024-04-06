import board
import busio
import adafruit_pca9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

# Set the PWM frequency to 60hz
pca.frequency = 60

# Set the duty cycle for channel 0 to 50%
pca.channels[0].duty_cycle = 0x7fff
