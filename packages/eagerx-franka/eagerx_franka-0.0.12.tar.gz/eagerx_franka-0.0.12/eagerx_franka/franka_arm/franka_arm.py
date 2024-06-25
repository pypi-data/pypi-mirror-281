import eagerx
from eagerx import Space
from eagerx_pybullet.engine import PybulletEngine
from eagerx_reality.engine import RealEngine
from eagerx.core.specs import ObjectSpec
from eagerx.core.graph_engine import EngineGraph
import eagerx.core.register as register
import eagerx_franka
from eagerx_franka.utils import generate_urdf, get_joint_limits

import os

try:
    from urdf_parser_py.urdf import URDF
except ImportError:
    print("Please install urdf_parser_py")


class FrankaArm(eagerx.Object):
    @classmethod
    @register.sensors(
        position=Space(dtype="float32"),
        velocity=Space(dtype="float32"),
        force_torque=Space(low=-20, high=20, shape=(6,), dtype="float32"),
        gripper_position=Space(dtype="float32"),
        ee_pos=Space(low=[-2, -2, 0], high=[2, 2, 2], dtype="float32"),
        ee_orn=Space(low=-1, high=1, shape=(4,), dtype="float32"),
        moveit_status=Space(low=0, high=1, shape=(), dtype="int64"),
    )
    @register.actuators(
        pos_control=Space(dtype="float32"),
        vel_control=Space(dtype="float32"),
        gripper_control=Space(low=[0], high=[1], dtype="float32"),
        moveit_to=Space(dtype="float32"),
        moveit_to_ee_pose=Space(dtype="float32"),
    )
    @register.engine_states(
        ee_pose=Space(low=[-2, -2, 0, -1, -1, -1, -1], high=[2, 2, 2, 1, 1, 1, 1], dtype="float32"),
        position=Space(dtype="float32"),
        velocity=Space(dtype="float32"),
        gripper=Space(low=[0.5], high=[0.5], dtype="float32"),
    )
    def make(
        cls,
        name: str,
        robot_type: str,
        arm_name=None,
        sensors=None,
        actuators=None,
        states=None,
        rate=30,
        base_pos=None,
        base_or=None,
        self_collision=False,
        fixed_base=True,
        joint_limits=None,
        regenerate_urdf=False,
    ) -> ObjectSpec:
        """Object spec of FrankaArm"""
        if URDF is None:
            raise ImportError("Ros not installed. Required for generating urdf.")

        spec = cls.get_specification()
        joint_limits = get_joint_limits(robot_type, joint_limits)

        # Extract info on franka arm from assets
        if regenerate_urdf:
            urdf = URDF.from_parameter_server(generate_urdf(robot_type, ns="pybullet_urdf"))
        else:
            module_path = os.path.dirname(eagerx_franka.__file__) + "/assets/"
            urdf = URDF.from_xml_file(module_path + "franka_panda/panda.urdf")

        gripper_names = [joint.name for joint in urdf.joints if "finger" in joint.name]
        gripper_link = [link.name for link in urdf.links if f"{robot_type}_link8" in link.name][0]
        gripper_link = [link.name for link in urdf.links if f"{robot_type}_grasptarget" in link.name][0]

        # Determine joint limits
        joint_names = []
        joint_lower, joint_upper, vel_limit = [], [], []
        for n in joint_limits.keys():
            joint_names.append(f"{robot_type}_{n}")
            joint_obj = next((joint for joint in urdf.joints if joint.name == f"{robot_type}_{n}"), None)
            joint_lower.append(joint_obj.limit.lower)
            joint_upper.append(joint_obj.limit.upper)
            vel_limit.append(joint_obj.limit.velocity)

        # Determine gripper limits
        gripper_lower, gripper_upper = [], []
        for n in gripper_names:
            joint_obj = next((joint for joint in urdf.joints if joint.name == n), None)
            gripper_lower.append(joint_obj.limit.lower)
            gripper_upper.append(joint_obj.limit.upper)

        # Modify default config
        spec.config.name = name
        spec.config.sensors = sensors if isinstance(sensors, list) else ["position", "velocity"]
        spec.config.actuators = actuators if isinstance(actuators, list) else ["pos_control", "gripper_control"]
        spec.config.states = states if isinstance(states, list) else ["position", "velocity", "gripper"]

        # Add registered config params
        spec.config.robot_type = robot_type
        spec.config.arm_name = arm_name if arm_name else robot_type
        spec.config.joint_names = joint_names
        spec.config.gripper_names = gripper_names
        spec.config.gripper_link = gripper_link
        spec.config.gripper_lower = gripper_lower
        spec.config.gripper_upper = gripper_upper
        spec.config.base_pos = base_pos if base_pos else [0, 0, 0]
        spec.config.base_or = base_or if base_or else [0, 0, 0, 1]
        spec.config.self_collision = self_collision
        spec.config.fixed_base = fixed_base
        spec.config.joint_limits = joint_limits
        spec.config.joint_lower = joint_lower
        spec.config.joint_upper = joint_upper
        spec.config.vel_limit = vel_limit
        spec.config.urdf = urdf.to_xml_string()
        spec.config.regenerate_urdf = regenerate_urdf
        spec.config.sleep_positions = [0.0 for _j in joint_lower]

        # Set rates
        spec.sensors.position.rate = rate
        spec.sensors.velocity.rate = rate
        spec.sensors.force_torque.rate = rate
        spec.sensors.gripper_position.rate = rate
        spec.sensors.ee_pos.rate = rate
        spec.sensors.ee_orn.rate = rate
        spec.sensors.moveit_status.rate = rate
        spec.actuators.pos_control.rate = rate
        spec.actuators.moveit_to.rate = rate
        spec.actuators.moveit_to_ee_pose.rate = rate
        spec.actuators.vel_control.rate = rate
        spec.actuators.gripper_control.rate = 1

        # Set variable spaces
        spec.sensors.position.space.update(low=joint_lower, high=joint_upper)
        spec.sensors.velocity.space.update(low=[-v for v in vel_limit], high=vel_limit)
        spec.sensors.ee_pos.rate = rate
        spec.sensors.ee_orn.rate = rate
        spec.sensors.gripper_position.space.update(low=[gripper_lower[0] * 0.9], high=[gripper_upper[0] * 1.1])
        spec.actuators.pos_control.space.update(low=joint_lower, high=joint_upper)
        spec.actuators.vel_control.space.update(low=[-v for v in vel_limit], high=vel_limit)
        spec.actuators.moveit_to.space.update(low=joint_lower, high=joint_upper)
        spec.actuators.moveit_to_ee_pose.space.update(low=[-2, -2, 0, -1, -1, -1, -1], high=[2, 2, 2, 1, 1, 1, 1])
        spec.states.position.space.update(low=[0.0 for _j in joint_lower], high=[0.0 for _j in joint_upper])
        spec.states.velocity.space.update(low=[0.0 for _j in joint_lower], high=[0.0 for _j in joint_upper])
        return spec

    @staticmethod
    @register.engine(PybulletEngine)
    def pybullet_engine(spec: ObjectSpec, graph: EngineGraph):
        import pybullet as pb

        """Engine-specific implementation (Pybullet) of the object."""
        # Set object arguments (as registered per register.engine_params(..) above the engine.add_object(...) method.)

        module_path = os.path.dirname(eagerx_franka.__file__) + "/assets/franka_panda/"
        urdf = spec.config.urdf
        if not spec.config.regenerate_urdf:
            urdf_sbtd = urdf.replace("package://", module_path)
            spec.engine.urdf = urdf_sbtd
        else:
            spec.engine.urdf = urdf
        spec.engine.basePosition = spec.config.base_pos
        spec.engine.baseOrientation = spec.config.base_or
        spec.engine.fixed_base = spec.config.fixed_base
        spec.engine.self_collision = spec.config.self_collision
        spec.engine.flags = pb.URDF_ENABLE_CACHED_GRAPHICS_SHAPES

        lower = spec.config.gripper_lower
        upper = spec.config.gripper_upper
        constant = abs(float(lower[0]))
        scale = float(upper[0]) - float(lower[0])

        # Create engine_states (no agnostic states defined in this case)
        from eagerx_franka.franka_arm.pybullet.enginestates import FrankaGripper, PoseState
        from eagerx_pybullet.enginestates import JointState

        joints = spec.config.joint_names
        spec.engine.states.gripper = FrankaGripper.make(spec.config.gripper_names, constant, scale)
        spec.engine.states.ee_pose = PoseState.make(
            joints=spec.config.joint_names,
            upper=spec.config.joint_upper,
            lower=spec.config.joint_lower,
            ee_link=spec.config.gripper_link,
            rest_poses=spec.config.sleep_positions,
        )
        spec.engine.states.position = JointState.make(joints=joints, mode="position")
        spec.engine.states.velocity = JointState.make(joints=joints, mode="velocity")

        # Fix gripper if we are not controlling it.
        if "gripper_control" not in spec.config.actuators:
            spec.engine.states.gripper.fixed = True

        # Create sensor engine nodes
        from eagerx_pybullet.enginenodes import LinkSensor, JointSensor, JointController
        from eagerx_franka.franka_arm.pybullet.enginenodes import MoveItController, TaskSpaceControl

        pos_sensor = JointSensor.make("pos_sensor", rate=spec.sensors.position.rate, process=2, joints=joints, mode="position")
        vel_sensor = JointSensor.make("vel_sensor", rate=spec.sensors.velocity.rate, process=2, joints=joints, mode="velocity")
        ft_sensor = JointSensor.make(
            "ft_sensor",
            rate=spec.sensors.force_torque.rate,
            process=2,
            joints=[spec.config.joint_names[-1]],
            mode="force_torque",
        )

        gripper_sensor = JointSensor.make(
            "gripper_sensor",
            rate=spec.sensors.gripper_position.rate,
            joints=spec.config.gripper_names[:1],
            mode="position",
        )

        ee_pos_sensor = LinkSensor.make(
            "ee_pos_sensor",
            rate=spec.sensors.ee_pos.rate,
            links=[spec.config.gripper_link],
            mode="position",
        )
        ee_orn_sensor = LinkSensor.make(
            "ee_orn_sensor",
            rate=spec.sensors.ee_orn.rate,
            links=[spec.config.gripper_link],
            mode="orientation",
        )

        # Create actuator engine nodes
        # Rate=None, but we will connect it to an actuator (thus will use the rate set in the agnostic specification)
        pos_control = JointController.make(
            "pos_control",
            rate=spec.actuators.pos_control.rate,
            joints=joints,
            mode="position_control",
            vel_target=len(joints) * [0.0],
            pos_gain=len(joints) * [0.5],
            vel_gain=len(joints) * [1.0],
            max_vel=[0.5 * vel for vel in spec.config.vel_limit],
            max_force=len(joints) * [2.5],
        )
        vel_control = JointController.make(
            "vel_control",
            rate=spec.actuators.vel_control.rate,
            joints=joints,
            mode="velocity_control",
            vel_gain=len(joints) * [1.0],
            max_force=len(joints) * [5.0],  # todo: limit?
        )

        gripper = JointController.make(
            "gripper_control",
            rate=spec.actuators.gripper_control.rate,
            joints=spec.config.gripper_names,
            mode="position_control",
            vel_target=[0.0, 0.0],
            pos_gain=[0.1, 0.1],
            vel_gain=[1.0, 1.0],
            max_force=[2.0, 2.0],
        )

        moveit_to = MoveItController.make(
            "moveit_to",
            rate=spec.actuators.moveit_to.rate,
            joints=joints,
            vel_target=len(joints) * [0.0],
            pos_gain=len(joints) * [0.5],
            vel_gain=len(joints) * [1.0],
            max_vel=[0.5 * vel for vel in spec.config.vel_limit],
            max_force=len(joints) * [5.0],
        )

        ik_ee_pose = TaskSpaceControl.make(
            "task_space",
            rate=spec.actuators.moveit_to_ee_pose.rate,
            joints=spec.config.joint_names,
            upper=spec.config.joint_upper,
            lower=spec.config.joint_lower,
            ee_link=spec.config.gripper_link,
            rest_poses=spec.config.sleep_positions,
        )

        moveit_to_ee_pose = MoveItController.make(
            "moveit_to_ee_pose",
            rate=spec.actuators.moveit_to_ee_pose.rate,
            joints=joints,
            vel_target=len(joints) * [0.0],
            pos_gain=len(joints) * [0.5],
            vel_gain=len(joints) * [1.0],
            max_vel=[0.5 * vel for vel in spec.config.vel_limit],
            max_force=len(joints) * [5.0],
        )

        from eagerx_franka.franka_arm.processor import MirrorAction

        gripper.inputs.action.processor = MirrorAction.make(index=0, constant=constant, scale=scale)

        # Connect all engine nodes
        graph.add(
            [
                pos_sensor,
                vel_sensor,
                ft_sensor,
                ee_pos_sensor,
                ee_orn_sensor,
                gripper_sensor,
                pos_control,
                vel_control,
                gripper,
                moveit_to,
                ik_ee_pose,
                moveit_to_ee_pose,
            ]
        )
        graph.connect(source=pos_sensor.outputs.obs, sensor="position")
        graph.connect(source=vel_sensor.outputs.obs, sensor="velocity")
        graph.connect(source=ft_sensor.outputs.obs, sensor="force_torque")
        graph.connect(source=ee_pos_sensor.outputs.obs, sensor="ee_pos")
        graph.connect(source=ee_orn_sensor.outputs.obs, sensor="ee_orn")
        graph.connect(source=gripper_sensor.outputs.obs, sensor="gripper_position")
        graph.connect(source=moveit_to.outputs.status, sensor="moveit_status")
        graph.connect(actuator="pos_control", target=pos_control.inputs.action)
        graph.connect(actuator="vel_control", target=vel_control.inputs.action)
        graph.connect(actuator="gripper_control", target=gripper.inputs.action)
        graph.connect(actuator="moveit_to", target=moveit_to.inputs.action)
        graph.connect(actuator="moveit_to_ee_pose", target=ik_ee_pose.inputs.ee_pose)
        graph.connect(source=ik_ee_pose.outputs.goal, target=moveit_to_ee_pose.inputs.action)

    @staticmethod
    @register.engine(RealEngine)
    def reality_engine(spec: ObjectSpec, graph: EngineGraph):
        """Engine-specific implementation (reality) of the object."""
        # Determine gripper min/max
        from eagerx_franka.franka_arm.real.enginestates import DummyState

        spec.engine.states.position = DummyState.make()
        spec.engine.states.velocity = DummyState.make()
        spec.engine.states.gripper = DummyState.make()
        spec.engine.states.ee_pose = DummyState.make()

        # Create sensor engine nodes
        from eagerx_franka.franka_arm.real.enginenodes import FrankaSensor, FrankaGripper, TaskSpaceControl

        joints = spec.config.joint_names
        robot_type = spec.config.robot_type
        arm_name = spec.config.arm_name

        # todo: set space to limits (pos=joint_limits, vel=vel_limits, effort=[-1, 1]?)
        pos_sensor = FrankaSensor.make(
            "pos_sensor",
            rate=spec.sensors.position.rate,
            joints=joints,
            mode="position",
            arm_name=arm_name,
            robot_type=robot_type,
        )
        ee_pos_sensor = FrankaSensor.make(
            "ee_pos_sensor",
            rate=spec.sensors.ee_pos.rate,
            joints=joints,
            mode="ee_position",
            arm_name=arm_name,
            robot_type=robot_type,
        )
        ee_orn_sensor = FrankaSensor.make(
            "ee_orn_sensor",
            rate=spec.sensors.ee_orn.rate,
            joints=joints,
            mode="ee_orientation",
            arm_name=arm_name,
            robot_type=robot_type,
        )
        vel_sensor = FrankaSensor.make(
            "vel_sensor",
            rate=spec.sensors.velocity.rate,
            joints=joints,
            mode="velocity",
            arm_name=arm_name,
            robot_type=robot_type,
        )
        gripper_sensor = FrankaSensor.make(
            "gripper_sensor",
            rate=spec.sensors.gripper_position.rate,
            joints=joints,
            mode="gripper_position",
            arm_name=arm_name,
            robot_type=robot_type,
        )

        gripper = FrankaGripper.make(
            "gripper_control",
            rate=spec.actuators.gripper_control.rate,
            arm_name=arm_name,
            robot_type=robot_type,
        )

        task_space_control = TaskSpaceControl.make(
            "task_space_control",
            rate=spec.actuators.moveit_to_ee_pose.rate,
            arm_name=arm_name,
            robot_type=robot_type,
        )

        # Connect all engine nodes
        graph.add(
            [
                pos_sensor,
                vel_sensor,
                ee_pos_sensor,
                ee_orn_sensor,
                gripper_sensor,
                task_space_control,
                gripper,
            ]
        )
        graph.connect(source=pos_sensor.outputs.obs, sensor="position")
        graph.connect(source=vel_sensor.outputs.obs, sensor="velocity")
        graph.connect(source=ee_pos_sensor.outputs.obs, sensor="ee_pos")
        graph.connect(source=ee_orn_sensor.outputs.obs, sensor="ee_orn")
        graph.connect(source=gripper_sensor.outputs.obs, sensor="gripper_position")
        graph.connect(actuator="gripper_control", target=gripper.inputs.action)
        graph.connect(actuator="moveit_to_ee_pose", target=task_space_control.inputs.ee_pose)
