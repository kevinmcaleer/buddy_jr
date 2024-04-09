import asyncio
import os
from typing import Any, ClassVar, Dict, Mapping, Optional, Tuple
from typing_extensions import Self

from viam.components.arm import Arm, JointPositions, KinematicsFileFormat, Pose
from viam.operations import run_with_operation
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily


class MyModularArm(Arm):
    # Subclass the Viam Arm component and implement the required functions
    MODEL: ClassVar[Model] = Model(ModelFamily("KevsRobots", "Buddy Jr"), "myarm")

    def __init__(self, name: str):
        # Starting joint positions
        self.joint_positions = JointPositions(values=[90, 90, 90, 90])
        super().__init__(name)

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        arm = cls(config.name)
        return arm

    async def get_end_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Pose:
        raise NotImplementedError()

    async def move_to_position(self, pose: Pose, extra: Optional[Dict[str, Any]] = None, **kwargs):
        raise NotImplementedError()

    async def get_joint_positions(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> JointPositions:
        return self.joint_positions

    @run_with_operation
    async def move_to_joint_positions(self, positions: JointPositions, extra: Optional[Dict[str, Any]] = None, **kwargs):
        operation = self.get_operation(kwargs)

        self.is_stopped = False

        # Simulate the length of time it takes for the arm to move to its new joint position
        for x in range(10):
            await asyncio.sleep(1)

            # Check if the operation is cancelled and, if it is, stop the arm's motion
            if await operation.is_cancelled():
                await self.stop()
                break

        self.joint_positions = positions
        self.is_stopped = True

    async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self.is_stopped = True

    async def is_moving(self) -> bool:
        return not self.is_stopped

    async def get_kinematics(self, **kwargs) -> Tuple[KinematicsFileFormat.ValueType, bytes]:
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, "./buddy_udrf.xml")
        with open(filepath, mode="rb") as f:
            file_data = f.read()
        return (KinematicsFileFormat.KINEMATICS_FILE_FORMAT_URDF, file_data)