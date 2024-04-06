from buddyjr.arm import Arm
from time import sleep
import asyncio

arm = Arm()

# arm.calibrate() # Set all the servo positions to 0


async def main():

    # reset
    await arm.move_to_async(Arm.CAMERA, 1, 90)
    await arm.move_to_async(Arm.ELBOW, 1, 90)
    await arm.move_to_async(Arm.BASE, 1, 90)
    await arm.move_to_async(Arm.SHOULDER, 1, 90)

    sleep(1)

    print('testing IK')
    x = 40
    y = 40
    shoulder_pos, elbow_pos, camera_pos = arm.calculate_position(x,y)
    await arm.move_to_async(Arm.SHOULDER,1,shoulder_pos)
    await arm.move_to_async(Arm.ELBOW,1, elbow_pos)
    await arm.move_to_async(Arm.CAMERA, 1, camera_pos)
    await arm.move_to_async(Arm.BASE, 1, 0)

    sleep(2)

     # reset
    await arm.move_to_async(Arm.CAMERA, 1, 90)
    await arm.move_to_async(Arm.ELBOW, 1, 90)
    await arm.move_to_async(Arm.BASE, 1, 90)
    await arm.move_to_async(Arm.SHOULDER, 1, 90)

    sleep(1)

asyncio.run(main())