import subprocess
from highlight_points import draw_skeleton
import sys

import subprocess
import utility
import utility.utility

# Path to the Blender executable (adjust according to your system)
blender_path = "/usr/bin/blender"

# Path to the Blender script you want to execute
script_path = "./extract_info.py"
# Prepare arguments - include -n properly
arguments = [blender_path, '--background', '--python', script_path,"--"] + sys.argv[1:]

# Print arguments for debugging
print("Arguments:", arguments)
# Call Blender from the command line with the script
subprocess.run(arguments)



args = utility.utility.parse_args(sys.argv[1:])

ncam = 2 if  "n" not in args else  int(args["n"])
ncam = 2 if ncam>2 else ncam

output_base_dir = "./out"
for i in range(ncam):
    n = i+1
    image_path = output_base_dir+f"/render_{n}.png"
    coordinates_file = output_base_dir + f"/bones_2D_coordinates_{n}.txt"  # File containing 2D bone coordinates
    bone_pairs_file = output_base_dir + "/bone_pairs.txt"            # File containing bone pairs
    output_path = output_base_dir + f"/skeleton_{n}.png"
    draw_skeleton(image_path, coordinates_file, bone_pairs_file, output_path)

if n==2:

    #  Statistic fo the reconstruction
    file_path = './out/bones_3D_coordinates.txt'
    estimated_coordinates = utility.utility.create_coordinates_map('./out/reconstructed_3d_points.txt')
    extracted_coordinates = utility.utility.create_coordinates_map('./out/bones_3D_coordinates.txt')


    # Find common labels
    common_labels = set(estimated_coordinates.keys()).intersection(extracted_coordinates.keys())

    (mpjpe, ax, ay, az) = utility.utility.compute_results(common_labels,estimated_coordinates, extracted_coordinates)
    # All values are mutliplied by 1000 to obtain measure in mm
    print(f"Mean Per Joint Position Error (MPJPE): {mpjpe * 1000} mm")
    print(f"Mean Absolute Error X: {ax * 1000} mm")
    print(f"Mean Absolute Error Y: {ay * 1000} mm")
    print(f"Mean Absolute Error Z: {az * 1000} mm")
