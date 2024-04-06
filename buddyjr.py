from adafruit_pca9685 import PCA9685

pca = PCA9685()

# Set the PWM frequency to 60hz
pca.frequency = 60

# Set the duty cycle for channel 0 to 50%
pca.channels[0].duty_cycle = 0x7fff
