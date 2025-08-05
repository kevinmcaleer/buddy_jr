from Adafruit_PCA9685 import PCA9685

pca = PCA9685()

class Servo():
    def __init__(self, channel):
        self.channel = channel
        self.pca = pca
        self.pca.channels[channel].duty_cycle = 0x7fff

    @property
    def duty_cycle(self):
        return self.pca.channels[self.channel].duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value):
        self.pca.channels[self.channel].duty_cycle = value

    @property
    def angle(self):
        return int((self.duty_cycle - 0x1fff) * 180 / 0x3fff)

    @angle.setter
    def angle(self, value):
        self.duty_cycle = int(0x1fff + value * 0x3fff / 180)

    def move(self, angle):
        self.angle = angle

    def __str__(self):
        return f"Servo({self.channel})"

    def __repr__(self):
        return f"Servo({self.channel})"

class Arm():

    BASE = 0
    SHOULDER = 1
    ELBOW = 2
    CAMERA = 3
    def __init__(self):
        self.pca = PCA9685()
        self.pca.frequency = 50

        # Map the Servos to PCA channels
        self.shoulder = self.pca.channels[self.SHOULDER]
        self.elbow = self.pca.channels[self.ELBOW]
        self.camera = self.pca.channels[self.CAMERA]
        self.base = self.pca.channels[self.BASE]

    