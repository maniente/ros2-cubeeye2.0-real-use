import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

# Launch camera node (with YAML config) AND the image processing pipeline
def generate_launch_description():
    # 1. Trova il percorso del pacchetto e del file YAML
    pkg_share = get_package_share_directory('cubeeye_camera')
    config_file_path = os.path.join(pkg_share, 'config', 'configurazione.yaml')

    # 2. Definisci il nodo base della telecamera (che carica i parametri)
    cubeeye_node = Node(
        package='cubeeye_camera',
        executable='cubeeye_camera_node',
        name='cubeeye_camera_node', # IMPORTANTE: Deve corrispondere all'intestazione nel file YAML
        output='screen',
        parameters=[config_file_path] # Carica i parametri da configurazione.yaml
    )

    # 3. Container per l'elaborazione delle immagini (Zero-Copy)
    image_pipeline_container = ComposableNodeContainer(
        name='image_pipeline_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            
            # --- A. Nodo di Rettifica (image_proc) ---
            ComposableNode(
                package='image_proc',
                plugin='image_proc::RectifyNode',
                name='rectify_depth_node',
                remappings=[
                    # INPUT: prende i dati raw dalla telecamera
                    ('image', '/cubeeye_camera_node/depth'),
                    ('camera_info', '/cubeeye_camera_node/camera_info'),
                    # OUTPUT: pubblica l'immagine corretta
                    ('image_rect', '/cubeeye_camera_node/depth_rectified')
                ],
            ),
            
            # --- B. Nodo di Creazione PointCloud (depth_image_proc) ---
            ComposableNode(
                package='depth_image_proc',
                plugin='depth_image_proc::PointCloudXyzNode',
                name='point_cloud_xyz_node',
                remappings=[
                    # INPUT: prende l'immagine rettificata dal nodo precedente
                    ('image_rect', '/cubeeye_camera_node/depth_rectified'),
                    ('camera_info', '/cubeeye_camera_node/camera_info'),
                    # OUTPUT: pubblica i punti 3D elaborati
                    ('points', '/cubeeye_camera_node/points_from_image') 
                ],
            ),
        ],
        output='screen',
    )

    # 4. Ritorna il LaunchDescription con entrambi gli elementi
    return LaunchDescription([
        cubeeye_node,
        image_pipeline_container
    ])