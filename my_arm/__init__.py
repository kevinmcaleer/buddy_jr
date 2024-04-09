from viam.components.arm import Arm
from viam.resource.registry import Registry, ResourceCreatorRegistration
from .my_modular_arm import MyModularArm


Registry.register_resource_creator(Arm.SUBTYPE, MyModularArm.MODEL, ResourceCreatorRegistration(MyModularArm.new))