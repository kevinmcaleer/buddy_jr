import asyncio
import os
from typing import Any, ClassVar, Dict, Mapping, Optional, Tuple, cast
from typing_extensions import Self

from viam.components.arm import Arm, JointPositions, KinematicsFileFormat, Pose
from viam.operations import run_with_operation
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.utils import struct_to_dict
from viam.components.servo import Servo
from viam.logging import getLogger

# TODO: Rename Camera to Head (the joint)

LOGGER = getLogger(__file__)

# TODO: #1 add some return values to the functions, such as move_to_position, get_end_position, etc.

class MyModularArm(Arm):
    # Subclass the Viam Arm component and implement the required functions
    MODEL: ClassVar[Model] = Model(ModelFamily("kevsrobots", "arm"), "buddy_jr")

    joints = []

    def __init__(self, name: str):
        # Starting joint positions
        # Base, Shoulder, Elbow, Camera

        self.joint_positions = JointPositions(values=[90, 90, 90, 90])
        super().__init__(name)
        self.is_stopped = True

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        arm = cls(config.name)

        # Need to do this when running code
        arm.reconfigure(config, dependencies)

        # Add the arm.reconfigure(config, dependencies) call here
        return arm

    async def get_end_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Pose:

        raise NotImplementedError()

    async def move_to_position(self, pose: Pose, extra: Optional[Dict[str, Any]] = None, **kwargs):
        
        raise NotImplementedError()

    async def get_joint_positions(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> JointPositions:
        
        # Base
        # Shoulder
        # Elbow
        # Camera

        # Joint Position is 0 - 180, 
        LOGGER.info("joint positions - setting new joint array")
        LOGGER.info(f"joint positions - self.joints is {self.joints}")

        new_list = []
        for joint in self.joints:
            position = await joint.get_position()
            LOGGER.info(f"joint position is {position}")
            new_list.append(int(position))
        
        LOGGER.info(f"joint positions {new_list}")

        self.joint_positions = JointPositions(values=new_list)

        return self.joint_positions

    @run_with_operation
    async def move_to_joint_positions(self, positions: JointPositions, extra: Optional[Dict[str, Any]] = None, **kwargs):
        operation = self.get_operation(kwargs)

        self.is_stopped = False

        new_positions = positions.values

        for index, joint in enumerate(self.joints):
            await joint.move(int(new_positions[index]))

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
    
    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        attributes_dict = struct_to_dict(config.attributes)
        base_name = attributes_dict.get("base_servo")
        shoulder_name = attributes_dict.get("shoulder_servo")
        camera_name = attributes_dict.get("camera_servo")
        elbow_name = attributes_dict.get("elbow_servo")

        assert isinstance(camera_name, str) and isinstance(elbow_name, str)

        # set the servo class instead of Motor
        camera_servo = dependencies[Servo.get_resource_name(camera_name)]
        elbow_servo = dependencies[Servo.get_resource_name(elbow_name)]
        shoulder_servo = dependencies[Servo.get_resource_name(shoulder_name)]
        base_servo = dependencies[Servo.get_resource_name(base_name)]

        self.joints.append(cast(Servo, base_servo))
        self.joints.append(cast(Servo, shoulder_servo))
        self.joints.append(cast(Servo, elbow_servo))
        self.joints.append(cast(Servo, camera_servo))

        # self.camera_servo = cast(Servo, camera_servo)
        # self.elbow_servo = cast(Servo, elbow_servo)