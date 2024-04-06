from buddyjr.arm import Arm
from time import sleep
import asyncio

arm = Arm()

# arm.calibrate() # Set all the servo positions to 0


async def main():

    # await arm.calibrate_async()

    await arm.move_to_async(Arm.CAMERA, 1, 180)
    await arm.move_to_async(Arm.ELBOW, 1, 180)

    sleep(5)

    await arm.move_to_async(Arm.CAMERA, 1, 0)
    await arm.move_to_async(Arm.ELBOW, 1, 0)

    # arm.camera.angle = 0

asyncio.run(main())