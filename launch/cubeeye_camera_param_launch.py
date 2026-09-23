import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.substitutions import FindExecutable
from launch.event_handlers import OnProcessStart, OnProcessExit

def generate_launch_description():
    pkg_share = get_package_share_directory('cubeeye_camera')
    config_file_path = os.path.join(pkg_share, 'config', 'configurazione_pcl_depth_intensity.yaml')

    with open(config_file_path, 'r') as f:
        config = yaml.safe_load(f)
        frametype = config['cubeeye_camera_node']['ros__parameters']['autorun_frametype']

    cubeeye_node = Node(
        package='cubeeye_camera',
        executable='cubeeye_camera_node',
        name='cubeeye_camera_node', 
        output='screen',
        parameters=[config_file_path] 
    )

    camera_scan_call_cmd = ExecuteProcess(
        cmd=[
            FindExecutable(name='ros2'),
            'service', 'call',
            '/cubeeye_camera_node/scan',
            'cubeeye_camera/srv/Scan'
        ],
        shell=False
    )

    camera_connect_call_cmd = ExecuteProcess(
        cmd=[
            FindExecutable(name='ros2'),
            'service', 'call',
            '/cubeeye_camera_node/connect',
            'cubeeye_camera/srv/Connect',
            '{index: 0}'
        ],
        shell=False
    )

    camera_run_call_cmd = ExecuteProcess(
        cmd=[
            FindExecutable(name='ros2'),
            'service', 'call',
            '/cubeeye_camera_node/run',
            'cubeeye_camera/srv/Run',
            f'{{type: {frametype}}}'
        ],
        shell=False
    )

    return LaunchDescription([
        cubeeye_node,

        # 1. Start Scan when the camera node starts
        RegisterEventHandler(
            OnProcessStart(
                target_action=cubeeye_node,
                on_start=[camera_scan_call_cmd]
            )
        ),

        # 2. Start Connect ONLY after Scan completes and exits
        RegisterEventHandler(
            OnProcessExit(
                target_action=camera_scan_call_cmd,
                on_exit=[camera_connect_call_cmd]
            )
        ),

        # 3. Start Run ONLY after Connect completes and exits
        RegisterEventHandler(
            OnProcessExit(
                target_action=camera_connect_call_cmd,
                on_exit=[camera_run_call_cmd]
            )
        )
    ])