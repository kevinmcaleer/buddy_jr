import board
import busio
from adafruit_servokit import ServoKit
from time import sleep
import asyncio
# import time

class Arm():

    BASE = 0
    SHOULDER = 1
    ELBOW = 2
    CAMERA = 3

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
   
    def move_to(self, channel: int, duration: float, target_angle: int):

        if channel > 15:
            raise ValueError(f'The servo channel was greater than 1 - it was {channel}')
        
        if (target_angle) > 180 or (target_angle < 0):
            raise ValueError('The angle value was outside the valid range or 0 to 180')
        current_angle = self.kit.servo[channel].angle

        # Calculate the total distance to move
        angle_difference = target_angle - current_angle

        # Define the number of steps you want to use
        steps = 60

        # Calculate the time to wait between steps to achieve the overall duration
        sleep_duration = duration / steps

        # Calculate the angle to move at each step
        angle_step = angle_difference / steps

        for _ in range(steps):
            # Update the current angle
            current_angle += angle_step
            self.kit.servo[channel].angle = current_angle
            # Wait before the next step
            sleep(sleep_duration)

    async def move_to_async(self, channel: int, duration: float, target_angle: int):
        print(f"Channel is {channel}")
        
        if channel is None:
            raise ValueError("Channel was None, it needs to be a value between 0 and 15")
        
        if channel > 15:
            raise ValueError(f'The servo channel was greater than 1 - it was {channel}')
        
        if (target_angle) > 180 or (target_angle < 0):
            raise ValueError('The angle value was outside the valid range or 0 to 180')
        
        print(f'self.kit.servo[{channel}].angle is {self.kit.servo[channel].angle}')
        current_angle = self.kit.servo[channel].angle

        if current_angle is None:
            current_angle = 0  # or any other value you deem appropriate

        # Calculate the total distance to move
        angle_difference = target_angle - current_angle

        # Define the number of steps you want to use
        steps = 60

        # Calculate the time to wait between steps to achieve the overall duration
        sleep_duration = duration / steps

        # Calculate the angle to move at each step
        angle_step = angle_difference / steps

        for _ in range(steps):
            # Update the current angle
            current_angle += angle_step
            self.kit.servo[channel].angle = current_angle
            # Async wait before the next step
            await asyncio.sleep(sleep_duration)
