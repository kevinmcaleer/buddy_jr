from buddyjr.arm import Arm
from time import sleep
import asyncio

arm = Arm()

# arm.calibrate() # Set all the servo positions to 0


async def main():

    # await arm.calibrate_async()

    print('setting camera and below')
    await arm.move_to_async(Arm.CAMERA, 1, 180)
    await arm.move_to_async(Arm.ELBOW, 1, 180)

    sleep(5)

    print('part 2')
    await arm.move_to_async(Arm.CAMERA, 1, 0)
    await arm.move_to_async(Arm.ELBOW, 1, 0)

    sleep(0.5)

    await arm.move_to_async(Arm.CAMERA, 1, 90)
    await arm.move_to_async(Arm.ELBOW, 1, 90)
    await arm.move_to_async(Arm.BASE, 1, 90)
    await arm.move_to_async(Arm.SHOULDER, 1, 90)

    # arm.camera.angle = 0

asyncio.run(main())