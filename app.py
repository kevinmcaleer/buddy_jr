from buddyjr.arm import Arm
from time import sleep
import asyncio

arm = Arm()

# arm.calibrate() # Set all the servo positions to 0


async def main():
    # Reset all parts simultaneously
    await asyncio.gather(
        arm.move_to_async(Arm.CAMERA, 1, 90),
        arm.move_to_async(Arm.ELBOW, 1, 90),
        arm.move_to_async(Arm.BASE, 1, 90),
        arm.move_to_async(Arm.SHOULDER, 1, 90)
    )
    
    await asyncio.sleep(1)  # Use asyncio.sleep for async compatibility

    print('Testing IK')
    x, y = 40, 40
    shoulder_pos, elbow_pos, camera_pos = arm.calculate_position(x, y)
    
    # Move all parts based on IK calculations simultaneously
    await asyncio.gather(
        arm.move_to_async(Arm.SHOULDER, 1, shoulder_pos),
        arm.move_to_async(Arm.ELBOW, 1, elbow_pos),
        arm.move_to_async(Arm.CAMERA, 1, camera_pos),
        arm.move_to_async(Arm.BASE, 1, 0)
    )

    await asyncio.sleep(2)  # Use asyncio.sleep for async compatibility

    # Reset all parts simultaneously again
    await asyncio.gather(
        arm.move_to_async(Arm.CAMERA, 1, 90),
        arm.move_to_async(Arm.ELBOW, 1, 90),
        arm.move_to_async(Arm.BASE, 1, 90),
        arm.move_to_async(Arm.SHOULDER, 1, 90)
    )

    await asyncio.sleep(1)  # Use asyncio.sleep for async compatibility