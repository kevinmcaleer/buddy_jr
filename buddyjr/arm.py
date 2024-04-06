import board
import busio
from adafruit_servokit import ServoKit
from time import sleep
import asyncio
from math import atan2, sqrt, pi, acos, degrees

# import time

class Arm():

    BASE = 0
    SHOULDER = 1
    ELBOW = 2
    CAMERA = 3

    # Base is the 0,0 origin
    SHOLDER_LENGTH = 80
    ELBOW_LENGTH = 80

    def __init__(self):
        self.kit = ServoKit(channels=16)

        self.base = self.kit.servo[self.BASE]
        self.shoulder = self.kit.servo[self.SHOULDER]
        self.elbow = self.kit.servo[self.ELBOW]
        self.camera = self.kit.servo[self.CAMERA]
        self.base.angle = 90
        self.shoulder.angle = 90
        self.elbow.angle = 90
        self.camera = 90

    def calibrate(self):
        self.base.angle = 90
        self.shoulder.angle = 90
        self.elbow.angle = 90
        self.camera.angle = 90

    async def calibrate_async(self):
        print('Calibrating')
        print('setting base')
        await self.move_to_async(channel = self.BASE, duration=2, target_angle=90)
        print('setting shoulder')
        await self.move_to_async(self.SHOULDER, 2, 90)
        print('setting elbow')
        await self.move_to_async(self.ELBOW, 2, 90)
        print('setting camera')
        await self.move_to_async(self.CAMERA, 2, 90)
   
    async def move_to_async(self, channel: int, duration: float, target_angle: int):
        print(f"Channel is {channel}")
        
        if channel > 15:
            raise ValueError(f'The servo channel was greater than 1 - it was {channel}')
        
        if (target_angle) > 180 or (target_angle < 0):
            # raise ValueError(f'The angle value was outside the valid range or 0 to 180 - was {target_angle}')
            target_angle = 0
        
        print(f'self.kit.servo[{channel}].angle is {self.kit.servo[channel].angle}')
        current_angle = round(self.kit.servo[channel].angle,0)

        if current_angle is None:
            current_angle = 0  # or any other value you deem appropriate

        # Calculate the total distance to move
        angle_difference = target_angle - current_angle

        # Define the number of steps you want to use
        steps = 1000

        # Calculate the time to wait between steps to achieve the overall duration
        sleep_duration = duration / steps

        # Calculate the angle to move at each step
        angle_step = angle_difference / steps

        range_limit = self.kit.servo[channel].actuation_range
        for _ in range(steps):
            # Update the current angle
            current_angle += angle_step

            if current_angle > range_limit or current_angle < 0:
                continue
            self.kit.servo[channel].angle = current_angle
            # Async wait before the next step
            await asyncio.sleep(sleep_duration)

    import math

    def calculate_position(self, x, y):
        """ Returns Shoulder, Elbow and Camera angles to move to"""
        shoulder_length = self.SHOLDER_LENGTH
        elbow_length = self.ELBOW_LENGTH

        # Calculate distance to target point
        d = sqrt(x**2 + y**2)

        # Law of Cosines to find angles
        angle_to_target = atan2(y, x)
        cos_angle_shoulder = (shoulder_length**2 + d**2 - elbow_length**2) / (2 * shoulder_length * d)
        shoulder_angle = acos(cos_angle_shoulder) + angle_to_target

        cos_angle_elbow = (shoulder_length**2 + elbow_length**2 - d**2) / (2 * shoulder_length * elbow_length)
        elbow_angle = acos(cos_angle_elbow)

        # Assuming a simple scenario where the camera angle needs to compensate the shoulder and elbow movement
        # to stay level. This needs adjustment based on your setup.
        camera_angle = -(shoulder_angle + elbow_angle - pi/2) 
        print(f'Cam angle: {degrees(camera_angle)}')

        # Convert radians to degrees if necessary
        shoulder_angle_deg = degrees(shoulder_angle)
        elbow_angle_deg = degrees(elbow_angle)
        camera_angle_deg = degrees(camera_angle) + 90
        # camera_angle_deg = degrees(camera_angle)  

        return shoulder_angle_deg, elbow_angle_deg, camera_angle_deg

