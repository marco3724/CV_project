
import sys
import os


# Add the current directory or a specific directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'blender_scripts'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'utility'))
from setup_env import setup_env
from extract_3D_coordinates import extract_3d_coordinates
from projection_2D import projection
from estimate_3D_coordinates import compute_3d_points
from utility import parse_args

args = parse_args(sys.argv[5:])
print(sys.argv[5:])
ncam = 2 if  "n" not in args else  int(args["n"])
ncam = 2 if ncam>2 else ncam
ncam = 1 if ncam<1 else ncam

position_offest =  (0,0,0) if  "t" not in args else args["t"]
rotation = (0.16,0,0) if "r" not in args else args["r"]
light = False if "l" not in args else args["l"]



# Set up the scene
fbx_file_path = "./assets/GiuliaRigged.fbx"
cameras,armature = setup_env(fbx_file_path,num_cameras=ncam,position_offset = position_offest,rotation=rotation,light=light)


output_base_dir = "./out"

# Extract the 3 coordinates
bone_pairs_path =output_base_dir + "/bone_pairs.txt"
output_coordinates_3D_path = output_base_dir + "/bones_3D_coordinates.txt"
bone_coordinates_3d = extract_3d_coordinates(armature,output_coordinates_3D_path,bone_pairs_path)

bone_coordinates_2d =[]
# Compute the projection wrt to each camera
for i,camera in enumerate(cameras):
    output_file_path_2d = output_base_dir + f"/bones_2D_coordinates_{i+1}.txt"
    output_render = output_base_dir + f"/render_{i+1}.png"
    bone_coordinates_2d.append(projection(camera,bone_coordinates_3d,output_file_path_2d,output_render))
    


if len(bone_coordinates_2d) == 2:
    compute_3d_points(bone_coordinates_2d[0],bone_coordinates_2d[1],cameras[0],cameras[1])
