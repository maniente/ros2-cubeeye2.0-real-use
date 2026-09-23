import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    pkg_share = get_package_share_directory('cubeeye_camera')
    config_file_path = os.path.join(pkg_share, 'config', 'configurazione_autolaunch.yaml')
    urdf_path = os.path.join(pkg_share, 'urdf', 'camera.urdf')
    with open(urdf_path, 'r') as infp:
        robot_description_content = infp.read()

    cubeeye_node = Node(
        package='cubeeye_camera',
        executable='cubeeye_camera_node',
        name='cubeeye_camera_node', 
        output='screen',
        parameters=[config_file_path] 
    )

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content
        }]
    )
    return LaunchDescription([
        cubeeye_node,
        node_robot_state_publisher
    ])