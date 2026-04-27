import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

# Launch camera node and configure it using the configurazione.yaml file
def generate_launch_description():
    # 1. Get the path to the cubeeye_camera package
    pkg_share = get_package_share_directory('cubeeye_camera')

    # 2. Construct the full path to your YAML file
    # (Assuming it is placed inside a 'config' folder in your package)
    config_file_path = os.path.join(pkg_share, 'config', 'configurazione.yaml')

    # 3. Define the camera node
    cubeeye_node = Node(
        package='cubeeye_camera',
        executable='cubeeye_camera_node',
        name='cubeeye_camera_node', # Note: Your YAML file MUST use this exact name
        output='screen',
        parameters=[config_file_path] # Pass the YAML file path here
    )
    

    return LaunchDescription([
        cubeeye_node,
    ])