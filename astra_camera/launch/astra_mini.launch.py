from launch import LaunchDescription
from ament_index_python import get_package_share_directory
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import yaml


def generate_launch_description():
    namespace = LaunchConfiguration('namespace')

    namespace_launch_arg = DeclareLaunchArgument(
        'namespace',
        default_value='astra'
    )
    params_file = get_package_share_directory(
        "astra_camera") + "/params/astra_mini_params.yaml"
    with open(params_file, 'r') as file:
        config_params = yaml.safe_load(file)
    container = ComposableNodeContainer(
        name='astra_camera_container',
        namespace=namespace,
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            ComposableNode(package='astra_camera',
                           plugin='astra_camera::OBCameraNodeFactory',
                           name='camera',
                           namespace=namespace,
                           parameters=[config_params]),
            ComposableNode(package='astra_camera',
                           plugin='astra_camera::PointCloudXyzNode',
                           namespace=namespace,
                           name='point_cloud_xyz'),
            ComposableNode(package='astra_camera',
                           plugin='astra_camera::PointCloudXyzrgbNode',
                           namespace=namespace,
                           name='point_cloud_xyzrgb')
        ],
        output='screen')
    return LaunchDescription([namespace_launch_arg,
                              container
                              ])
