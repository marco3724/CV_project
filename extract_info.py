
import sys
import os

# Add the current directory or a specific directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'blender_scripts'))

from setup_env import setup_env
from extract_3D_coordinates import extract_3d_coordinates
from projection_2D import projection

fbx_file_path = "./assets/GiuliaRigged.fbx"
camera,armature = setup_env(fbx_file_path)


output_base_dir = "./out"

bone_pairs_path =output_base_dir + "/bone_pairs.txt"
output_coordinates_3D_path = output_base_dir + "/bones_3D_coordinates.txt"
bone_coordinates_3d = extract_3d_coordinates(armature,output_coordinates_3D_path,bone_pairs_path)


output_file_path_2d = output_base_dir + "/bones_2D_coordinates.txt"
output_render = output_base_dir + "/render.png"
projection(camera,bone_coordinates_3d,output_file_path_2d,output_render)